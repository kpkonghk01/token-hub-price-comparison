# -*- coding: utf-8 -*-
"""
把 providers/ 下的原始報價資料整理成一份 JSON，供 index.html 使用。
資料來源：
  A. providers/Gemini Developer API 定價.md            -> Google 官方定價 (paid tier, standard)
  B. providers/tencent/模型价格.md                       -> 騰訊雲「語言模型/視覺模型」平台 (新加坡/廣州/矽谷)
  C. providers/tencent/模型单价/*.png                    -> 騰訊雲「VOD AIGC」平台 (國內站 CNY / 國際站 USD)，人手轉錄
  D. providers/yz/悦如Token Hub模型报价单.xlsx           -> 悅智 TokenHub 的「折扣率」(不是絕對價)
所有價格單位：USD / 1M tokens（文本）、USD / 張（圖片）、USD / 秒（影片）
"""
import json, os, collections

OUT = os.path.join(os.path.dirname(__file__), '..', 'data.json')

# ---------------------------------------------------------------- 悅智折扣
# 來自 D：報價單「TokenHub平台」欄。折扣是對「原廠官方價」的乘數。
YZ_FACTOR = {
    'anthropic': 0.85, 'google': 0.75, 'openai': 0.80, 'zhipu': 0.85,
    'deepseek': 0.70, 'minimax': 0.85, 'moonshot': 0.95, 'tencent': 0.65,
    'bytedance': 0.70, 'seedream': 0.95, 'seedance': 0.95, 'vidu': 0.70,
    'kling': 0.70, 'pixverse': 0.70, 'hailuo': 0.70, 'alibaba': 0.70,
}
# 個別覆寫（報價單上單獨列出的例外）
YZ_OVERRIDE = {
    'moonshot:K3': 1.00,          # Kimi K3 冇折
    'tencent:Vision 2.0 Instruct': 0.70,
}
# 報價單上明確列出的型號（用嚟標示「報價單有列」定「同廠推算」）
YZ_LISTED = {
 'anthropic': ['Opus 4.8','Opus 4.7','Sonnet 4.6','Opus 4.6','Opus 4.5','Sonnet 4.5','Haiku 4.5'],
 'google': ['3.0-flash','3.1-flash-lite-preview','3.1-flash-lite','3.1-pro','3.5-flash','veo 3.1','veo 3.1-fast','veo 3.1-lite'],
 'openai': ['5.3-codex','5.3-chat-latest','5.2-chat-latest','5.4','5.4-nano','5.4-mini','5.4-pro','5.5','5-nano','5.5-pro','image-2'],
 'zhipu': ['5','5.1','5.1-Turbo','5.2','5-Turbo','5V-Turbo'],
 'deepseek': ['V3.2','V4-Flash','V4-Pro'],
 'minimax': ['M2.5','M2.7','M3'],
 'moonshot': ['K2.5','K2.6','K2.7 Code','K3'],
 'tencent': ['Hy3','Hy3 preview','Hunyuan 3.0','MT2 Plus','MT2 Pro'],
}

VENDOR_LABEL = {
 'google':'Google','anthropic':'Anthropic','openai':'OpenAI','xai':'xAI (Grok)',
 'zhipu':'智譜 GLM','moonshot':'月之暗面 Kimi','deepseek':'DeepSeek','minimax':'MiniMax',
 'tencent':'騰訊混元','stepfun':'階躍星辰','bytedance':'字節','seedream':'字節 Seedream',
 'seedance':'字節 Seedance','vidu':'生數 Vidu','kling':'快手可靈','pixverse':'愛詩 PixVerse',
 'hailuo':'MiniMax 海螺','alibaba':'阿里','midjourney':'Midjourney','qwen':'阿里千問','other':'其他',
}

rows = []
def T(vendor, model, variant, official=None, ob=None, sg=None, gz=None, intl=None,
      note=None, cond=None, peak=None):
    """official/sg/gz/intl 格式：[input, cacheIn, output]（缺值用 None）"""
    rows.append(dict(kind='t2t', vendor=vendor, model=model, variant=variant or '',
                     cond=cond or '', peak=peak, note=note or '',
                     p=dict(official=official, tcSG=sg, tcGZ=gz, tcINTL=intl),
                     officialBase=ob))

# ============================================================ GOOGLE GEMINI
# official = Gemini Developer API 定價.md (Paid tier / Standard)
# intl     = 騰訊 VOD AIGC 國際站 (4.2 AIGC多模態理解.png，GG 廠商)
G = 'google'
T(G,'Gemini 3.8 Flash','', [0.75,0.075,3.75],'google-doc', intl=[0.75,0.075,3.75],
  cond='2026-12-31 前價', note='2027-01-01 起：1.50 / 0.15 / 7.50')
