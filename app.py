# -*- coding: utf-8 -*-
import sys
import os

# Windowsの文字コード判定をUTF-8に強制上書き
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

if hasattr(sys, 'reconfigure'):
    try:
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ===========================================================================
# 選ばれるガクチカ＆自己PRのための √Structure (ルート構造) AI添削
# Streamlit Webアプリ用 完全版コード
# ===========================================================================
import os
import re
import time
import requests
import json
import streamlit as st
import io
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

def create_pdf(text):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    # 日本語フォントの設定
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
    p.setFont('HeiseiKakuGo-W5', 10)
    
    y = 800
    # 文章を改行ごとに分割
    for line in text.split('\n'):
        # 長い行を自動で折り返す（A4幅に合わせて全角45文字で改行）
        wrapped_lines = textwrap.wrap(line, width=45)
        
        # 空行（改行のみ）の場合の処理
        if not wrapped_lines:
            y -= 15
            continue
            
        for w_line in wrapped_lines:
            if y < 50:
                p.showPage()
                p.setFont('HeiseiKakuGo-W5', 10)
                y = 800
            p.drawString(40, y, w_line)
            y -= 15
            
    p.save()
    buffer.seek(0)
    return buffer

# ---------------------------------------------------------------------------
# 0. モニター限定のパスワード設定
# ---------------------------------------------------------------------------
MONITOR_PASSWORD = "hizume_lab"

# ---------------------------------------------------------------------------
# 1. ルート構造添削システム：完成版システムプロンプト定義（マイルドなトーン版）
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
あなたは、中央経済社刊の著書で提唱された就活理論「ルート構造」を完全に熟知した超プロ級の就活アドバイザーAIです。
就活生から提出された7つの構成要素（p1〜p7）を元に、選考通過率を最大化させるESの推敲と面接対策を行ってください。

【入力される7つの要素】
①（失敗等の経験）
②（傷心・反省・感情の言葉）
③（気付き）
④（新たな行動工夫）
⑤（結果）
⑥（学んだこと）
⑦（入社後の工夫）

【出力文体・トーン】
・論理的でありながら、学生らしい誠実さと熱意が伝わる自然な文体で作成してください。過度に硬い熟語（「猛省」「看破」「創出」など）は避け、「深く反省し」「気づき」「作り出し」といった、面接で本人が自分の言葉として違和感なく話せる等身大の丁寧な表現を使用してください。

【特別指示：中高エピソードの接続】
・入力素材が中学・高校時代のエピソード中心である場合は、⑥学びの末尾を単に「現在の活動でも心がけています」とするのではなく、
  「この学びは、現在の大学生活やアルバイト、サークル活動でも常に心がけています」のように、過去の経験を現在の大学での行動へ繋げる具体的な表現に補強すること。

【出力フォーマット】
回答は必ず以下の4つのセクション構成で厳密に出力してください。

### 1. 【プロ引き上げES（本選考400字用）】
・「ルート構造」に基づき、①〜⑦の要素を論理的に再構築した350〜390字程度の完成文章を作成してください。
・冒頭は継続力をアピールするため、「〇年間継続している『〜』です」の形で書き始めてください。
・※Web提出フォームで401文字以上は足切りとなるため、指定上限字数の400文字は1文字たりとも超えないこと（350〜390文字を厳守）。
・文章の深みと組織貢献度をアピールするため、必要に応じて「現在では後輩の指導や育成役も任されています」等の要素を自然に補強・挿入してください。

### 2. 【プロ引き上げES（短縮200字用）】
・400字用の要点を保持したまま、180〜195字程度に圧縮した簡潔でインパクトのある文章を作成してください。
・※200字版は文字数不足や詰め込み感を防ぐため、抱負⑦は省略し、学び⑥（またはその学びの現在への実践）で簡潔に締めること。
・※指定上限字数の200文字は1文字たりとも超えないこと（180〜195文字を厳守）。

### 3. 【面接対策：面接官が絶対に突いてくる3つの深掘りポイント（罠の準備）】
以下の3つの視点から、面接官の鋭い深掘り質問と回答のポイント・準備例を提示してください。
※「雑談で仲良くなった」等の抽象的な回答に留めず、「共有ノートの作成・運用」のように泥臭く具体的な工夫・プロセスの回答例を必ず作成してください。
① 【挫折と感情の深掘り（p1, p2関連）】
② 【自発的行動・工夫の具体性（p4関連）】
③ 【会社での再現性・貢献（p6, p7関連） または 中高エピソードの現在への応用】
  ※中高のエピソードを「現在の大学生活やアルバイトでも心がけている」と接続した場合は、面接官から「具体的に今のアルバイトやサークルで、その学びをどのように行動に移しているか？」と問われた際の泥臭く具体的な回答準備例（例：「バイト先で〇〇な工夫をしている」等）を質問③に組み込むこと。

