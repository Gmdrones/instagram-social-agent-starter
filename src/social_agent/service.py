"""Production-oriented local orchestration for eligible Instagram business conversations.

Official Meta APIs only. No scraping, arbitrary following, or unsolicited outbound DMs.
Requires public HTTPS webhook URL and approved Meta permissions for live service.
"""
import argparse,datetime,json,os,sqlite3,time,urllib.request,urllib.error,hmac,hashlib
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
ROOT=Path(os.environ.get("SOCIAL_AGENT_HOME",Path.home()/".social-agent")).expanduser()
CONFIG=ROOT/"config.json"; DB=ROOT/"social.db"
def settings():
 if not CONFIG.exists(): raise RuntimeError("Run setup first")
 return json.loads(CONFIG.read_text(encoding="utf-8"))
def db():
 ROOT.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(DB,timeout=20)
 c.execute("PRAGMA journal_mode=WAL")
 c.execute("CREATE TABLE IF NOT EXISTS contacts (sender TEXT PRIMARY KEY, first_seen TEXT, last_seen TEXT, last_message TEXT, state TEXT)")
 c.execute("CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, sender TEXT, received_at TEXT, body TEXT, processed INTEGER DEFAULT 0)")
 c.execute("CREATE TABLE IF NOT EXISTS outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, recipient TEXT, text TEXT, state TEXT DEFAULT 'review', requested_at TEXT, delivered_at TEXT, platform_id TEXT, error TEXT)")
 c.execute("CREATE TABLE IF NOT EXISTS activity (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, kind TEXT, details TEXT)")
 return c
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def setup(args):
 ROOT.mkdir(parents=True,exist_ok=True)
 current=json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
 for k in ("company","niche","region","message","website"):
  v=getattr(args,k,None)
  if v:current[k]=v
 current.setdefault("company","My Business");current.setdefault("niche","my audience")
 current.setdefault("region","");current.setdefault("website","")
 current.setdefault("message","Olá! Obrigado pelo contato com {company}. Como podemos ajudar?")
 current.setdefault("auto_reply",False);current.setdefault("daily_limit",20)
 if args.auto_reply:current["auto_reply"]=True
 CONFIG.write_text(json.dumps(current,indent=2,ensure_ascii=False),encoding="utf-8")
 db().close();print("Saved local configuration:",CONFIG)
def log(c,kind,details):c.execute("INSERT INTO activity(date,kind,details) VALUES(?,?,?)",(utc(),kind,details))
def process_event(payload):
 c=db(); added=0
 for entry in payload.get("entry",[]):
  for e in entry.get("messaging",[]):
   sender=(e.get("sender") or {}).get("id")
   msg=e.get("message") or {}
   mid=msg.get("mid")
   if not sender or not mid or msg.get("is_echo"):continue
   body=msg.get("text") or "[media/nontext]"
   cur=c.execute("INSERT OR IGNORE INTO events(event_id,sender,received_at,body) VALUES(?,?,?,?)",(mid,sender,utc(),body))
   if cur.rowcount==0:continue
   c.execute("INSERT INTO contacts(sender,first_seen,last_seen,last_message,state) VALUES(?,?,?,?,?) ON CONFLICT(sender) DO UPDATE SET last_seen=excluded.last_seen,last_message=excluded.last_message",(sender,utc(),utc(),body,"inbound"))
   conf=settings()
   draft=conf["message"].format(company=conf["company"],niche=conf["niche"],website=conf["website"])
   c.execute("INSERT INTO outbox(recipient,text,state,requested_at) VALUES(?,?,?,?)",(sender,draft,"eligible_review",utc()))
   log(c,"inbound",mid);added+=1
 c.commit();c.close();return added
def send_meta(recipient,message):
 token=os.getenv("META_ACCESS_TOKEN")
 account=os.getenv("META_IG_USER_ID")
 if not token or not account:raise RuntimeError("META_ACCESS_TOKEN and META_IG_USER_ID required")
 ver=os.getenv("META_API_VERSION","v24.0")
 import re
 if not re.fullmatch(r"v\d+\.\d+",ver):raise RuntimeError("Bad API version")
 url=f"https://graph.instagram.com/{ver}/{account}/messages"
 content=json.dumps({"recipient":{"id":recipient},"message":{"text":message}}).encode()
 req=urllib.request.Request(url,data=content,headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},method="POST")
 try:
  with urllib.request.urlopen(req,timeout=25) as resp: return json.load(resp)
 except urllib.error.HTTPError as e:raise RuntimeError(f"Meta HTTP {e.code}: check API permissions and messaging eligibility")