T(G,'Gemini 3.8 Flash','', [1.50,0.15,7.50],'google-doc', intl=[1.50,0.15,7.50], cond='2027-01-01 起價')
T(G,'Gemini 3.7 Flash','', [0.75,0.075,3.75],'google-doc', intl=[0.75,0.075,3.75], cond='2026-12-31 前價')
T(G,'Gemini 3.7 Flash','', [1.50,0.15,7.50],'google-doc', intl=[1.50,0.15,7.50], cond='2027-01-01 起價')
T(G,'Gemini 3.6 Flash','', [0.75,0.075,3.75],'google-doc', intl=[0.75,0.075,3.75], cond='2026-12-31 前價')
T(G,'Gemini 3.5 Flash','', [1.50,0.15,9.00],'google-doc', intl=[1.50,0.15,9.00], cond='文字/圖/影片/音訊')
T(G,'Gemini 3.5 Flash-Lite','', [0.30,0.03,2.50],'google-doc', intl=[0.30,0.03,2.50])
T(G,'Gemini 3.1 Pro Preview','', [2.00,0.20,12.00],'google-doc', intl=[2.00,0.20,12.00], cond='輸入 ≤200k token')
T(G,'Gemini 3.1 Pro Preview','', [4.00,0.40,18.00],'google-doc', intl=[4.00,0.40,18.00], cond='輸入 >200k token')
T(G,'Gemini 3.1 Flash-Lite','', [0.25,0.025,1.50],'google-doc', intl=[0.25,0.025,1.50], cond='文字/圖/影片')
T(G,'Gemini 3.1 Flash-Lite','', [0.50,0.05,1.50],'google-doc', intl=[0.50,0.05,1.50], cond='音訊輸入')
T(G,'Gemini 3.1 Flash-Lite Preview','', [0.25,0.025,1.50],'google-doc', intl=[0.25,0.025,1.50], cond='文字/圖/影片')
T(G,'Gemini 3 Flash Preview','', [0.50,0.05,3.00],'google-doc', intl=[0.50,0.05,3.00], cond='文字/圖/影片')
T(G,'Gemini 3 Flash Preview','', [1.00,0.10,3.00],'google-doc', intl=[1.00,0.10,3.00], cond='音訊輸入')
T(G,'Gemini Omni Flash','', [1.50,None,9.00],'google-doc', cond='文字輸出', note='影片輸出 $17.50')
T(G,'Gemini 2.5 Pro','', [1.25,0.125,10.00],'google-doc', intl=[1.25,0.125,10.00], cond='輸入 ≤200k token')
T(G,'Gemini 2.5 Pro','', [2.50,0.25,15.00],'google-doc', intl=[2.50,0.25,15.00], cond='輸入 >200k token')
T(G,'Gemini 2.5 Flash','', [0.30,0.03,2.50],'google-doc', intl=[0.30,0.03,2.50], cond='文字/圖/影片')
T(G,'Gemini 2.5 Flash','', [1.00,0.10,2.50],'google-doc', intl=[1.00,0.10,2.50], cond='音訊輸入')
T(G,'Gemini 2.5 Flash-Lite','', [0.10,0.01,0.40],'google-doc', cond='文字/圖/影片')
T(G,'Gemini 2.5 Flash-Lite','', [0.30,0.03,0.40],'google-doc', cond='音訊輸入')
T(G,'Gemini 3.5 Transcribe','', [2.00,None,12.00],'google-doc', cond='音訊轉錄')
T(G,'Gemini 3.5 Live Translate','', [3.50,None,21.00],'google-doc', cond='即時翻譯')

# ============================================================ ANTHROPIC CLAUDE
# 騰訊 VOD AIGC 國際站 CD 表 = Anthropic 官方 USD 目錄價
A='anthropic'
CD = [
 ('Claude Opus 5','',        [5.0,0.5,25.0]),
 ('Claude Sonnet 5','',      [3.0,0.3,15.0],'2026-09-01 調價後'),
 ('Claude Sonnet 5','',      [2.0,0.2,10.0],'2026-08-31 前'),
 ('Claude Fable 5','',       [10.0,1.0,50.0]),
 ('Claude Opus 4.8','',      [5.0,0.5,25.0]),
 ('Claude Opus 4.7','',      [5.0,0.5,25.0]),
 ('Claude Opus 4.6','',      [5.0,0.5,25.0]),
 ('Claude Opus 4.5','',      [5.0,0.5,25.0]),
 ('Claude Sonnet 4.6','',    [3.0,0.3,15.0]),
 ('Claude Sonnet 4.5','',    [3.0,0.3,15.0],'≤200K token'),
 ('Claude Sonnet 4.5','',    [6.0,0.6,22.5],'>200K token'),
 ('Claude Haiku 4.5','',     [1.0,0.1,5.0]),
]
for r in CD:
    name,var,pr = r[0],r[1],r[2]; cond = r[3] if len(r)>3 else ''
    T(A,name,var,pr,'tencent-intl',intl=pr,cond=cond,note='騰訊只有國際站供應')

# ============================================================ OPENAI
O='openai'
OG=[
 ('GPT 6-astra','', [10.0,1.0,50.0],'輸入 <272K'),
 ('GPT 6-astra','', [20.0,2.0,75.0],'輸入 >272K'),
 ('GPT 5.6-sol','', [4.0,0.4,20.0],'輸入 <272K・26.9.2 後限時優惠'),
 ('GPT 5.6-sol','', [8.0,0.8,30.0],'輸入 >272K・26.9.2 後限時優惠'),
 ('GPT 5.6-sol','', [5.0,0.5,30.0],'輸入 <272K・26.9.2 前價'),
 ('GPT 5.6-sol','', [10.0,1.0,45.0],'輸入 >272K・26.9.2 前價'),
 ('GPT 5.6-terra','',[2.0,0.2,12.0],'輸入 <272K'),
 ('GPT 5.6-terra','',[4.0,0.4,18.0],'輸入 >272K'),
 ('GPT 5.6-luna','', [0.2,0.02,1.2],'輸入 <272K'),
 ('GPT 5.6-luna','', [0.4,0.04,1.8],'輸入 >272K'),
 ('GPT 5.5','',      [5.0,0.5,30.0],'輸入 <272K'),
 ('GPT 5.5','',      [10.0,1.0,45.0],'輸入 >272K'),
 ('GPT 5.4-pro','',  [30.0,None,180.0],'輸入 <272K'),
 ('GPT 5.4-pro','',  [60.0,None,270.0],'輸入 >272K'),
 ('GPT 5.4','',      [2.5,0.25,15.0],'輸入 <272K'),
 ('GPT 5.4','',      [5.0,0.5,22.5],'輸入 >272K'),
 ('GPT 5.4-mini','', [0.75,0.075,4.5],''),
 ('GPT 5.4-nano','', [0.20,0.02,1.25],''),
 ('GPT 5.3-codex','',[1.75,0.18,14.0],''),
 ('GPT 5.3-chat-latest','',[1.75,0.18,14.0],''),
 ('GPT 5.2','',      [1.75,0.175,14.0],''),
 ('GPT 5.2-chat-latest','',[1.75,0.18,14.0],''),
 ('GPT 5.1','',      [1.25,0.125,10.0],''),
 ('GPT 5.1-chat-latest','',[1.25,0.125,10.0],''),
 ('GPT 5.1-chat','', [1.25,0.125,10.0],''),
 ('GPT 5','',        [1.25,0.125,10.0],''),
 ('GPT 5-chat-latest','',[1.25,0.125,10.0],''),
 ('GPT 5-mini','',   [0.25,0.025,2.0],''),
 ('GPT 5-nano','',   [0.05,0.005,0.40],''),
 ('GPT chat-latest','',[5.0,0.5,30.0],''),
 ('GPT 4.1','',      [2.0,0.5,8.0],''),
 ('GPT 4o','',       [2.5,1.25,10.0],''),
]
for name,var,pr,cond in OG:
    T(O,name,var,pr,'tencent-intl',intl=pr,cond=cond)

