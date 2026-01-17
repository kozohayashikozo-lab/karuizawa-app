import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定（ここを書き換えてください）
# ==========================================
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA" # ←貼り付けました
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz7Zm-RxqCfRhZGLrhzslqdGgb0QvG2v8YpqQo_-jTdIpedcF7J0x9BdIjVX2Tqop3j3g/exec" # ←前回のURLを！

# AIの設定
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

st.set_page_config(page_title="最強・音声実績システム", layout="wide")
st.title("🎙️ 軽井沢 施設実績・音声入力")

# ==========================================
# 2. 音声録音セクション
# ==========================================
st.subheader("ステップ1：音声で報告してください")
st.info("例：「トランス軽井沢、大人10人、子供2人。冷蔵庫1番は5.2度、2番はマイナス18度。今日は忙しかったです」")

audio_value = st.audio_input("マイクを押して話してください")

# 音声が録音されたらAIで解析
if audio_value:
    with st.spinner("AIが内容を分析しています..."):
        try:
            # AIに音声を読み込ませて情報を抽出させる指示
            prompt = """
            この音声から以下の情報を抽出し、日本語のJSON形式で返してください。
            不明な項目は空欄（""）にしてください。
            項目：施設名(facility), 大人人数(adults), 子供人数(children), 
            冷蔵庫1温度(temp1), 冷蔵庫2温度(temp2), メモ(memo)
            """
            response = model.generate_content([prompt, audio_value])
            
            # AIの結果を表示
            st.success("AIが聞き取りました！")
            st.markdown(f"**解析結果のプレビュー:**\n\n{response.text}")
            st.warning("※下のフォームに自動反映はされていません。上の結果を見ながら最終確認して送信してください。")
            
        except Exception as e:
            st.error(f"AI解析エラー: {e}")

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
        # GASに送信
        res = requests.post(WEB_APP_URL, data=json.dumps(data))
        if "Success" in res.text:
            st.balloons()
            st.success("スプレッドシートに無事保存されました！")
