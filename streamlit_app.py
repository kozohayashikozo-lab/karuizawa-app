import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定
# ==========================================
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA"
WEB_APP_URL = "ここにウェブアプリ(GAS)のURLを貼り付け" # ←ここだけ忘れずに！

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
audio_value = st.audio_input("マイクを押して話してください")

if audio_value:
    # ボタンが押されたら解析開始
    if st.button("声を解析する"):
        with st.spinner("AIが内容を分析しています..."):
            try:
                # 【修正ポイント】音声データをAIが読める形式に変換
                audio_data = {
                    "mime_type": "audio/wav",
                    "data": audio_value.read()
                }
                
                prompt = """
                この音声を聞いて、以下の項目を抽出し、日本語のJSON形式で返してください。
                不明な項目は空欄（""）または0にしてください。
                項目：facility(施設名), adults(大人人数), children(子供人数), 
                temp1(冷蔵庫1温度), temp2(冷蔵庫2温度), memo(メモ)
                """
                
                # AIに依頼
                response = model.generate_content([prompt, audio_data])
                
                st.success("AIが聞き取りました！")
                st.markdown(f"**解析結果:**\n\n{response.text}")
                
            except Exception as e:
                st.error(f"解析中にエラーが発生しました: {e}")

# ==========================================
# 3. 最終確認と送信フォーム
# ==========================================
st.divider()
st.subheader("ステップ2：内容を確認して送信")
# （以下、前のフォームと同じなので省略...GitHubの画面に貼り付ける際は、
# 前回のコードの「3.最終確認と送信フォーム」以降をそのまま残して繋げてくださいね）