# ============================================================ xAI GROK (騰訊 GK，僅國際站)
X='xai'
for name,pr in [('Grok 4.3',[1.25,0.20,2.50]),('Grok 4.20-0309 reasoning',[1.25,0.20,2.50]),
                ('Grok 4.20-0309 non-reasoning',[2.00,0.20,6.00]),('Grok 4-1-fast-reasoning',[0.20,0.05,0.50])]:
    T(X,name,'',pr,'tencent-intl',intl=pr,note='悅智報價單無此廠')

# ============================================================ 智譜 GLM
Z='zhipu'
T(Z,'GLM-5.3','',      [1.4,0.26,4.4],'tencent-sg', sg=[1.4,0.26,4.4], gz=[1.1116,0.2779,3.8907])
T(Z,'GLM-5.3-Flash','',[0.15,0.03,0.50],'tencent-sg', sg=[0.15,0.03,0.50], gz=[0.11116,0.03196,0.38907],
  note='2026-09-10 23:59 前 5 折')
T(Z,'GLM-5.2','',      [1.4,0.26,4.4],'tencent-sg', sg=[1.4,0.26,4.4], gz=[1.12,0.28,3.92], intl=[1.232,0.308,4.312],
  note='矽谷區同價 1.4/4.4')
T(Z,'GLM-5.1','',      [1.4,0.26,4.4],'tencent-sg', sg=[1.4,0.26,4.4], gz=[0.84,0.182,3.36], intl=[0.924,0.200,3.696], cond='輸入 <32K')
T(Z,'GLM-5.1','',      [1.4,0.26,4.4],'tencent-sg', sg=[1.4,0.26,4.4], gz=[1.12,0.28,3.92], intl=[1.232,0.308,4.312], cond='輸入 ≥32K')
T(Z,'GLM-5','',        [1.0,0.20,3.2],'tencent-sg', sg=[1.0,0.20,3.2], gz=[0.573,0.115,2.58], intl=[0.616,0.154,2.772], cond='輸入 <32K')
T(Z,'GLM-5','',        [1.0,0.20,3.2],'tencent-sg', sg=[1.0,0.20,3.2], gz=[0.86,0.172,3.154], intl=[0.924,0.231,3.388], cond='輸入 ≥32K')
T(Z,'GLM-5-Turbo','',  [1.2,0.24,4.0],'tencent-sg', sg=[1.2,0.24,4.0], gz=[0.7,0.168,3.08], intl=[0.770,0.185,3.388], cond='輸入 <32K')
T(Z,'GLM-5-Turbo','',  [1.2,0.24,4.0],'tencent-sg', sg=[1.2,0.24,4.0], gz=[0.98,0.252,3.64], intl=[1.078,0.277,4.004], cond='輸入 ≥32K')
T(Z,'GLM-5V-Turbo','', [1.2,0.24,4.0],'tencent-sg', sg=[1.2,0.24,4.0], gz=[0.7,0.168,3.08], cond='輸入 <32K・視覺')
T(Z,'GLM-5V-Turbo','', [1.2,0.24,4.0],'tencent-sg', sg=[1.2,0.24,4.0], gz=[0.98,0.252,3.64], cond='輸入 ≥32K・視覺')
T(Z,'GLM-4.7','',      [0.308,0.062,1.232],'tencent-intl', intl=[0.308,0.062,1.232], cond='輸入 ≤32K・輸出 ≤0.2K')
T(Z,'GLM-4.7','',      [0.462,0.092,2.156],'tencent-intl', intl=[0.462,0.092,2.156], cond='輸入 ≤32K・輸出 >0.2K')
T(Z,'GLM-4.7','',      [0.616,0.123,2.464],'tencent-intl', intl=[0.616,0.123,2.464], cond='輸入 >32K')

# ============================================================ Kimi
K='moonshot'
T(K,'Kimi K3','',                  [3.0,0.30,15.0],'tencent-sg', sg=[3.0,0.30,15.0], gz=[2.731,0.2731,13.653], intl=[3.0,0.30,15.0])
T(K,'Kimi K2.7 Code HighSpeed','', [1.9,0.38,8.0],'tencent-sg', sg=[1.9,0.38,8.0], gz=[1.9,0.38,8.0], intl=[1.9,0.38,8.0])
T(K,'Kimi K2.7 Code','',           [0.95,0.19,4.0],'tencent-sg', sg=[0.95,0.19,4.0], gz=[0.95,0.19,4.0], intl=[0.95,0.19,4.0])
T(K,'Kimi K2.6','',                [0.858,0.145,3.566],'tencent-sg', sg=[0.858,0.145,3.566], gz=[0.858,0.145,3.566], intl=[1.001,0.169,4.158])
T(K,'Kimi K2.5','',                [0.6,0.10,3.0],'tencent-sg', sg=[0.6,0.10,3.0], gz=[0.56,0.098,2.94], intl=[0.616,0.108,3.234])

