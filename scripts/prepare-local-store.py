#!/usr/bin/env python3
"""Build a private, disposable catalog for local OctoSense testing only."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import time

APP=Path(__file__).resolve().parents[1]
HUB=Path(os.environ.get('OCTO_HUB',APP.parent/'OctoSense-App-Hub/target/release/hub'))
def hub(*args):
    return subprocess.check_output([str(HUB),*map(str,args)],text=True).strip()

def main():
    os.umask(0o077)
    out=APP/'build'/('local-store-'+str(time.time_ns()))
    out.mkdir(parents=True)
    keys=out/'keys'; keys.mkdir()
    bundle=out/'bundle'; shutil.copytree(APP/'bundle',bundle)
    anchor=hub('keygen',keys/'anchor.key')
    hub('keygen',keys/'working.key')
    pub=hub('keygen',keys/'publisher.key')
    cert=hub('certify','--anchor',keys/'anchor.key','--working',keys/'working.key')
    hub('stamp',bundle)
    hub('sign-manifest',bundle,'--key',keys/'publisher.key','--key-id','local-demo')
    mirror=out/'mirror'; mirror.mkdir()
    print(hub('publish',bundle,'--catalog',mirror/'catalog.json','--key',keys/'working.key','--anchor-cert',cert,'--publisher','local-demo','--publisher-key','local-demo='+pub,'--out',mirror))
    print(hub('verify',mirror/'catalog.json','--anchor',anchor))
    (APP/'build/local-store.json').write_text(json.dumps({'mirror':str(mirror),'anchor':anchor},indent=2)+'\n')
    print('Local test only. No remote publication. Source bundle remains unsigned.')
if __name__=='__main__': main()
