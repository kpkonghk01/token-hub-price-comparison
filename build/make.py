# -*- coding: utf-8 -*-
"""build/template.html + data.json  ->  index.html（單一自足檔案）"""
import os, subprocess, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

subprocess.check_call([sys.executable, os.path.join(BASE, 'build', 'build_data.py')])

tpl  = open(os.path.join(BASE, 'build', 'template.html'), encoding='utf-8').read()
data = open(os.path.join(BASE, 'data.json'), encoding='utf-8').read()
# `</` 喺 <script> 入面會提早收尾，JSON 容許 \/ 轉義，所以安全咁避開
data = data.replace('</', '<\\/')
assert tpl.count('@@PAYLOAD@@') == 1, 'template 入面要啱啱好一個 @@PAYLOAD@@'
out = tpl.replace('@@PAYLOAD@@', data)
path = os.path.join(BASE, 'index.html')
open(path, 'w', encoding='utf-8').write(out)
print('index.html %d bytes' % len(out))
