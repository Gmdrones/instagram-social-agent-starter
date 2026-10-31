"""Independent, configurable public-web discovery of Instagram prospects.

Uses the user's own Brave Search API key; never imports publisher contacts or sessions.
Produces a locally deduplicated review list, not automatic follows or cold DMs.
"""
import argparse,datetime,json,os,re,sqlite3,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(os.environ.get("SOCIAL_AGENT_HOME",Path.home()/".social-agent")).expanduser()
DB=ROOT/"social.db"; CONFIG=ROOT/"config.json"
PATTERN=re.compile(r"(?:https?://)?(?:www\.)?instagram\.com/([a-zA-Z0-9._]{1,30})(?:/|\?|$)",re.I)
RESERVED={"p","reel","reels","stories","explore","accounts","direct","about","privacy","developer"}
def database():
 ROOT.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(DB)
 c.execute("CREATE TABLE IF NOT EXISTS prospects(handle TEXT PRIMARY KEY, niche TEXT, region TEXT, source_url TEXT, title TEXT, stage TEXT DEFAULT 'review', found_at TEXT)")
 return c
def search(niche,region,limit):
 key=os.getenv("BRAVE_SEARCH_API_KEY","")
 if not key:raise SystemExit("Configure your own BRAVE_SEARCH_API_KEY for public web discovery")
 query=f'site:instagram.com {niche} {region}'
 url="https://api.search.brave.com/res/v1/web/search?"+urllib.parse.urlencode({"q":query,"count":min(20,max(1,limit))})
 req=urllib.request.Request(url,headers={"X-Subscription-Token":key,"Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=25) as response: body=json.load(response)
 return body.get("web",{}).get("results",[])
def discover(args):
 cfg=json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
 niche=args.niche or cfg.get("niche","")
 region=args.region if args.region is not None else cfg.get("region","")
 if not niche:raise SystemExit("Supply --niche or configure your own niche")
 results=search(niche,region,args.limit)
 c=database();new=0
 for x in results:
  u=x.get("url","")
  m=PATTERN.search(u)
  if not m or m.group(1).lower() in RESERVED:continue
  handle=m.group(1).lower()
  cur=c.execute("INSERT OR IGNORE INTO prospects(handle,niche,region,source_url,title,stage,found_at) VALUES(?,?,?,?,?,'review',?)",(handle,niche,region,u,x.get("title",""),datetime.datetime.now(datetime.timezone.utc).isoformat()))
  new+=cur.rowcount
 c.commit();c.close()
 print(f"Found {len(results)} search results, added {new} unique accounts to LOCAL review queue.")
 print("Candidates are unverified and have NOT been followed or contacted.")
def listing(args):
 c=database()
 for handle,niche,region,url,stage in c.execute("SELECT handle,niche,region,source_url,stage FROM prospects ORDER BY found_at DESC LIMIT ?",(args.limit,)):
  print(f"@{handle} | {niche} | {region} | {stage} | {url}")
 c.close()
def plan(args):
 cfg=json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}
 c=database()
 rows=c.execute("SELECT handle,niche,region,source_url FROM prospects WHERE stage='review' ORDER BY found_at DESC LIMIT ?",(args.limit,)).fetchall()
 for handle,niche,region,url in rows:
  message=cfg.get("message_template") or cfg.get("message") or "Olá, somos {company}."
  message=message.format(company=cfg.get("company","sua empresa"),niche=niche,website=cfg.get("website",""))
  print(f"@{handle}: {url}\n  SUGESTÃO PARA REVISÃO HUMANA: {message}\n")
 print(f"{len(rows)} items prepared. No follows or Directs sent.")
 c.close()
def main():
 p=argparse.ArgumentParser(description="Configurable, independent niche discovery")
 sub=p.add_subparsers(dest="cmd",required=True)
 s=sub.add_parser("discover");s.add_argument("--niche");s.add_argument("--region");s.add_argument("--limit",type=int,default=20);s.set_defaults(fn=discover)
 s=sub.add_parser("list");s.add_argument("--limit",type=int,default=50);s.set_defaults(fn=listing)
 s=sub.add_parser("plan");s.add_argument("--limit",type=int,default=20);s.set_defaults(fn=plan)
 args=p.parse_args();args.fn(args)
if __name__=="__main__":main()
