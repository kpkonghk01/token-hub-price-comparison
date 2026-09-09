# Token Hub 比價台

把幾間供應商嘅模型報價擺埋一齊比：**同一隻 model、唔同 provider 顯示喺同一 row**。
涵蓋 text→text、生圖（text→image）、生片（text→video），價格全部換算成美元。

交付物係 **`index.html`** —— 單一自足檔案，雙擊就開得，唔使裝嘢、唔使起 server、唔使上任何平台。

---

## 快速開始

```
雙擊 index.html
```

搞掂。想 send 畀人就直接 send 個檔（email 附件 / IM / USB 都得）。

**離線可唔可以用？** 可以。全部報價數字都 inline 咗喺 HTML 入面。唯一外部依賴係 Google Fonts；斷網嘅話會 fallback 落系統字體，排版同數字一個都唔會走位。

**想出 PDF？** 喺瀏覽器撳 `Cmd/Ctrl + P`。已經寫咗列印樣式：控制項會自動收起、成個表攤開唔會被 sticky 表頭剪走、摺埋咗嘅說明會自動展開。

**Deep link**：`index.html#t2t`、`#t2i`、`#t2v` 可以直接開去指定分頁。

---

## 頁面點睇

由上而下分四段：

| 段落 | 內容 |
|---|---|
| **重點結論** | 五張結論卡 + 「計費方法點拉平」對照表。想畀老細睇嘅嘢喺呢度。 |
| **比價表** | 三個分頁（文本／生圖／生片）+ 篩選控制項 + 四格 KPI。 |
| **點樣比先算公道** | 比較方法、基準價來源、騰訊三個平台嘅分別、未計入嘅費用、縮寫對照。 |
| **頁底** | 資料來源檔案路徑同更新日期。 |

頁首有粒「直接去比價表 ↓」，唔想睇結論可以一撳跳落工具。
右下角有主題掣（自動／淺色／深色）。

### 讀表

- **大隻嗰個數 = 綜合單價**，已經按你設定嘅輸入輸出比例同快取命中率計埋
- 細字係入／出／快取嘅原價
- <u>虛線底</u>嘅數字係**推算價** = 基準價 × 折扣（悅智、現用供應商兩欄）；冇虛線嘅係報價表照抄
- **米黃色格 = 嗰行最平**
- `—` = 嗰個 provider 冇上架呢隻 model，唔會硬砌對照

### 控制項

| 控制項 | 做咩 |
|---|---|
| **搜尋型號** | 搵型號名、原廠、條件、備註 |
| **輸入 : 輸出 比例** | 綜合單價 = `(R × 有效輸入 + 輸出) ÷ (R+1)`，預設 4:1 |
| **快取命中率** | `有效輸入價 = 輸入 ×(1−命中率) + 快取價 × 命中率`；冇公佈快取價嘅型號一律用足全價 |
| **解析度**（生圖／生片） | 生圖揀 1K／2K／4K；生片揀 540P→4K。成個表跟住換 |
| **排序** | 最低價平→貴／貴→平、按原廠、按型號名 |
| **峰谷計費** | 全部顯示／全當高峰／全當空閒。只有 DeepSeek 原廠直供分峰谷 |
| **現用 Gemini 供應商折扣** | 預設 95（收 Google 正價 95%）。改咗之後結論卡同成個表即刻重算 |
| **原廠篩選** | 揀睇邊幾間廠 |
| **顯示欄位** | 開關 provider 欄；另有「只睇 2 個以上報價渠道」 |

### KPI 四格

報價點數 · 平均可省（最平 vs 原廠目錄價）· 騰訊有貨但悅智冇報價嘅數目 · 目前最平嗰個報價。
全部跟住篩選即時重算。

---

## 檔案結構

```
.
├── index.html            ← 交付物。單一自足檔案，唔好直接手改
├── data.json             ← 結構化報價，想倒入 Excel / 第二個系統可以直接用
├── README.md
├── build/
│   ├── build_data.py     ← 所有報價數字嘅唯一出處。改價改呢度
│   ├── template.html     ← 版面、樣式、互動邏輯
│   └── make.py           ← 一鍵重建
└── providers/            ← 原始報價文件（唯讀，唔會被程式改動）
    ├── Gemini Developer API 定價.md
    ├── tencent/
    │   ├── 模型价格.md                        （語言模型平台：新加坡／廣州／矽谷）
    │   ├── 模型单价/*.png                     （VOD AIGC 平台，圖片報價表）
    │   └── 【对外】音视频AIGC大模型功能对比.xlsx  （功能對照，非報價）
    └── yz/悦如Token Hub模型报价单.xlsx        （只有折扣率，冇絕對價）
```

---

## 更新報價

需要 **Python 3**（3.8 以上）。**冇任何第三方套件**，clone 落嚟就跑得。

```bash
python3 build/make.py
```

`make.py` 會自動先跑 `build_data.py` 產生 `data.json`，再同 `template.html` 砌成 `index.html`。

### 改數字

全部報價都寫喺 `build/build_data.py`，按廠商分段。三個 helper：

```python
# 文本：[輸入, 快取輸入, 輸出]，缺值用 None
T(vendor, model, variant, official=[...], ob='來源', sg=[...], gz=[...], intl=[...],
  cond='條件', note='備註', peak='peak'|'off')

# 生圖：{解析度: 每張美元}
I(vendor, model, variant, official={...}, ob='來源', intl={...}, tclm={...})

# 生片：{解析度: 每秒美元}
V(vendor, model, variant, official={...}, ob='來源', intl={...}, tclm={...})
```

