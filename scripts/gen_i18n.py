#!/usr/bin/env python3
"""Generate zh/ja/ko translations of index.html from the English root.

Run from repo root: python3 scripts/gen_i18n.py
The English root index.html is the source of truth.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

EN = {
    "title": "tautiu — a tiny indie app studio",
    "meta_desc": "tautiu (透抽) is Taiwanese for squid. One little squid, ten busy arms — indie Mac & iPhone apps: DeepSRT, DeepSRT Transcribe, Foldic, Recilic, Ripplic, Raidic, Mergic, Nookic, Lossic, OpenAB Connect, OpenAB Remote.",
    "og_title": "tautiu — a tiny indie app studio",
    "og_desc": "One little squid, ten busy arms. Indie Mac & iPhone apps made with care.",
    "tagline": "a tiny indie app studio",
    "story": """<span class="zh">tautiu（透抽）</span> is Taiwanese for squid —
    one little squid, ten busy arms, building apps
    for your Mac and iPhone.""",
    "deepsrt": "Instant AI summaries and clean, clickable transcripts for any YouTube video — natively on your Mac.",
    "deepsrt_transcribe": "Fully offline transcription with Apple's on-device speech models — then refined by Gemini and auto-corrected with Google Search grounding.",
    "foldic": "Your Photos albums, mirrored to real folders — automatically on your Mac, or straight onto a USB-C drive from your iPhone.",
    "recilic": "Your private backup mesh — weave the Macs and drives you already own into one end-to-end encrypted backup pool.",
    "ripplic": "One-way sync from your folders to your own cloud storage — S3, R2, GCS, B2, and any S3-compatible destination.",
    "raidic": "A native Mac control panel for AppleRAID — create, monitor, repair, and manage mirror, stripe, and concatenated disk sets without Terminal.",
    "mergic": "Merge one folder into another safely, with MD5-verified conflict handling. Never lose a file again.",
    "nookic": "Your own nook for what you've already seen — keep posts exactly the way you saw them, on your own iPhone.",
    "lossic": "The lossless player for your Google Drive — instant, private playback, plus AI stories about the performer and piece, suggested questions, and follow-up chat with your own key.",
    "openab_connect": "A native Mac command center for persistent coding-agent terminals — connect, split panes, dictate, and manage remote sessions in one place.",
    "openab_remote": "Push to talk on your iPhone; speech stays on-device, and only terminal-safe text reaches OpenAB Connect on your Mac.",
    "ribbon": "coming soon",
    "ribbon_internal": "internal only",
    "footer": '<span class="squid">🦑</span> made by one small squid · © 2026 tautiu · <a href="privacy/">privacy</a> · <a href="mailto:tautiu.dev@gmail.com">contact us</a>',
}

LANGS = {
    "zh": {
        "html_lang": "zh-Hant",
        "title": "tautiu — 小小的獨立 App 工作室",
        "meta_desc": "tautiu（透抽）是台語的魷魚。一隻小透抽、十隻忙碌的觸手 — 獨立開發的 Mac 與 iPhone App：DeepSRT、DeepSRT Transcribe、Foldic、Recilic、Ripplic、Raidic、Mergic、Nookic、Lossic、OpenAB Connect、OpenAB Remote。",
        "og_title": "tautiu — 小小的獨立 App 工作室",
        "og_desc": "一隻小透抽、十隻忙碌的觸手。用心打造的獨立 Mac 與 iPhone App。",
        "tagline": "小小的獨立 App 工作室",
        "story": """<span class="zh">tautiu（透抽）</span>是台語的魷魚 —
    一隻小透抽、十隻忙碌的觸手，
    忙著為你的 Mac 和 iPhone 打造 App。""",
        "deepsrt": "任何 YouTube 影片，立即生成 AI 摘要與乾淨可點擊的逐字稿 — 原生 Mac 體驗。",
        "deepsrt_transcribe": "Apple 語音模型完全本地運算，影像聲音全部離線處理 — 再由最強 Gemini 模型優化語言，Grounding with Google Search 自動校正。",
        "foldic": "把你的「照片」相簿鏡像成真實資料夾 — 在 Mac 上自動執行，或直接從 iPhone 存進 USB-C 隨身碟。",
        "recilic": "你的私有備份網 — 把手邊的 Mac 和硬碟編織成一個端到端加密的備份池。",
        "ripplic": "從資料夾單向同步到你自己的雲端儲存 — S3、R2、GCS、B2 以及任何 S3 相容服務。",
        "raidic": "原生 Mac AppleRAID 管理工具 — 不用終端機，就能建立、監控、修復與管理鏡像、分散及串接磁碟陣列。",
        "mergic": "安全地把一個資料夾合併進另一個，MD5 驗證的衝突處理。再也不弄丟檔案。",
        "nookic": "為你看過的內容留一個小角落 — 把貼文以你看到的樣子，留存在你自己的 iPhone。",
        "lossic": "Google Drive 裡的無損音樂，一點即播；右滑就有 AI 演出者與樂曲介紹、推薦問題，還能用自己的 AI Key 繼續聊。唯讀直連，不經 Lossic 後端。",
        "openab_connect": "原生 Mac coding agent 終端控制中心 — 連線、分割窗格、語音輸入，並在一處管理持久化的遠端工作階段。",
        "openab_remote": "在 iPhone 按住說話；語音只在本機轉成文字，只有終端安全文字會送到 Mac 上的 OpenAB Connect。",
        "ribbon": "即將推出",
        "ribbon_internal": "內部限定",
        "footer": '<span class="squid">🦑</span> 一隻小透抽做的 · © 2026 tautiu · <a href="../privacy/">隱私權政策</a> · <a href="mailto:tautiu.dev@gmail.com">聯絡我們</a>',
    },
    "ja": {
        "html_lang": "ja",
        "title": "tautiu — 小さなインディーアプリスタジオ",
        "meta_desc": "tautiu（透抽）は台湾語でイカのこと。小さなイカと十本の忙しい腕 — Mac と iPhone のためのインディーアプリ：DeepSRT、DeepSRT Transcribe、Foldic、Recilic、Ripplic、Raidic、Mergic、Nookic、Lossic、OpenAB Connect、OpenAB Remote。",
        "og_title": "tautiu — 小さなインディーアプリスタジオ",
        "og_desc": "小さなイカと十本の忙しい腕。心を込めてつくった Mac と iPhone のアプリ。",
        "tagline": "小さなインディーアプリスタジオ",
        "story": """<span class="zh">tautiu（透抽）</span>は台湾語でイカのこと —
    小さなイカが十本の忙しい腕で、
    Mac と iPhone のためのアプリをつくっています。""",
        "deepsrt": "どんな YouTube 動画も、AI 要約とクリックできる文字起こしに — Mac ネイティブで。",
        "deepsrt_transcribe": "Apple の音声モデルで完全オンデバイス処理、映像も音声もすべてオフライン。さらに最強の Gemini が言語を最適化し、Google 検索グラウンディングで自動補正。",
        "foldic": "「写真」のアルバムをそのままフォルダへミラーリング — Mac では自動的に、iPhone からは USB-C ドライブへ直接。",
        "recilic": "あなただけのプライベートバックアップメッシュ — 手元の Mac とドライブを、エンドツーエンド暗号化のバックアッププールに。",
        "ripplic": "フォルダから自分のクラウドストレージへ一方向同期 — S3、R2、GCS、B2、S3 互換ストレージに対応。",
        "raidic": "AppleRAID を管理するネイティブ Mac アプリ — ターミナルなしでミラー、ストライプ、連結セットを作成・監視・修復。",
        "mergic": "フォルダを安全にマージ。MD5 検証つきの競合処理で、ファイルをもう失わない。",
        "nookic": "見たままの投稿を、自分の iPhone にそのまま残しておく小さな居場所。",
        "lossic": "Google Drive のロスレス音源を瞬時に再生。再生画面を右にスワイプすれば、AI による演奏者と楽曲の紹介、おすすめの質問、自分の AI キーで続ける会話へ。読み取り専用で直接接続します。",
        "openab_connect": "永続する coding agent 端末のためのネイティブ Mac コントロールセンター。接続、分割、音声入力、リモートセッション管理をひとつに。",
        "openab_remote": "iPhone で押して話すだけ。音声は端末上で文字化され、安全なテキストだけが Mac の OpenAB Connect に届きます。",
        "ribbon": "近日公開",
        "ribbon_internal": "内部限定",
        "footer": '<span class="squid">🦑</span> 小さなイカがつくりました · © 2026 tautiu · <a href="../privacy/">プライバシー</a> · <a href="mailto:tautiu.dev@gmail.com">お問い合わせ</a>',
    },
    "ko": {
        "html_lang": "ko",
        "title": "tautiu — 작은 인디 앱 스튜디오",
        "meta_desc": "tautiu(透抽)는 대만어로 오징어. 작은 오징어와 열 개의 바쁜 다리 — Mac과 iPhone을 위한 인디 앱: DeepSRT, DeepSRT Transcribe, Foldic, Recilic, Ripplic, Raidic, Mergic, Nookic, Lossic, OpenAB Connect, OpenAB Remote.",
        "og_title": "tautiu — 작은 인디 앱 스튜디오",
        "og_desc": "작은 오징어와 열 개의 바쁜 다리. 정성껏 만든 Mac & iPhone 앱.",
        "tagline": "작은 인디 앱 스튜디오",
        "story": """<span class="zh">tautiu（透抽）</span>는 대만어로 오징어 —
    작은 오징어 한 마리가 열 개의 바쁜 다리로,
    Mac과 iPhone을 위한 앱을 만들고 있어요.""",
        "deepsrt": "어떤 YouTube 영상도 즉시 AI 요약과 클릭 가능한 자막으로 — Mac 네이티브로.",
        "deepsrt_transcribe": "Apple 음성 모델로 완전 온디바이스 처리, 영상과 음성 모두 오프라인. 최강 Gemini 모델의 언어 최적화와 Google 검색 그라운딩으로 자동 교정까지.",
        "foldic": "사진 앨범을 실제 폴더로 미러링 — Mac에서는 자동으로, iPhone에서는 USB-C 드라이브로 바로.",
        "recilic": "나만의 프라이빗 백업 메시 — 가지고 있는 Mac과 드라이브를 종단간 암호화 백업 풀로.",
        "ripplic": "폴더에서 내 클라우드 스토리지로 단방향 동기화 — S3, R2, GCS, B2 및 S3 호환 스토리지 지원.",
        "raidic": "AppleRAID를 관리하는 네이티브 Mac 앱 — 터미널 없이 미러, 스트라이프, 연결 세트를 생성·모니터링·복구하세요.",
        "mergic": "폴더를 안전하게 병합. MD5 검증 충돌 처리로 파일을 잃지 않아요.",
        "nookic": "본 그대로의 게시물을 내 iPhone에 간직하는 작은 공간.",
        "lossic": "내 Google Drive의 무손실 음악을 즉시 재생하고, 오른쪽으로 스와이프해 AI 연주자·악곡 소개와 추천 질문을 만나세요. 내 AI 키로 대화를 이어 가며, Drive에는 읽기 전용으로 직접 연결합니다.",
        "openab_connect": "지속형 코딩 에이전트 터미널을 위한 네이티브 Mac 제어 센터. 연결, 화면 분할, 음성 입력, 원격 세션 관리를 한곳에서.",
        "openab_remote": "iPhone에서 누르고 말하세요. 음성은 기기에서 텍스트로 변환되고, 터미널에 안전한 텍스트만 Mac의 OpenAB Connect로 전송됩니다.",
        "ribbon": "출시 예정",
        "ribbon_internal": "내부 전용",
        "footer": '<span class="squid">🦑</span> 작은 오징어가 만들었어요 · © 2026 tautiu · <a href="../privacy/">개인정보 처리방침</a> · <a href="mailto:tautiu.dev@gmail.com">문의하기</a>',
    },
}

NAV_EN = '''<nav class="lang" aria-label="Language">
  <a href="./" data-lang="en" class="active">EN</a>
  <a href="zh/" data-lang="zh">中文</a>
  <a href="ja/" data-lang="ja">日本語</a>
  <a href="ko/" data-lang="ko">한국어</a>
</nav>'''

def nav_for(code):
    items = [("en", "../", "EN"), ("zh", "../zh/", "中文"),
             ("ja", "../ja/", "日本語"), ("ko", "../ko/", "한국어")]
    lines = ['<nav class="lang" aria-label="Language">']
    for c, href, label in items:
        active = ' class="active"' if c == code else ""
        lines.append(f'  <a href="{href}" data-lang="{c}"{active}>{label}</a>')
    lines.append('</nav>')
    return "\n".join(lines)

REDIRECT_RE = re.compile(r'<script>\s*// First visit only.*?</script>\n', re.S)

for code, t in LANGS.items():
    out = src
    out = out.replace('<html lang="en">', f'<html lang="{t["html_lang"]}">')
    out = out.replace(f'<title>{EN["title"]}</title>', f'<title>{t["title"]}</title>')
    out = out.replace(EN["meta_desc"], t["meta_desc"])
    out = out.replace(f'og:title" content="{EN["og_title"]}"', f'og:title" content="{t["og_title"]}"')
    out = out.replace(f'og:description" content="{EN["og_desc"]}"', f'og:description" content="{t["og_desc"]}"')
    out = out.replace('og:url" content="https://tautiu.dev"', f'og:url" content="https://tautiu.dev/{code}/"')
    # asset and internal page paths one level up
    out = out.replace('src="assets/', 'src="../assets/').replace('href="assets/', 'href="../assets/')
    assert 'href="deepsrt-transcribe/"' in out, "Transcribe app link not found"
    out = out.replace('href="deepsrt-transcribe/"', 'href="../deepsrt-transcribe/"')
    assert out.count('href="https://connect.openab.dev/"') == 2, "OpenAB links must stay shared and exact"
    # language nav
    assert NAV_EN in out, "nav block not found — update NAV_EN in this script"
    out = out.replace(NAV_EN, nav_for(code))
    # drop the auto-redirect script (translated pages ARE the destination)
    out2 = REDIRECT_RE.sub("", out)
    assert out2 != out, "redirect script not found"
    out = out2
    # content strings
    for key in ("tagline", "story", "deepsrt_transcribe", "deepsrt", "foldic", "recilic",
                "ripplic", "raidic", "mergic", "nookic", "lossic", "openab_connect", "openab_remote",
                "ribbon_internal", "ribbon", "footer"):
        assert EN[key] in out, f"source string for {key!r} not found"
        out = out.replace(EN[key], t[key])
    # app links → language-matched subpage (linked sites ship zh/ja/ko dirs)
    for domain in ("deepsrt.com", "foldic.app", "recilic.app",
                   "ripplic.app", "raidic.app", "mergic.foldic.app", "nookic.app"):
        needle = f'href="https://{domain}"'
        assert needle in out, f"app link for {domain} not found"
        out = out.replace(needle, f'href="https://{domain}/{code}/"')
    dst = os.path.join(ROOT, code, "index.html")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(out)
    print(f"wrote {code}/index.html ({len(out)} bytes)")

print("done")
