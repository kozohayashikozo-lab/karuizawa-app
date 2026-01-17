import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定
# ==========================================
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA"
WEB_APP_URL = "ここにあなたのGASのURLを貼り付け" # ←ここを忘れずに！

# AIの設定（ここを最も安定した最新版に修正しました）
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-8b') # 名前を変更

STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

st.set_page_config(page_title="最強・音声実績システム", layout="wide")
st.title("🎙️ 軽井沢 施設実績・音声入力")

# ==========================================
# 2. 音声録音セクション
# ==========================================
st.subheader("ステップ1：音声で報告してください")
audio_value = st.audio_input("マイクを押して話してください")

if audio_value:
    if st.button("声を解析する"):
        with st.spinner("AIが聞き取り中..."):
            try:
                # 音声データを読み込んでAIがわかる形にする
                audio_data = audio_value.read()
                
                # AIへの指示
                prompt = "この音声から、施設名、大人人数、子供人数、冷蔵庫1温度、冷蔵庫2温度、メモを抽出して日本語で教えてください。"
                
                # AIに依頼（新しい形式）
                response = model.generate_content([
                    prompt,
                    {"mime_type": "audio/wav", "data": audio_data}
                ])
                
                st.success("AIの解析が完了しました！")
                st.info(response.text)
                
            except Exception as e:
                # もしこれでも404が出る場合はモデルを 'gemini-1.5-pro' に変える指示を出すため、エラーを表示
                st.error(f"解析エラー: {e}")

# ==========================================
# 3. 最終確認と送信フォーム
# ==========================================
st.divider()
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
        data = {"date": str(target_date), "facility": facility, "adults": adults, "children": children, "temp1": temp1, "temp2": temp2, "memo": memo}
        res = requests.post(WEB_APP_URL, data=json.dumps(data))
        if "Success" in res.text:
            st.balloons()
            st.success("保存されました！")