# ============================================================ DeepSeek
D='deepseek'
T(D,'DeepSeek-V4-Pro','原廠直供',  [0.66,0.022,1.98],'tencent-sg', sg=[0.66,0.022,1.98], gz=[0.66,0.022,1.98], intl=[0.66,0.022,1.98], peak='off', cond='空閒時段')
T(D,'DeepSeek-V4-Pro','原廠直供',  [1.32,0.044,3.96],'tencent-sg', sg=[1.32,0.044,3.96], gz=[1.32,0.044,3.96], intl=[1.32,0.044,3.96], peak='peak', cond='高峰時段（京 9-12、14-18）')
T(D,'DeepSeek-V4-Flash','原廠直供',[0.22,0.007,0.66],'tencent-sg', sg=[0.22,0.007,0.66], gz=[0.22,0.007,0.66], intl=[0.22,0.007,0.66], peak='off', cond='空閒時段')
T(D,'DeepSeek-V4-Flash','原廠直供',[0.44,0.014,1.32],'tencent-sg', sg=[0.44,0.014,1.32], gz=[0.44,0.014,1.32], intl=[0.44,0.014,1.32], peak='peak', cond='高峰時段（京 9-12、14-18）')
T(D,'DeepSeek-V4-Flash-Vision-Exp','原廠直供',[0.22,0.007,0.66],'tencent-sg', sg=[0.22,0.007,0.66], gz=[0.22,0.007,0.66], peak='off', cond='空閒時段')
T(D,'DeepSeek-V4-Flash-Vision-Exp','原廠直供',[0.44,0.014,1.32],'tencent-sg', sg=[0.44,0.014,1.32], gz=[0.44,0.014,1.32], peak='peak', cond='高峰時段')
T(D,'DeepSeek-V4-Pro','聚合',      [1.74,0.145,3.48],'tencent-sg', sg=[1.74,0.145,3.48], gz=[1.74,0.145,3.48], cond='非原廠直供渠道')
T(D,'DeepSeek-V4-Flash','聚合',    [0.14,0.028,0.28],'tencent-sg', sg=[0.14,0.028,0.28], gz=[0.14,0.028,0.28], cond='非原廠直供渠道')
T(D,'DeepSeek-V4-Pro','8.18 前價', [0.462,0.004,0.923],'tencent-intl', intl=[0.462,0.004,0.923])
T(D,'DeepSeek-V4-Flash','8.18 前價',[0.154,0.003,0.308],'tencent-intl', intl=[0.154,0.003,0.308])
T(D,'DeepSeek-V3.2','',            [0.28,0.056,0.42],'tencent-gz', sg=[0.57,0.114,1.71], gz=[0.28,0.056,0.42], intl=[0.28,0.028,0.42],
  note='新加坡區貴 2 倍，注意選區')

# ============================================================ MiniMax
M='minimax'
T(M,'MiniMax-M3','', [0.3,0.06,1.2],'tencent-sg', sg=[0.3,0.06,1.2], gz=[0.3,0.06,1.2], cond='輸入 ≤512K')
T(M,'MiniMax-M3','', [0.6,0.12,2.4],'tencent-sg', sg=[0.6,0.12,2.4], gz=[0.6,0.12,2.4], cond='輸入 >512K')
T(M,'MiniMax-M2.7','',[0.3,0.06,1.2],'tencent-sg', sg=[0.3,0.06,1.2], gz=[0.3,0.06,1.2], intl=[0.3,0.06,1.2])
T(M,'MiniMax-M2.5','',[0.3,0.03,1.2],'tencent-sg', sg=[0.3,0.03,1.2], gz=[0.3,0.03,1.2], intl=[0.3,0.03,1.2])

# ============================================================ 騰訊混元
H='tencent'
T(H,'Hunyuan 4-preview','', [0.834,0.042,2.501],'tencent-sg', sg=[0.834,0.042,2.501], gz=[0.834,0.042,2.501], intl=[0.834,0.042,2.501])
T(H,'Hunyuan 3.0','',       [0.132,0.033,0.528],'tencent-sg', sg=[0.132,0.033,0.528], gz=[0.132,0.033,0.528], intl=[0.132,0.033,0.528])
T(H,'Hy-MT2-Pro','翻譯',     [0.074,None,0.295],'tencent-sg', sg=[0.074,None,0.295], gz=[0.074,None,0.295])
T(H,'Hy-MT2-Plus','翻譯',    [0.074,None,0.295],'tencent-sg', sg=[0.074,None,0.295], gz=[0.074,None,0.295])
T(H,'Hy-MT2-Lite','翻譯',    [0.044,None,0.177],'tencent-sg', sg=[0.044,None,0.177], gz=[0.044,None,0.177])
T(H,'MiMo-V2.5-Pro','小米',  [0.435,0.0036,0.87],'tencent-sg', sg=[0.435,0.0036,0.87], gz=[0.41,0.003,0.819])

# ============================================================ 階躍星辰（僅騰訊國際站）
S='stepfun'
for n,pr,c in [('Step evolving',[1.0,0.2,5.0],'輸入長度 [0,1024]'),
               ('Step 2.1-pro',[1.0,0.2,5.0],''),
               ('Step 2.1-turbo',[0.5,0.1,2.5],''),
               ('Step character',[0.123,0.025,0.308],'輸入長度 [0,32]'),
               ('Step character',[0.185,0.025,0.923],'輸入長度 (32,128]'),
               ('Step 2.0-mini',[0.10,0.02,0.40],'輸入 [0,32]・非音訊'),
               ('Step 2.0-mini',[0.10,0.02,0.40],'輸入 (32,128]・非音訊'),
               ('Step 2.0-mini',[0.20,0.04,0.80],'輸入 (128,256]・非音訊')]:
    T(S,n,'',pr,'tencent-intl',intl=pr,cond=c,note='悅智報價單無此廠')

# 註：騰訊向量模型（Kinfra-Text/VL-Embedding，$0.07-0.252/M token）唔屬於 text->text，冇收入本表。

# ================================================================= T2I
img = []
def I(vendor, model, variant, intl=None, tclm=None, official=None, ob=None, note=None, cond=None):
    """intl / tclm / official 格式：{res: usd_per_image}"""
    img.append(dict(kind='t2i', vendor=vendor, model=model, variant=variant or '', cond=cond or '',
                    note=note or '', p=dict(official=official, tcINTL=intl, tcLLM=tclm), officialBase=ob))

# Google 官方（Gemini Developer API 定價.md）
I('google','Gemini 3 Pro Image (Nano Banana Pro)','', official={'1K':0.134,'2K':0.134,'4K':0.24}, ob='google-doc',
  intl={'1K':0.1350,'2K':0.1350,'4K':0.2400}, note='騰訊叫 GG 3.0')
I('google','Gemini 3.1 Flash Image (Nano Banana 2)','', official={'512':0.045,'1K':0.067,'2K':0.101,'4K':0.151}, ob='google-doc',
  intl={'512':0.0450,'1K':0.0670,'2K':0.1010,'4K':0.1510}, note='騰訊叫 GG 3.1')
