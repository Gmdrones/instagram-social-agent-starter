"""Local Instagram business assistant. Official Meta API only; no cold DMs or following."""
from __future__ import annotations
import argparse,datetime as dt,json,os,re,sqlite3,urllib.error,urllib.request
from pathlib import Path
ROOT=Path(os.environ.get("SOCIAL_AGENT_HOME",Path.home()/".social-agent")).expanduser()
CONFIG=ROOT/"config.json"; DB=ROOT/"social.db"
def connect():
 ROOT.mkdir(parents=True,exist_ok=True)
 db=sqlite3.connect(DB)
 db.execute("CREATE TABLE IF NOT EXISTS leads(id INTEGER PRIMARY KEY, handle TEXT UNIQUE NOT NULL,niche TEXT NOT NULL,source TEXT,notes TEXT,status TEXT DEFAULT 'research',created TEXT NOT NULL)")
 return db
def init(a):
 if CONFIG.exists() and not a.force:
  print("Already configured:",CONFIG);return
 ROOT.mkdir(parents=True,exist_ok=True)
 CONFIG.write_text(json.dumps({"company":"Your business","niche":"Your audience","website":"https://example.com","message_template":"Olá! Obrigado por falar com {company}. Como podemos ajudar?","api_version":"v24.0"},ensure_ascii=False,indent=2),encoding="utf-8")
 connect().close();print("Configured:",CONFIG)
def lead(a):
 h=a.handle.strip().lstrip("@").lower()
 if not re.fullmatch(r"[a-z0-9._]{1,30}",h):raise SystemExit("Invalid handle")
 with connect() as db: db.execute("INSERT OR IGNORE INTO leads(handle,niche,source,notes,created) VALUES(?,?,?,?,?)",(h,a.niche,a.source,a.notes,dt.datetime.now(dt.timezone.utc).isoformat()))
 print("Saved or already present:",h)
def listed(a):
 with connect() as db:
  for row in db.execute("SELECT handle,niche,status,COALESCE(source,'') FROM leads ORDER BY id DESC LIMIT ?",(max(1,a.limit),)):print(" | ".join(map(str,row)))
def draft(a):
 c=json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
 t=a.template or c.get("message_template","Olá! Como podemos ajudar?")
 print(t.format(company=c.get("company","nossa empresa"),niche=c.get("niche",""),website=c.get("website","")))
 print("RASCUNHO — NÃO ENVIADO")
def meta_me(a):
 token=os.environ.get("IG_ACCESS_TOKEN")
 if not token:raise SystemExit("IG_ACCESS_TOKEN not set")
 c=json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
 v=c.get("api_version","v24.0")
 if not re.fullmatch(r"v\d+\.\d+",v):raise SystemExit("Invalid API version")
 req=urllib.request.Request("https://graph.instagram.com/"+v+"/me?fields=id,username,account_type",headers={"Authorization":"Bearer "+token})
 try:
  with urllib.request.urlopen(req,timeout=18) as f:r=json.load(f)
 except urllib.error.HTTPError as e:raise SystemExit("Meta HTTP "+str(e.code)+" — check permissions")
 print(json.dumps({k:r.get(k) for k in ("id","username","account_type")},ensure_ascii=False))
def test_inbound(a):
 print("Local simulation only; not verified by Meta. ID:",a.recipient)
def send(a):
 print("Sending disabled: requires verified official Meta messaging integration, eligible inbound conversations and app permissions.")
def main():
 p=argparse.ArgumentParser(description="Instagram Social Agent — safe local starter")
 s=p.add_subparsers(dest="command",required=True)
 c=s.add_parser("init");c.add_argument("--force",action="store_true");c.set_defaults(func=init)
 c=s.add_parser("lead");c.add_argument("handle");c.add_argument("--niche",required=True);c.add_argument("--source",default="");c.add_argument("--notes",default="");c.set_defaults(func=lead)
 c=s.add_parser("list");c.add_argument("--limit",type=int,default=50);c.set_defaults(func=listed)
 c=s.add_parser("draft");c.add_argument("--template");c.set_defaults(func=draft)
 c=s.add_parser("meta-me");c.set_defaults(func=meta_me)
 c=s.add_parser("test-inbound");c.add_argument("recipient");c.add_argument("--at",required=True);c.set_defaults(func=test_inbound)
 c=s.add_parser("send");c.set_defaults(func=send)
 s.parse_args().func(s.parse_args())
if __name__=="__main__":main()
