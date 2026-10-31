import os,tempfile,unittest,subprocess,importlib.util,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CORE=ROOT/"src/social_agent/core.py"
SERVICE=ROOT/"src/social_agent/service.py"
class StarterTests(unittest.TestCase):
 def run_cmd(self,script,*args,env=None):
  return subprocess.run([sys.executable,str(script),*args],capture_output=True,text=True,env=env)
 def test_cli_help(self):
  p=self.run_cmd(CORE,"--help");self.assertEqual(p.returncode,0)
 def test_setup_draft(self):
  with tempfile.TemporaryDirectory() as d:
   env={**os.environ,"SOCIAL_AGENT_HOME":d}
   self.assertEqual(self.run_cmd(CORE,"init",env=env).returncode,0)
   self.assertEqual(self.run_cmd(SERVICE,"setup","--company","Example",env=env).returncode,0)
   self.assertIn("NÃO ENVIADO",self.run_cmd(CORE,"draft",env=env).stdout)
 def test_no_automatic_outbound(self):
  p=self.run_cmd(CORE,"send");self.assertIn("Sending disabled",p.stdout)
 def test_signed_event_queue_dedup(self):
  with tempfile.TemporaryDirectory() as d:
   os.environ["SOCIAL_AGENT_HOME"]=d
   spec=importlib.util.spec_from_file_location("service_test",str(SERVICE))
   m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
   from argparse import Namespace
   m.setup(Namespace(company="Example",niche="design",region="",message=None,website="",auto_reply=False))
   event={"entry":[{"messaging":[{"sender":{"id":"123"},"message":{"mid":"m-1","text":"Hello"}}]}]}
   self.assertEqual(m.process_event(event),1)
   self.assertEqual(m.process_event(event),0)
   c=m.db()
   self.assertEqual(c.execute("SELECT COUNT(*) FROM outbox").fetchone()[0],1)
   self.assertEqual(c.execute("SELECT state FROM outbox").fetchone()[0],"eligible_review")
   c.close()
