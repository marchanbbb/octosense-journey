#!/usr/bin/env python3
"""Exercise the shipped Splash app through the real Makepad input bridge."""
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.parse
import urllib.request

APP = Path(__file__).resolve().parents[1]
OCTO = Path(os.environ.get('OCTO_TOOL', APP.parent / 'OctoScript-App-Design-Flow/tools/octo'))
PORT = int(os.environ.get('JOURNEY_TEST_PORT', '8153'))
BASE = f'http://127.0.0.1:{PORT}'
STATE = APP / 'build' / ('test-' + str(time.time_ns()))
STORE = STATE / 'journey/journeys.json'
RESULTS = []

def request(route, **params):
    url = BASE + route + ('?' + urllib.parse.urlencode(params) if params else '')
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)

def launch():
    subprocess.run([str(OCTO), 'run', str(APP/'bundle'), '--port', str(PORT), '--hidden', '--detach', '--app-data', str(STATE)], check=True)

def stop():
    request('/quit')
    for _ in range(50):
        try: request('/s')
        except Exception: return
        time.sleep(.1)
    raise AssertionError('Host did not exit')

def widgets():
    return request('/snap')['s']

def scroll(dy):
    request('/m', k='scroll', x=210, y=620, dy=dy, precise=1, wait=1)
    time.sleep(.08)

def locate(text=None, identity=None, ty=None):
    for pass_no in range(2):
        scroll(-5000)
        for _ in range(16):
            for w in widgets():
                x,y,width,height = w['r']
                if (text is None or w.get('t') == text) and (identity is None or w['i']==identity) and (ty is None or w['ty']==ty) and 0 <= y and y+height <= 846:
                    return w
            scroll(270)
    raise AssertionError(f'Widget not found: {text or identity}; {[w.get("t") for w in widgets() if w["ty"] != "Splash"]}')

def click(text):
    w=locate(text=text,ty='Button'); x,y,width,height=w['r']
    request('/click',x=x+width/2,y=y+height/2,wait=1)

def enter(identity,text):
    w=locate(identity=identity,ty='TextInput'); x,y,width,height=w['r']
    request('/click',x=x+width/2,y=y+height/2,wait=1)
    request('/t',t=text,wait=1)

def has(text):
    locate(text=text,ty='Label')

def state():
    return json.loads(STORE.read_text())['tasks']

def passed(name):
    RESULTS.append(name); print('PASS:',name,flush=True)

def main():
    owned=False
    try:
        launch(); owned=True
        has('买到，还要用好。'); passed('empty state')
        click('新建 +'); click('创建任务'); has('请填写商品或任务名称。'); passed('required title validation')
        enter('product','卧室空调'); enter('order_no','ORDER-002'); enter('tracking_no','TRACK-002'); click('创建任务')
        assert len(state())==1 and state()[0]['title']=='卧室空调'
        click('记录已发货'); assert state()[0]['phase']==1; passed('manual create and dispatch')
        click('任务'); click('打开空调演示'); assert len(state())==2; passed('demo task remains separate')
        click('演示：配送延误'); has('配送超时，联系物流'); assert state()[1]['due'] < time.time()
        click('记录已联系物流'); has('等待物流反馈，核实到货'); assert state()[1]['contacted']; passed('delay changes next action')
        click('确认已收货'); assert state()[1]['phase']==2 and not state()[1]['contacted']; has('记录安装时间，确认安装条件'); passed('receipt retires delivery tasks')
        click('填写安装安排'); click('保存记录'); has('请先填写内容。')
        enter('detail_input','10月3日 09:00-12:00，已与师傅确认'); click('保存记录'); assert state()[1]['phase']==3; passed('installation appointment and validation')
        click('记录售后问题'); enter('detail_input','配件缺失，需要补发'); click('保存记录'); assert state()[1]['issue']=='配件缺失，需要补发'
        has('跟进售后处理结果'); click('记录售后已解决'); assert state()[1]['phase']==3 and state()[1]['issue']==''; passed('aftersales restores interrupted installation phase')
        click('确认安装并验收'); assert state()[1]['phase']==4; has('本次任务已完成'); passed('acceptance closes task')
        click('记录售后问题'); enter('detail_input','使用时有异响'); click('保存记录'); assert state()[1]['phase']==4 and state()[1]['issue']
        click('记录售后已解决'); assert state()[1]['phase']==4 and not state()[1]['issue']; passed('post-completion aftersales lifecycle')
        click('请系统模型分析下一步'); has('系统模型暂不可用；继续使用上方规则待办。'); passed('model unavailable fallback')
        assert state()[0]['phase']==1 and state()[0]['title']=='卧室空调'; passed('no cross-task mutation')
        click('待办'); has('卧室空调')
        assert not any(w.get('t')=='客厅空调 · 送装一体' for w in widgets() if w['ty']=='Label'); passed('completed task removed from pending')
        before=STORE.read_text(); stop(); owned=False
        launch(); owned=True
        assert STORE.read_text()==before
        click('任务'); has('卧室空调'); click('打开空调演示'); has('本次任务已完成'); passed('restart persistence')
        log=(STATE/'card-host.log').read_text()
        assert '[E]' not in log and 'on_render closure failed' not in log, log[-4000:]
        stop(); owned=False
        STORE.write_text('{broken')
        launch(); owned=True; has('存档需要修复'); assert STORE.read_text()=='{broken'; passed('corrupt storage preserved and edits blocked')
    finally:
        if owned: stop()
        (APP/'build/native-results.json').write_text(json.dumps({'passed':RESULTS,'state_dir':str(STATE)},ensure_ascii=False,indent=2)+'\n')
    print(f'{len(RESULTS)} checks passed')


if __name__ == "__main__":
    main()