I('google','Gemini 3.1 Flash Lite Image (Nano Banana 2 Lite)','', official={'1K':0.0336}, ob='google-doc',
  intl={'1K':0.0336,'2K':0.0403,'4K':0.0484}, note='騰訊叫 GG 3.1-lite；2K/4K 為騰訊超分直出價')
I('google','Gemini 2.5 Flash Image (Nano Banana)','', official={'1K':0.039}, ob='google-doc',
  intl={'1K':0.0390,'2K':0.0510,'4K':0.0630}, note='騰訊叫 GG 2.5；2K/4K 暫按 1K 收取')
# OpenAI
I('openai','GPT image-2 (low)','', intl={'1K':0.0060,'2K':0.0120,'4K':0.0200}, ob='tencent-intl',
  official={'1K':0.0060,'2K':0.0120,'4K':0.0200}, cond='2026-05-12 起新價')
I('openai','GPT image-2 (medium)','', intl={'1K':0.0530,'2K':0.1070,'4K':0.1780}, ob='tencent-intl',
  official={'1K':0.0530,'2K':0.1070,'4K':0.1780}, cond='2026-05-12 起新價')
I('openai','GPT image-2 (high)','', intl={'1K':0.2110,'2K':0.4280,'4K':0.7120}, ob='tencent-intl',
  official={'1K':0.2110,'2K':0.4280,'4K':0.7120}, cond='2026-05-12 起新價')
# 字節 Seedream
I('seedream','Seedream 5.0-pro','', intl={'1K':0.0450,'2K':0.0900,'4K':0.1080}, ob='tencent-intl',
  official={'1K':0.0450,'2K':0.0900,'4K':0.1080},
  tclm={'1K':0.045,'2K':0.045,'4K':0.09}, cond='輸出圖；首張輸入圖免費，第 2 張起 $0.003；騰訊混元平台按像素分檔（≤261萬 / >261萬）')
I('seedream','Seedream 5.0-lite','', intl={'1K':0.0339,'2K':0.0339,'4K':0.0339}, ob='tencent-intl',
  official={'1K':0.0339,'2K':0.0339,'4K':0.0339}, tclm={'1K':0.035,'2K':0.035,'4K':0.035})
I('seedream','Seedream 4.5','', intl={'1K':0.0385,'2K':0.0385,'4K':0.0385}, ob='tencent-intl', official={'1K':0.0385,'2K':0.0385,'4K':0.0385})
I('seedream','Seedream 4.0','', intl={'1K':0.0308,'2K':0.0308,'4K':0.0308}, ob='tencent-intl', official={'1K':0.0308,'2K':0.0308,'4K':0.0308})
# 可靈
I('kling','Kling 3.0','', intl={'1K':0.0280,'2K':0.0280,'4K':0.0560}, ob='tencent-intl', official={'1K':0.0280,'2K':0.0280,'4K':0.0560})
I('kling','Kling 3.0-omni','', intl={'1K':0.0280,'2K':0.0280,'4K':0.0560}, ob='tencent-intl', official={'1K':0.0280,'2K':0.0280,'4K':0.0560})
I('kling','Kling O1','', intl={'1K':0.0280,'2K':0.0280,'4K':0.0560}, ob='tencent-intl', official={'1K':0.0280,'2K':0.0280,'4K':0.0560})
I('kling','Kling 2.1 文生圖','', intl={'1K':0.0140,'2K':0.0140,'4K':0.0370}, ob='tencent-intl', official={'1K':0.0140,'2K':0.0140,'4K':0.0370})
I('kling','Kling 2.1 單圖生圖','', intl={'1K':0.0280,'2K':0.0280,'4K':0.0560}, ob='tencent-intl', official={'1K':0.0280,'2K':0.0280,'4K':0.0560})
I('kling','Kling 2.1 多圖參考生圖','', intl={'1K':0.0560,'2K':0.0680,'4K':0.0790}, ob='tencent-intl', official={'1K':0.0560,'2K':0.0680,'4K':0.0790})
I('kling','Kling expand 擴圖','', intl={'1K':0.0280,'2K':0.0280,'4K':0.0280}, ob='tencent-intl', official={'1K':0.0280,'2K':0.0280,'4K':0.0280})
# Vidu
I('vidu','Vidu q2 文生圖','', intl={'1K':0.0288,'2K':0.0385,'4K':0.0481}, ob='tencent-intl', official={'1K':0.0288,'2K':0.0385,'4K':0.0481},
  tclm={'1K':0.03,'2K':0.04,'4K':0.05})
I('vidu','Vidu q2 參考生圖 1-3 張','', intl={'1K':0.0385,'2K':0.0577,'4K':0.0769}, ob='tencent-intl', official={'1K':0.0385,'2K':0.0577,'4K':0.0769},
  tclm={'1K':0.04,'2K':0.06,'4K':0.10})
I('vidu','Vidu q2 參考生圖 4-7 張','', intl={'1K':0.0481,'2K':0.0962,'4K':0.1442}, ob='tencent-intl', official={'1K':0.0481,'2K':0.0962,'4K':0.1442},
  tclm={'1K':0.05,'2K':0.08,'4K':0.15})
# 騰訊混元 / 其他
I('tencent','Hunyuan Image 3.0','', intl=None, tclm={'1K':0.032,'2K':0.032,'4K':0.032}, ob='tencent-llm',
  official={'1K':0.032,'2K':0.032,'4K':0.032}, note='騰訊 VOD 國際站未上架，只有國內站 0.2-0.36 元/張')
