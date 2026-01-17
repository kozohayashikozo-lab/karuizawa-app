import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定
# ==========================================
# 先ほど教えていただいたAPIキーです
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA"

# ★ここに、前回作成したGoogleスプレッドシート(GAS)のURLを貼り付けてください
WEB_APP_URL = "ここにウェブアプリのURLを貼り付け"

# AIの設定（404エラー対策：最も安定した指定方法に変更）
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 施設リスト
STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

st.set_page_config(page_title="最強・音声実績システム", layout="wide")
st.title("🎙️ 軽井沢 施設実績・音声入力")

# ==========================================
# 2. 音声録音セクション
# ==========================================
st.subheader("ステップ1：音声で報告してください")
st.info("例：「トランス軽井沢、大人10人、子供2人。冷蔵庫1番は5.2度、2番はマイナス18度」")

audio_value = st.audio_input("マイクを押して話してください")

if audio_value:
    if st.button("声を解析する"):
        with st.spinner("AIが内容を分析しています..."):
            try:
                # 音声データを読み込む
                audio_data = audio_value.read()
                
                # AIに渡す指示
                prompt = """
                この音声を解析し、以下の項目を抽出して日本語で答えてください。
                ・施設名
                ・大人人数
                ・子供人数
                ・冷蔵庫1の温度
                ・冷蔵庫2の温度
                ・メモ（その他報告内容）
                """
                
                # AIに依頼
                response = model.generate_content([
                    prompt,
                    {"mime_type": "audio/wav", "data": audio_data}
                ])
                
                st.success("AIの解析が完了しました！")
                # 解析結果を表示
                st.markdown(f"### 【AIが聞き取った内容】\n\n{response.text}")
                st.warning("※下のフォームに内容が自動で入るわけではありません。上の結果を見て、自分で数字を修正・確認してください。")
                
            except Exception as e:
                st.error(f"解析エラーが発生しました: {e}")
                st.info("もし404エラーが続く場合は、APIキーをGoogle AI Studioで『新規作成(New Project)』し直してみてください。")

# ==========================================
# 3. 最終確認と送信フォーム
# ==========================================
st.divider()
st.subheader("ステップ2：内容を確認して送信")

with st.form("input_form"):
    target_date = st.date_input("日付", date.today())
    facility = st.selectbox("施設名", list(STATIONS.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        adults = st.number_input("大人人数", 0)
        children = st.number_input("子供人数", 0)
    with col2:
        temp1 = st.number_input("冷蔵庫1 温度", -30.0, 30.0, 0.0, step=0.1)
        temp2 = st.number_input("冷蔵庫2 温度", -30.0, 30.0, 0.0, step=0.1)
    
    memo = st.text_area("メモ・特記事項")
    
    submitted = st.form_submit_button("スプレッドシートに保存")
    
    if submitted:
        if WEB_APP_URL == "ここにウェブアプリのURLを貼り付け":
            st.error("GASのURLが設定されていません。")
        else:
            data = {
                "date": str(target_date),
                "facility": facility,
                "adults": adults,
                "children": children,
                "temp1": temp1,
                "temp2": temp2,
                "memo": memo
            }
            try:
                res = requests.post(WEB_APP_URL, data=json.dumps(data))
                if "Success" in res.text:
                    st.balloons()
                    st.success("スプレッドシートへの保存に成功しました！")
                else:
                    st.error(f"保存失敗: {res.text}")
            except Exception as e:
                st.error(f"送信エラー: {e}")