### 4. 【プロからの指導講評・アドバイス】
・行動・学び・抱負の軸の一致、数字の具体化について評価・助言してください。
・【ガクチカ / 自己PRの適性判定】：このエピソードが「ガクチカ向き」か「自己PR向き」かの判定と理由。
  ※中学・高校時代の経験がベースであり、それを「現在の大学生活やアルバイトでもモットーとして実践している」構成になっている場合は、長い時間軸で一貫した強み・行動原則を証明する【自己PR向き】としての適性が高い旨を明記し、冒頭を「私の強みは〜」に書き換えるアレンジ例を提示すること。
・【後輩指導・組織貢献の実践アドバイス】：400字版に補強した「後輩指導・サポート役」について、「面接で自信を持って語れるよう、今日からのアルバイトやサークルで、後輩に自ら声をかけたり仕事を教えてあげる行動を早速スタートして、リアルな事実（実績）を作っておきましょう！」と熱く促すこと。
"""

# ---------------------------------------------------------------------------
# 2. 内部関数群（文字数カウント・LLM呼び出し・自動リトライ処理）
# ---------------------------------------------------------------------------
def count_pure_text_length(text: str) -> int:
    pure_text = re.sub(r'\s+', '', text)
    return len(pure_text)

def extract_es_texts(response_content: str):
    pattern_400 = r"(?:###\s*)?1\.\s*【.*?400字.*?】\s*\n+(.*?)(?=\n+(?:###\s*)?2\.|\Z)"
    pattern_200 = r"(?:###\s*)?2\.\s*【.*?200字.*?】\s*\n+(.*?)(?=\n+(?:###\s*)?3\.|\Z)"
    
    match_400 = re.search(pattern_400, response_content, re.DOTALL)
    match_200 = re.search(pattern_200, response_content, re.DOTALL)
    
    text_400 = match_400.group(1).strip() if match_400 else ""
    text_200 = match_200.group(1).strip() if match_200 else ""
    
    text_400 = re.sub(r'（\d+文字）|\(\d+文字\)', '', text_400).strip()
    text_200 = re.sub(r'（\d+文字）|\(\d+文字\)', '', text_200).strip()
    
    return text_400, text_200

def call_gemini(user_input: str) -> str:
    # クラッシュ防止：st.secrets を安全に読み込む処理
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return "【エラー】GEMINI_API_KEY が取得できませんでした。`.streamlit/secrets.toml` または環境変数を確認してください。"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "system_instruction": {
            "parts": [{"text": str(SYSTEM_PROMPT)}]
        },
        "contents": [{
            "parts": [{"text": str(user_input)}]
        }],
        "generationConfig": {
            "temperature": 0.4
        }
    }

    # 混雑時（503エラー等）の自動再試行（最大3回）
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=(10, 60))
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code == 503:
                if attempt < max_retries - 1:
                    time.sleep(3 * (attempt + 1))  # 3秒、6秒と待機時間を延ばして自動リトライ
                    continue
                else:
                    return "【エラー】AIサーバーが混雑しています（503エラー）。数十秒ほど時間をおいて再実行してください。"
            else:
                return f"APIエラー (HTTP {response.status_code}): {response.text}"

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            err_detail = repr(e)
            st.error(f"API通信エラー詳細: {err_detail}")
            return f"エラーが発生しました: {err_detail}"

# ---------------------------------------------------------------------------
# 3. Streamlit UI 構築
# ---------------------------------------------------------------------------
st.set_page_config(page_title="√Structure AI添削", page_icon="🌱", layout="centered")

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.image("logo.jpeg", use_container_width=True)
        st.markdown("<h2 style='text-align: center; color: #1f3a93;'>The √ Structure Method for ES</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>選ばれるガクチカ＆自己PRのためのAIアドバイザー</p>", unsafe_allow_html=True)
        
        pwd = st.text_input("モニター用パスワードを入力してください", type="password")
        if st.button("ログイン"):
            if pwd == MONITOR_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("パスワードが間違っています。")
        return False
    return True

if check_password():
    st.image("logo.jpeg", use_container_width=True)
    st.markdown("<h2 style='color: #1f3a93;'>√Structure (ルート構造) AI添削</h2>", unsafe_allow_html=True)
    st.write("授業で学んだ「ルート構造」の7つの要素を入力してください。AIがあなたの経験を、選考を通過するレベルへと引き上げます。")
    st.info("※「ルート構造」は、国家資格キャリアコンサルティング技能士・日詰慎一郎の独自メソッドとして商標登録出願中（第35・41・42類）です。")

    with st.form("input_form"):
        essay_type = st.radio(
            "■ 添削モードの選択",
            ("自動", "ガクチカとして添削", "自己PRとして添削"),
            horizontal=True,
            help="特定の設問として添削したい場合は選択してください。「自動」の場合は文章の内容からAIが判断します。"
        )
        st.write("")

        # ① 失敗・困難などの経験
        p1 = st.text_area("① 失敗等の経験（挫折や課題など）", 
                          placeholder="例：カフェのアルバイトで、新人研修を任されたが最初は上手く教えられなかった。",
                          help="【NG】単なる状況説明\n【OK】自身の至らなさや直面した壁")
        st.caption("⚠️ **【NG】**「レジが混んで大変だった」といった単なる状況説明 / **【OK】**自身の至らなさや、直面した壁を具体的に書く")
        st.caption("💡 **【考えるヒント・問いかけ】**「その時、一番『焦った』『悔しい』と感じた具体的な出来事は何ですか？」「誰かに迷惑をかけてしまったり、自分の力不足を痛感した場面はありましたか？」")
        st.write("")

        # ② 反省・傷心
        p2 = st.text_area("② 傷心・反省・感情の言葉", 
                          placeholder="例：自分の説明不足を痛感し、後輩に申し訳ない気持ちになった。",
                          help="【NG】表面的な感想\n【OK】原因の自己分析")
        st.caption("⚠️ **【NG】**「申し訳ないと思った」「次は気をつけよう」という表面的な感想 / **【OK】**自分の何が足りなかったのか、原因を自己分析する")
        st.caption("💡 **【考えるヒント・問いかけ】**「その失敗をした瞬間、どのような気持ちになりましたか？」「今振り返ると、自分のどのような考え方や行動が原因だったと思いますか？」")
        st.write("")

        # ③ 気づき
        p3 = st.text_area("③ 気付き", 
                          placeholder="例：一方的に教えるのではなく、相手の理解度に合わせて伝える必要があると気づいた。",
                          help="【NG】一般論\n【OK】新しい視点やターゲットの特定")
        st.caption("⚠️ **【NG】**「もっと丁寧にすべきだと気づいた」という一般論 / **【OK】**状況を好転させるための「新しい視点」や「ターゲットの特定」")
        st.caption("💡 **【考えるヒント・問いかけ】**「その失敗を踏まえて、次は『どこを』『誰に対して』『どう変えれば』上手くいくと考えましたか？」")
        st.write("")

        # ④ 新たな行動工夫
        p4 = st.text_area("④ 新たな行動工夫", 
                          placeholder="例：マニュアルを図解化し、作業後に必ず振り返りの時間を10分設けた。",
                          help="【NG】抽象的な表現\n【OK】映像が浮かぶ具体的なアクションと周囲の巻き込み")
        st.caption("⚠️ **【NG】**「一生懸命声かけをした」という抽象的な表現 / **【OK】**映像が浮かぶ具体的なアクションと、周囲を巻き込んだ事実")
        st.caption("💡 **【考えるヒント・問いかけ】**「具体的にどのような行動をとり、どんな言葉をかけましたか？」「自分一人で解決しようとしましたか？それとも周囲の誰かに協力を仰ぎましたか？」")
        st.write("")

        # ⑤ 結果
        p5 = st.text_area("⑤ 結果", 
                          placeholder="例：後輩の独り立ちが2週間早まり、店長からも教え方を褒められた。",
                          help="【NG】主観的な感想\n【OK】数字、他者からの評価など客観的変化")
        st.caption("⚠️ **【NG】**「雰囲気が良くなった気がする」という主観的な感想 / **【OK】**数字、他者からの評価、目に見える客観的な変化")
        st.caption("💡 **【考えるヒント・問いかけ】**「その行動の後、周囲の人（店長、お客様、チームメンバーなど）からどのような言葉をかけられましたか？」「数字で表せる変化はありましたか？」")
        st.write("")

        # ⑥ 学んだこと
        p6 = st.text_area("⑥ 学んだこと", 
                          placeholder="例：相手の立場に立って考え、仕組みを改善することの大切さを学んだ。",
                          help="【NG】浅い結論\n【OK】汎用的な能力への昇華")
        st.caption("⚠️ **【NG】**「コミュニケーションは大事だと学んだ」という浅い結論 / **【OK】**他の仕事や場面でも使える「汎用的な能力」への昇華")
        st.caption("💡 **【考えるヒント・問いかけ】**「この一連の経験を通して、社会や仕事において『何が一番大切』だと学びましたか？」「この教訓は、他のどのような場面で活かせそうですか？」")
        st.write("")

        # ⑦ 入社後の工夫
        p7 = st.text_area("⑦ 入社後の工夫", 
                          placeholder="例：この経験を活かし、チームの課題解決や業務効率化に貢献したい。",
                          help="【NG】定型文\n【OK】特定の職種・業務とリンクさせる")
        st.caption("⚠️ **【NG】**「この学びを活かして御社でも頑張ります」という定型文 / **【OK】**志望企業の「特定の職種・業務」と学びをリンクさせる")
        st.caption("💡 **【考えるヒント・問いかけ】**「この経験で得た『強み』や『学び』は、志望企業の〇〇職のどのような業務で一番発揮できそうですか？」")
        st.write("")
        
        submitted = st.form_submit_button("✨ AIに添削・面接対策を依頼する")

    if submitted:
        if not all([p1, p2, p3, p4, p5, p6, p7]):
            st.warning("すべての項目（①〜⑦）を入力してください。箇条書きや短い文章でも大丈夫です！")
        else:
            with st.spinner("AIが日詰教授のメソッドであなたの文章を論理的に再構築しています...（約30〜40秒）"):
                if essay_type == "ガクチカとして添削":
                    mode_instruction = "【優先指示】この文章は「ガクチカ（学生時代に最も力を入れたこと）」として添削してください。特に①〜⑤の行動プロセスや課題解決の具体性を重点的に評価・指導してください。\n"
                elif essay_type == "自己PRとして添削":
                    mode_instruction = "【優先指示】この文章は「自己PR」として添削してください。特に⑥〜⑦の強みの明確さや、入社後の仕事における再現性・貢献度を重点的に評価・指導してください。\n"
                else:
                    mode_instruction = ""

                user_input = f"""
{mode_instruction}
①（失敗等の経験）: {p1}
②（傷心・反省・感情の言葉）: {p2}
③（気付き）: {p3}
④（新たな行動工夫）: {p4}
⑤（結果）: {p5}
⑥（学んだこと）: {p6}
⑦（入社後の工夫）: {p7}
"""
                ai_output = call_gemini(user_input)
                
                if ai_output.startswith("【エラー】") or ai_output.startswith("【システムエラー】"):
                    st.error(ai_output)
                else:
                    st.success("添削が完了しました！結果を確認してください。")
                    
                    es_400, es_200 = extract_es_texts(ai_output)
                    len_400 = count_pure_text_length(es_400)
                    len_200 = count_pure_text_length(es_200)
                    st.markdown(f"**【実文字数チェッカー】** 400字版: `{len_400}字` / 200字版: `{len_200}字`")
                    st.caption("※AIの特性上、指定文字数を若干前後する場合があります。提出前に文字数を微調整してください。")
                    st.info("💡 **ワンポイントアドバイス**\n面接では緊張するので、ルートの形状を意識して、ルートの順番で伝えましょう！")
                    
                    st.markdown("---")
                    st.image("logo.jpeg", use_container_width=True)
                    
                    # 添削結果の表示
                    st.markdown(ai_output)
                    
                    # ↓↓↓ 4か所目：PDFダウンロードボタン ↓↓↓
                    st.markdown("---")
                    pdf_text = f"{ai_output}\n\n---------------------------------------------\n【実文字数チェッカー】\n400字版: {len_400}字 / 200字版: {len_200}字\n※AIの特性上、指定文字数を若干前後する場合があります。\n\n💡 ワンポイントアドバイス\n面接では緊張するので、ルートの形状を意識して、ルートの順番で伝えましょう！"
                    pdf_data = create_pdf(pdf_text)
                    
                    st.download_button(
                        label="📥 添削結果をPDFで保存",
                        data=pdf_data,
                        file_name="ES_Advice_Report.pdf",
                        mime="application/pdf"
            )
            