I('qwen','Qwen Image 0925','', intl={'1K':0.0462,'2K':0.0585,'4K':0.0708}, ob='tencent-intl', official={'1K':0.0462,'2K':0.0585,'4K':0.0708})
I('bytedance','即夢 JI 4.0','', intl={'1K':0.0339,'2K':0.0339,'4K':0.0339}, ob='tencent-intl', official={'1K':0.0339,'2K':0.0339,'4K':0.0339})
I('midjourney','Midjourney v8.2','', intl={'1K':0.0390,'2K':0.0510,'4K':0.0630}, ob='tencent-intl', official={'1K':0.0390,'2K':0.0510,'4K':0.0630}, note='預設出 4 張圖')
I('midjourney','Midjourney v7','', intl={'1K':0.0390,'2K':0.0510,'4K':0.0630}, ob='tencent-intl', official={'1K':0.0390,'2K':0.0510,'4K':0.0630}, note='預設出 4 張圖')
I('other','Vega 1.0-lite','', intl={'1K':0.0259,'2K':0.0288,'4K':0.0360}, ob='tencent-intl', official={'1K':0.0259,'2K':0.0288,'4K':0.0360})
I('other','Vega 1.0-flash','', intl={'1K':0.0603,'2K':0.0909,'4K':0.1359}, ob='tencent-intl', official={'1K':0.0603,'2K':0.0909,'4K':0.1359})
I('other','Vega 1.0-pro','', intl={'1K':0.1282,'2K':0.1282,'4K':0.2280}, ob='tencent-intl', official={'1K':0.1282,'2K':0.1282,'4K':0.2280}, note='前 3 張輸入圖免費，第 4 張起 $0.0154')
I('other','Mingmou 1.0','', intl={'1K':0.0462,'2K':0.0585,'4K':0.0708}, ob='tencent-intl', official={'1K':0.0462,'2K':0.0585,'4K':0.0708})

# ================================================================= T2V
vid=[]
def V(vendor, model, variant, intl=None, tclm=None, official=None, ob=None, note=None, cond=None):
    vid.append(dict(kind='t2v', vendor=vendor, model=model, variant=variant or '', cond=cond or '',
                    note=note or '', p=dict(official=official, tcINTL=intl, tcLLM=tclm), officialBase=ob))
R5,R7,R10,R2K,R4K='480P/540P','720P/768P','1080P','2K','4K'
# Google Veo（官方 = Gemini 定價頁；騰訊 GV）
V('google','Veo 3.1 標準（有聲）','', official={R7:0.40,R10:0.40,R4K:0.60}, ob='google-doc',
  intl={R7:0.4000,R10:0.5000,R2K:0.5000,R4K:0.6000}, cond='有聲')
V('google','Veo 3.1 標準（無聲）','', intl={R7:0.2000,R10:0.3000,R2K:0.3000,R4K:0.4000}, ob='tencent-intl',
  official={R7:0.2000,R10:0.3000,R4K:0.4000}, cond='無聲')
V('google','Veo 3.1 Fast（有聲）','', official={R7:0.10,R10:0.12,R4K:0.30}, ob='google-doc',
  intl={R7:0.1500,R10:0.2500,R2K:0.2500,R4K:0.3500}, cond='有聲')
V('google','Veo 3.1 Fast（無聲）','', intl={R7:0.1000,R10:0.2000,R2K:0.2000,R4K:0.3000}, ob='tencent-intl',
  official={R7:0.1000,R10:0.2000,R4K:0.3000}, cond='無聲')
V('google','Veo 3.1 Lite（有聲）','', official={R7:0.05,R10:0.08}, ob='google-doc',
  intl={R7:0.0800,R10:0.1200,R2K:0.1500}, cond='有聲')
V('google','Veo 3.1 Lite（無聲）','', intl={R7:0.0500,R10:0.0800,R2K:0.1000}, ob='tencent-intl',
  official={R7:0.0500,R10:0.0800}, cond='無聲')
# OpenAI Sora
V('openai','Sora 2.0 (OS)','', intl={R7:0.1000,R10:0.1500,R2K:0.2250,R4K:0.3400}, ob='tencent-intl',
  official={R7:0.1000,R10:0.1500,R2K:0.2250,R4K:0.3400})
# 可靈
V('kling','Kling 3.0-turbo','', intl={R7:0.1120,R10:0.1400,R2K:0.1680,R4K:0.2016}, ob='tencent-intl',
  official={R7:0.1120,R10:0.1400,R2K:0.1680,R4K:0.2016}, tclm={R7:0.112,R10:0.14}, cond='有聲')
V('kling','Kling 3.0-Omni 無參考影片・無聲','', intl={R7:0.0840,R10:0.1120,R2K:0.1400,R4K:0.4200}, ob='tencent-intl',
  official={R7:0.0840,R10:0.1120,R2K:0.1400,R4K:0.4200}, tclm={R7:0.084,R10:0.112,R4K:0.42})
V('kling','Kling 3.0-Omni 無參考影片・有聲','', intl={R7:0.1120,R10:0.1400,R2K:0.1680,R4K:0.4200}, ob='tencent-intl',
  official={R7:0.1120,R10:0.1400,R2K:0.1680,R4K:0.4200}, tclm={R7:0.112,R10:0.14,R4K:0.42})
V('kling','Kling 3.0-Omni 有參考影片・無聲','', intl={R7:0.1260,R10:0.1680,R2K:0.2100,R4K:0.2800}, ob='tencent-intl',
  official={R7:0.1260,R10:0.1680,R2K:0.2100,R4K:0.2800}, tclm={R7:0.126,R10:0.168,R4K:0.42})
V('kling','Kling 3.0 無聲','', intl={R7:0.0840,R10:0.1120,R2K:0.1400,R4K:0.4200}, ob='tencent-intl',
  official={R7:0.0840,R10:0.1120,R2K:0.1400,R4K:0.4200}, tclm={R7:0.084,R10:0.112,R4K:0.42})
V('kling','Kling 3.0 有聲・未指定音色','', intl={R7:0.1260,R10:0.1680,R2K:0.2100,R4K:0.4200}, ob='tencent-intl',
  official={R7:0.1260,R10:0.1680,R2K:0.2100,R4K:0.4200}, tclm={R7:0.126,R10:0.168,R4K:0.42})
V('kling','Kling O1 無參考影片','', intl={R7:0.0840,R10:0.1120,R2K:0.1680,R4K:0.2520}, ob='tencent-intl',
  official={R7:0.0840,R10:0.1120,R2K:0.1680,R4K:0.2520})
V('kling','Kling O1 有參考影片','', intl={R7:0.1260,R10:0.1680,R2K:0.2520,R4K:0.3780}, ob='tencent-intl',
  official={R7:0.1260,R10:0.1680,R2K:0.2520,R4K:0.3780})