| 參數 | 對應欄位 |
|---|---|
| `official` | 原廠官方價（同時係悅智折扣嘅基準） |
| `ob` | 基準價出處，會喺表入面顯示做 badge：`google-doc` / `tencent-intl` / `tencent-sg` / `tencent-gz` / `tencent-llm` |
| `sg` `gz` `intl` | 騰訊·新加坡／廣州／國際站 |
| `tclm` | 騰訊·混元平台（生圖／生片先有） |

解析度 key 要跟返常數：生圖用 `512` `1K` `2K` `4K`；生片用 `R5` `R7` `R10` `R2K` `R4K`（即 `480P/540P` `720P/768P` `1080P` `2K` `4K`）。

### 改悅智折扣

`build_data.py` 頂部：

- `YZ_FACTOR` — 每個原廠嘅折扣率（悅智價 = 原廠基準價 × 呢個數）
- `YZ_OVERRIDE` — 個別型號例外，例如 Kimi K3 冇折
- `YZ_LISTED` — 報價單上明確列出嘅型號。唔喺名單入面嘅會顯示「推算」badge
- `VENDOR_LABEL` — 原廠中文名

### 改版面／文案

改 `build/template.html`，再跑 `make.py`。
入面 `@@PAYLOAD@@` 係資料佔位符，唔好郁。

---

## 資料來源同基準假設

| 來源 | 用嚟做咩 |
|---|---|
| `Gemini Developer API 定價.md` | Google 官方定價（paid tier、standard，非 Batch/Flex/Priority）。唯一一份真·官方文件 |
| `tencent/模型价格.md` | 騰訊雲「語言模型」平台，新加坡／廣州／矽谷三個 region |
| `tencent/模型单价/*.png` | 騰訊雲「VOD AIGC」平台。**呢啲係圖片，已經人手轉錄入 `build_data.py`** |
| `yz/悦如Token Hub模型报价单.xlsx` | 悅智 TokenHub。**只有折扣率，冇絕對價** |

**悅智價點嚟：** 佢份報價單淨係畀折扣率，所以要有個底價先計到。每一行都標明基準價出處：

- **Gemini** → Google 官方定價頁
- **Claude / GPT / Grok** → 騰訊國際站（同原廠美元目錄價一致，核對過：Opus 5 = `$5/$25`、Sonnet 5 = `$3/$15`、Haiku 4.5 = `$1/$5`）
- **GLM / Kimi / MiniMax / 混元** → 騰訊新加坡區（整數美元，最似原廠國際版目錄價）
- **DeepSeek V3.2** → 騰訊廣州區（同 DeepSeek 官方美元價一致）

凡標「**推定**」badge 嘅，即係嗰個基準價唔係直接嚟自原廠文件，而係由騰訊報價推回去。睇趨勢 OK，**落單前要同供應商 double check**。

---

## 未計入（落單前記得問）

- **稅** — 悅智海外模型如用人民幣結算要加 15 個點（8% 非貿付匯稅 + 1% 附加稅 + 6% 增值稅），公式 `美金金額 × 匯率 × 1.15`。用美元結算就唔使。騰訊國際站港澳免稅，其餘國家另計
- **Batch / Flex / Priority** — Google 官方 Batch 平一半。本表一律只計 Standard
- **前置條件** — 悅智全部係預付，用量大 case by case；AWS Bedrock／GCP Vertex／Azure 通路寫「用量申請」。報價有效期 15–30 日
- **工具費** — Google Search grounding（Gemini 3.x 每月 5,000 次免費，之後 `$14/1,000` 次）、Maps grounding、file search 嘅 embedding 費
- **限時優惠** — GLM-5.3-Flash 至 2026-09-10 半價；OpenAI 5.6-sol 限時優惠；Gemini 3.6/3.7/3.8 Flash 2027-01-01 起加價一倍（兩個價都列咗）
- **按次雜費** — 可靈人臉識別、Vidu 主體識別／聲音複刻、Claude Web 搜索等
- **向量模型** — 唔屬於 text→text，冇收入本表（Gemini Embedding `$0.15`／騰訊 Kinfra `$0.07–0.252`）

---

## 縮寫對照

騰訊報價表用咗一堆縮寫，程式已經全部還原成正名：

| 縮寫 | 正名 |
|---|---|
| GG | Google Gemini（nano 2.5／3.0／3.1 = Nano Banana 系列） |
| GV | Google Veo |
| CD | Anthropic Claude |
| OG | OpenAI GPT（image-2 = GPT Image 2） |
| OS | OpenAI Sora |
| GK | xAI Grok |
| SI／SV | 字節 Seedream（圖）／Seedance（片） |
| JI／JV | 字節即夢 Jimeng（圖／片） |
| H2／H3 | MiniMax 海螺 Hailuo |
| ST | 階躍星辰 StepFun |
| Hy／Hunyuan | 騰訊混元 |
| MJ | Midjourney |
| Wan | 阿里通義萬相 |

---

## 注意

騰訊報價表最後更新 **2026-09-04**，本表資料截至 **2026-09-10**。
價格會變，**落單前請以供應商正式報價為準**。
