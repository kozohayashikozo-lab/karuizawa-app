import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定（ここを書き換えてください）
# ==========================================
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA"
WEB_APP_URL = "ここにウェブアプリ(GAS)のURLを貼り付け" 

# AIの設定（ここを修正しました）
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

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
        with st.spinner("AIが内容を分析しています..."):
            try:
                # 音声データを読み込む
                audio_bytes = audio_value.read()
                
                # AIに渡す命令文
                prompt = """
                この音声を聞いて、以下の項目を抽出し、日本語のJSON形式で返してください。
                不明な項目は空欄（""）または0にしてください。
                項目：facility(施設名), adults(大人人数), children(子供人数), 
                temp1(冷蔵庫1温度), temp2(冷蔵庫2温度), memo(メモ)
                """
                
                # AIに依頼
                response = model.generate_content([
                    prompt,
                    {"mime_type": "audio/wav", "data": audio_bytes}
                ])
                
                st.success("AIが聞き取りました！")
                st.markdown(f"**解析結果:**\n\n{response.text}")
                
            except Exception as e:
                st.error(f"解析中にエラーが発生しました: {e}")

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
        data = {
            "date": str(target_date),
            "facility": facility,
            "adults": adults,
            "children": children,
            "temp1": temp1,
            "temp2": temp2,
            "memo": memo
        }
        res = requests.post(WEB_APP_URL, data=json.dumps(data))
        if "Success" in res.text:
            st.balloons()
            st.success("保存完了！")