V('kling','Kling 2.6 無聲','', intl={R7:0.0420,R10:0.0700,R2K:0.1050,R4K:0.1568}, ob='tencent-intl',
  official={R7:0.0420,R10:0.0700,R2K:0.1050,R4K:0.1568})
V('kling','Kling 2.6 有聲','', intl={R10:0.1400,R2K:0.2100,R4K:0.3150}, ob='tencent-intl',
  official={R10:0.1400,R2K:0.2100,R4K:0.3150})
V('kling','Kling 2.5-turbo','', intl={R7:0.0420,R10:0.0700,R2K:0.1050,R4K:0.1570}, ob='tencent-intl',
  official={R7:0.0420,R10:0.0700,R2K:0.1050,R4K:0.1570})
V('kling','Kling 1.6 / 2.0 / 2.1','', intl={R7:0.0560,R10:0.0980,R2K:0.1400,R4K:0.2100}, ob='tencent-intl',
  official={R7:0.0560,R10:0.0980,R2K:0.1400,R4K:0.2100})
# 海螺 / MiniMax
V('hailuo','Hailuo H3 輸出影片','', intl={R7:0.0800,R10:0.1000,R2K:0.1300,R4K:0.1560}, ob='tencent-intl',
  official={R7:0.0800,R10:0.1000,R2K:0.1300,R4K:0.1560}, tclm={R7:0.08,R2K:0.13}, note='騰訊混元平台以 768P/2K 計')
V('hailuo','Hailuo H3-Max','', intl={R5:0.0500,R7:0.0800,R10:0.1000,R2K:0.1200,R4K:0.1440}, ob='tencent-intl',
  official={R5:0.0500,R7:0.0800,R10:0.1000,R2K:0.1200,R4K:0.1440})
V('hailuo','Hailuo 02 / 2.3','', intl={R7:0.0508,R10:0.0892,R2K:0.1431,R4K:0.2292}, ob='tencent-intl',
  official={R7:0.0508,R10:0.0892,R2K:0.1431,R4K:0.2292})
V('hailuo','Hailuo 2.3-fast','', intl={R7:0.0346,R10:0.0592,R2K:0.0892,R4K:0.1338}, ob='tencent-intl',
  official={R7:0.0346,R10:0.0592,R2K:0.0892,R4K:0.1338})
# Vidu
V('vidu','Vidu q3 參考生','', intl={R5:0.0500,R7:0.1000,R10:0.1250,R2K:0.1500,R4K:0.1800}, ob='tencent-intl',
  official={R5:0.0500,R7:0.1000,R10:0.1250,R2K:0.1500,R4K:0.1800})
V('vidu','Vidu q3 參考生＋錯峰','', intl={R5:0.0250,R7:0.0500,R10:0.0630,R2K:0.0750,R4K:0.0900}, ob='tencent-intl',
  official={R5:0.0250,R7:0.0500,R10:0.0630,R2K:0.0750,R4K:0.0900}, cond='錯峰模式，價格減半')
V('vidu','Vidu q3-pro 圖生/文生/首尾幀','', intl={R5:0.0500,R7:0.1250,R10:0.1500,R2K:0.1800,R4K:0.2160}, ob='tencent-intl',
  official={R5:0.0500,R7:0.1250,R10:0.1500,R2K:0.1800,R4K:0.2160})
V('vidu','Vidu q3-turbo 圖生/文生/首尾幀','', intl={R5:0.0400,R7:0.0600,R10:0.0700,R2K:0.0840,R4K:0.1008}, ob='tencent-intl',
  official={R5:0.0400,R7:0.0600,R10:0.0700,R2K:0.0840,R4K:0.1008})
V('vidu','Vidu q3-turbo ＋錯峰','', intl={R5:0.0200,R7:0.0300,R10:0.0350,R2K:0.0420,R4K:0.0504}, ob='tencent-intl',
  official={R5:0.0200,R7:0.0300,R10:0.0350,R2K:0.0420,R4K:0.0504}, cond='錯峰模式')
V('vidu','Vidu q3-drama 參考生','', intl={R10:0.1400,R2K:0.1680,R4K:0.2015}, ob='tencent-intl',
  official={R10:0.1400,R2K:0.1680,R4K:0.2015})
V('vidu','Vidu q3-mix 參考生','', intl={R7:0.1250,R10:0.1500,R2K:0.1800,R4K:0.2160}, ob='tencent-intl',
  official={R7:0.1250,R10:0.1500,R2K:0.1800,R4K:0.2160})
V('vidu','Vidu q2 文生','', intl={R7:0.0492,R10:0.0723,R2K:0.1077,R4K:0.1615}, ob='tencent-intl',
  official={R7:0.0492,R10:0.0723,R2K:0.1077,R4K:0.1615})
V('vidu','Vidu q2 文生＋錯峰','', intl={R7:0.0246,R10:0.0362,R2K:0.0538,R4K:0.0808}, ob='tencent-intl',
  official={R7:0.0246,R10:0.0362,R2K:0.0538,R4K:0.0808}, cond='錯峰模式')
V('vidu','Vidu q2-pro 圖生/首尾幀','', intl={R7:0.0538,R10:0.1077,R2K:0.1538,R4K:0.2308}, ob='tencent-intl',
  official={R7:0.0538,R10:0.1077,R2K:0.1538,R4K:0.2308})
V('vidu','Vidu q2-turbo 圖生/首尾幀','', intl={R7:0.0385,R10:0.0723,R2K:0.1077,R4K:0.1615}, ob='tencent-intl',
  official={R7:0.0385,R10:0.0723,R2K:0.1077,R4K:0.1615})
# PixVerse
V('pixverse','PixVerse V6.0 無聲','', intl={R5:0.0311,R7:0.0400,R10:0.0800,R2K:0.0960,R4K:0.1152}, ob='tencent-intl',
  official={R5:0.0311,R7:0.0400,R10:0.0800,R2K:0.0960,R4K:0.1152}, tclm={R5:0.03111,R7:0.04,R10:0.08})
