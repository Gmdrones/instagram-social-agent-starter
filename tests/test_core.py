import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
class StarterTests(unittest.TestCase):
 def test_cli_help(self):
  from subprocess import run
  p=run(["python","src/social_agent/core.py","--help"],capture_output=True,text=True)
  self.assertEqual(p.returncode,0)
  self.assertIn("draft",p.stdout)
 def test_init_and_draft(self):
  from subprocess import run
  with tempfile.TemporaryDirectory() as d:
   env={**os.environ,"SOCIAL_AGENT_HOME":d}
   a=run(["python","src/social_agent/core.py","init"],env=env,capture_output=True,text=True)
   b=run(["python","src/social_agent/core.py","draft"],env=env,capture_output=True,text=True)
   self.assertEqual(a.returncode,0);self.assertEqual(b.returncode,0)
   self.assertTrue((Path(d)/"config.json").exists())
   self.assertIn("NÃO ENVIADO",b.stdout)
 def test_no_live_send(self):
  from subprocess import run
  p=run(["python","src/social_agent/core.py","send"],capture_output=True,text=True)
  self.assertEqual(p.returncode,0)
  self.assertIn("Sending disabled",p.stdout)
