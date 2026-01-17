import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 設定（APIキーを貼り付けてください）
# ==========================================
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA"

genai.configure(api_key=GEMINI_API_KEY)
# 最新の安定モデルを指定
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI議事録・TODO生成", layout="wide")
st.title("📝 AI議事録：即実行TODO生成くん")
st.write("録音ファイルや声を解析して、次にやるべきことをリストアップします。")

# ==========================================
# 2. 音声の入力（録音またはファイルアップロード）
# ==========================================
st.subheader("1. 音声を準備する")
tab1, tab2 = st.tabs(["マイクで録音", "ファイル（MP3等）をアップロード"])

audio_data = None

with tab1:
    audio_record = st.audio_input("ここを押して話してください")
    if audio_record:
        audio_data = audio_record.read()

with tab2:
    audio_file = st.file_uploader("録音ファイルをドラッグ＆ドロップ", type=["mp3", "wav", "m4a"])
    if audio_file:
        audio_data = audio_file.read()

# ==========================================
# 3. AIによる解析
# ==========================================
if audio_data:
    st.subheader("2. AIでTODOを生成する")
    if st.button("議事録とTODOを作成", type="primary"):
        with st.spinner("AIが会議を振り返り、タスクを整理しています..."):
            try:
                # AIへの指示（プロンプト）
                prompt = """
                この音声を聞いて、以下の4つのセクションで議事録を作成してください。
                特に「TODO」は具体的に、誰が何をすべきか明確にしてください。

                1. 【決定事項】会議で決まったこと
                2. 【TODOリスト】すぐ実行すべきタスク（チェックボックス形式 [ ] で記述）
                3. 【重要ポイント】聞き漏らしてはいけない背景や理由
                4. 【保留・次回】今回は決まらなかったこと、次回の課題
                """

                # 通信エラーを回避する丁寧な呼び出し
                response = model.generate_content(
                    contents=[
                        {
                            "parts": [
                                {"text": prompt},
                                {"mime_type": "audio/wav", "data": audio_data}
                            ]
                        }
                    ]
                )

                st.success("作成完了しました！")
                
                # 結果の表示
                st.divider()
                st.markdown(response.text)
                
                # コピペ用のエリア
                st.subheader("そのままコピペ用")
                st.code(response.text, language="text")

            except Exception as e:
                st.error(f"解析エラー: {e}")
                st.info("APIキーが無効、またはモデル名が変更されている可能性があります。")

# ==========================================
# 4. 便利なヒント
# ==========================================
st.sidebar.title("使い方ヒント")
st.sidebar.info("""
- 会議の録音だけでなく、自分へのボイスメモにも使えます。
- 「今日やることを5つにまとめて」など、追加の要望がある場合は教えてください。
""")
