#!/usr/bin/env python3
"""Run an isolated OctoSense desktop against the private development catalog."""
import json
import os
from pathlib import Path
import sys
APP=Path(__file__).resolve().parents[1]
settings=APP/'build/local-store.json'
if not settings.exists():
    raise SystemExit('Run python3 scripts/prepare-local-store.py first.')
store=json.loads(settings.read_text())
os.environ.update(OCTOSENSE_HUB=store['mirror'],OCTOSENSE_HUB_ANCHOR=store['anchor'],OCTOSENSE_HOME=str(APP/'build/desktop-home'),OCTOSENSE_APP_DATA=str(APP/'build/desktop-apps'),MAKEPAD_BUNDLE_NAME='OctoSense · 顺程')
binary=Path(os.environ.get('OCTOSENSE_BIN',APP.parent/'OctoSense/target/release/octosense'))
os.chdir(APP.parent/'OctoSense')
args=sys.argv[1:]
if not args:
    installed=(APP/'build/desktop-apps/journey/bundle/manifest.json').exists()
    args=['--test-action','launch-hub:journey' if installed else 'launch-apphub']
os.execv(str(binary),[str(binary),*args])