def approve(args):
 c=db();row=c.execute("SELECT recipient,text,state FROM outbox WHERE id=?",(args.id,)).fetchone()
 if not row:raise RuntimeError("Unknown draft")
 if row[2]!="eligible_review":raise RuntimeError("Draft is not awaiting review")
 c.execute("UPDATE outbox SET state='approved' WHERE id=?",(args.id,));c.commit();c.close()
 print("Approved draft; use dispatch to send using official Meta API")
def dispatch(args):
 c=db();row=c.execute("SELECT recipient,text,state FROM outbox WHERE id=?",(args.id,)).fetchone()
 if not row or row[2]!="approved":raise RuntimeError("Only approved replies can be sent")
 try:
  result=send_meta(row[0],row[1]);mid=str(result.get("message_id",result.get("id","")))
  if not mid:raise RuntimeError("Meta did not return message id")
  c.execute("UPDATE outbox SET state='sent',delivered_at=?,platform_id=? WHERE id=?",(utc(),mid,args.id))
  log(c,"sent",mid);c.commit();print("Meta accepted message ID:",mid)
 except Exception as e:
  c.execute("UPDATE outbox SET error=? WHERE id=?",(str(e),args.id));c.commit();raise
 finally:c.close()
def status(args):
 c=db()
 print("Contacts:",c.execute("SELECT COUNT(*) FROM contacts").fetchone()[0])
 print("Outbox:",c.execute("SELECT state,COUNT(*) FROM outbox GROUP BY state").fetchall())
 print("Recent:",c.execute("SELECT id,recipient,state FROM outbox ORDER BY id DESC LIMIT 15").fetchall())
 c.close()
def report(args):
 c=db()
 for day,kind,n in c.execute("SELECT substr(date,1,10),kind,count(*) FROM activity GROUP BY 1,2 ORDER BY 1 DESC,2"):
  print(day,kind,n)
 c.close()
def serve(args):
 secret=os.getenv("META_APP_SECRET","")
 verify=os.getenv("META_VERIFY_TOKEN","")
 if not secret or not verify:raise RuntimeError("Set META_APP_SECRET and META_VERIFY_TOKEN (never commit these)")
 class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
   from urllib.parse import urlsplit,parse_qs
   p=urlsplit(self.path)
   if p.path=="/health":
    self.send_response(200);self.end_headers();self.wfile.write(b"ok");return
   if p.path!="/webhook":self.send_error(404);return
   q=parse_qs(p.query)
   if q.get("hub.mode")==["subscribe"] and hmac.compare_digest(q.get("hub.verify_token",[""])[0],verify):
    challenge=q.get("hub.challenge",[""])[0].encode()
    self.send_response(200);self.end_headers();self.wfile.write(challenge)
   else:self.send_error(403)
  def do_POST(self):
   if self.path!="/webhook":self.send_error(404);return
   try:
    size=int(self.headers.get("Content-Length","0"))
    if size<1 or size>1024*1024: self.send_error(413);return
    body=self.rfile.read(size)
    signature=self.headers.get("X-Hub-Signature-256","")
    expected="sha256="+hmac.new(secret.encode(),body,hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,signature):self.send_error(403);return
    n=process_event(json.loads(body));self.send_response(200);self.end_headers();self.wfile.write(f"accepted {n}".encode())
   except Exception as exc:
    print("Webhook error",type(exc).__name__);self.send_error(500)
 print("Listening locally:",args.host,args.port," (provide HTTPS reverse proxy for Meta)")
 ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest="cmd",required=True)
 s=sub.add_parser("setup")
 for x in ("company","niche","region","message","website"):s.add_argument("--"+x)
 s.add_argument("--auto-reply",action="store_true");s.set_defaults(fn=setup)
 s=sub.add_parser("serve");s.add_argument("--host",default="127.0.0.1");s.add_argument("--port",type=int,default=8765);s.set_defaults(fn=serve)
 s=sub.add_parser("status");s.set_defaults(fn=status)
 s=sub.add_parser("report");s.set_defaults(fn=report)
 s=sub.add_parser("approve");s.add_argument("id",type=int);s.set_defaults(fn=approve)
 s=sub.add_parser("dispatch");s.add_argument("id",type=int);s.set_defaults(fn=dispatch)
 a=p.parse_args();a.fn(a)
if __name__=="__main__":main()