V('pixverse','PixVerse V6.0 有聲','', intl={R5:0.0400,R7:0.0533,R10:0.1022,R2K:0.1227,R4K:0.1472}, ob='tencent-intl',
  official={R5:0.0400,R7:0.0533,R10:0.1022,R2K:0.1227,R4K:0.1472}, tclm={R5:0.04,R7:0.05333,R10:0.10222})
V('pixverse','PixVerse C1 無聲','', intl={R5:0.0356,R7:0.0444,R10:0.0844,R2K:0.1013,R4K:0.1216}, ob='tencent-intl',
  official={R5:0.0356,R7:0.0444,R10:0.0844,R2K:0.1013,R4K:0.1216}, tclm={R5:0.03556,R7:0.04444,R10:0.08444})
V('pixverse','PixVerse C1 有聲','', intl={R5:0.0444,R7:0.0578,R10:0.1067,R2K:0.1280,R4K:0.1536}, ob='tencent-intl',
  official={R5:0.0444,R7:0.0578,R10:0.1067,R2K:0.1280,R4K:0.1536}, tclm={R5:0.04444,R7:0.05778,R10:0.10667})
V('pixverse','PixVerse V5.6 無聲','', intl={R5:0.0392,R7:0.0504,R10:0.0840,R2K:0.1176,R4K:0.1646}, ob='tencent-intl',
  official={R5:0.0392,R7:0.0504,R10:0.0840,R2K:0.1176,R4K:0.1646})
# 字節 Seedance (SV)
V('seedance','Seedance 1.5-pro 無聲','', intl={R5:0.0123,R7:0.0265,R10:0.0597,R2K:0.1063,R4K:0.2388}, ob='tencent-intl',
  official={R5:0.0123,R7:0.0265,R10:0.0597,R2K:0.1063,R4K:0.2388})
V('seedance','Seedance 1.5-pro 有聲','', intl={R5:0.0246,R7:0.0532,R10:0.1197,R2K:0.2126,R4K:0.4785}, ob='tencent-intl',
  official={R5:0.0246,R7:0.0532,R10:0.1197,R2K:0.2126,R4K:0.4785})
V('seedance','Seedance 1.0-pro','', intl={R5:0.0225,R7:0.0474,R10:0.1129,R2K:0.1694,R4K:0.2541}, ob='tencent-intl',
  official={R5:0.0225,R7:0.0474,R10:0.1129,R2K:0.1694,R4K:0.2541})
V('seedance','Seedance 1.0-pro-fast','', intl={R5:0.0062,R7:0.0132,R10:0.0317,R2K:0.0475,R4K:0.0713}, ob='tencent-intl',
  official={R5:0.0062,R7:0.0132,R10:0.0317,R2K:0.0475,R4K:0.0713})
V('bytedance','即夢 JV 3.0-pro','', intl={R10:0.1538,R2K:0.2308,R4K:0.3462}, ob='tencent-intl',
  official={R10:0.1538,R2K:0.2308,R4K:0.3462})
# 阿里 Wan
V('alibaba','Wan 3.0','', intl={R5:0.0500,R7:0.1000,R10:0.2000,R2K:0.2400,R4K:0.2880}, ob='tencent-intl',
  official={R5:0.0500,R7:0.1000,R10:0.2000,R2K:0.2400,R4K:0.2880})
V('alibaba','Wan 3.0-prime','', intl={R5:0.0680,R7:0.1400,R10:0.2800,R2K:0.3360,R4K:0.4032}, ob='tencent-intl',
  official={R5:0.0680,R7:0.1400,R10:0.2800,R2K:0.3360,R4K:0.4032})
# 騰訊混元
V('tencent','Hunyuan Video 1.5','', tclm={R7:0.048}, ob='tencent-llm', official={R7:0.048},
  note='騰訊 VOD 國際站未上架（只有國內站 0.3-1.12 元/秒）')
V('other','Vega 1.0-lite 輸出影片','', intl={R7:0.0577,R10:0.0769,R2K:0.0962,R4K:0.1154}, ob='tencent-intl',
  official={R7:0.0577,R10:0.0769,R2K:0.0962,R4K:0.1154})
V('other','Vega 1.0-pro 無參考影片','', intl={R7:0.1223,R10:0.2662,R2K:0.6615,R4K:0.7538}, ob='tencent-intl',
  official={R7:0.1223,R10:0.2662,R2K:0.6615,R4K:0.7538})
V('other','Mingmou 1.0','', intl={R7:0.0462,R10:0.0769,R2K:0.1154,R4K:0.1723}, ob='tencent-intl',
  official={R7:0.0462,R10:0.0769,R2K:0.1154,R4K:0.1723})
V('minimax','MiniMax-Video-H3','', tclm={R7:0.08,R2K:0.13}, ob='tencent-llm', official={R7:0.08,R2K:0.13},
  cond='768P / 2K；輸入影片同價', note='騰訊混元平台報價')

# ---------------------------------------------------------------- 組裝
def yz_for(vendor, model):
    key = '%s:%s' % (vendor, model)
    if key in YZ_OVERRIDE: return YZ_OVERRIDE[key]
    for k,v in YZ_OVERRIDE.items():
        if k.startswith(vendor+':') and k.split(':',1)[1] in model: return v
    return YZ_FACTOR.get(vendor)

def _norm(x):
    return x.lower().replace('-',' ').replace('_',' ').replace('  ',' ').strip()
def listed(vendor, model):
    mm = _norm(model)
    for m in YZ_LISTED.get(vendor, []):
        if mm.endswith(_norm(m)): return True
    return False

all_rows = rows + img + vid
for i,r in enumerate(all_rows):
    r['id'] = 'm%03d' % i
    r['vendorLabel'] = VENDOR_LABEL.get(r['vendor'], r['vendor'])
    r['yzFactor'] = yz_for(r['vendor'], r['model'])
    r['yzListed'] = listed(r['vendor'], r['model'])

data = dict(
    generated='2026-09-10',
    fxNote='騰訊國際站人民幣→美元換算比例約 6.49（部分型號逐一定價，非統一匯率）',
    vendors=VENDOR_LABEL,
    yzFactor=YZ_FACTOR,
    rows=all_rows,
)
with open(OUT,'w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=1)
print('rows:',len(all_rows), ' t2t:',len(rows),' t2i:',len(img),' t2v:',len(vid))
