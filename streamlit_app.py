import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定
# ==========================================
# 最新のAPIキーをここに貼り付けてください
GEMINI_API_KEY = "AIzaSyCR1gN7-mfC1jsJxzWici2cVDwozgDsUnk"

# あなたのGAS（Google Apps Script）のURLをここに貼り付けてください
WEB_APP_URL = "ここにあなたのGASのURLを貼り付け"

# AIの設定
genai.configure(api_key=GEMINI_API_KEY)

# 404対策：最新のモデル指定方法
model = genai.GenerativeModel('gemini-1.5-flash')

# 施設リスト
STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

st.set_page_config(page_title="軽井沢実績システム", layout="wide")
st.title("🎙️ 音声入力・実績報告")

# ==========================================
# 2. 音声録音セクション
# ==========================================
st.subheader("ステップ1：音声で報告")
audio_value = st.audio_input("マイクを押して話してください")

if audio_value:
    if st.button("AIで解析する"):
        with st.spinner("AIが聞き取り中..."):
            try:
                # 音声データを読み込む
                audio_data = audio_value.read()
                
                # 【重要】404エラーを回避するための最も丁寧なデータ構成
                contents = [
                    {
                        "parts": [
                            {"text": "この音声を解析して、施設名、大人人数、子供人数、冷蔵庫1温度、冷蔵庫2温度、メモを日本語で抽出してください。"},
                            {"mime_type": "audio/wav", "data": audio_data}
                        ]
                    }
                ]
                
                # AIに依頼
                response = model.generate_content(contents=contents)
                
                st.success("解析成功！")
                st.markdown(f"**【解析結果】**\n\n{response.text}")
                
            except Exception as e:
                st.error(f"解析エラー: {e}")
                st.info("一度、この画面をリロード（再読み込み）してからもう一度試してみてください。")

# ==========================================
# 3. 入力フォーム
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
        temp1 = st.number_input("冷蔵庫1 温度", -30.0, 30.0, 0.0)
        temp2 = st.number_input("冷蔵庫2 温度", -30.0, 30.0, 0.0)
    
    memo = st.text_area("メモ")
    
    if st.form_submit_button("スプレッドシートに保存"):
        if WEB_APP_URL == "ここにあなたのGASのURLを貼り付け":
            st.warning("GASのURLを設定してください")
        else:
            data = {
                "date": str(target_date), "facility": facility,
                "adults": adults, "children": children,
                "temp1": temp1, "temp2": temp2, "memo": memo
            }
            res = requests.post(WEB_APP_URL, data=json.dumps(data))
            if "Success" in res.text:
                st.balloons()
                st.success("保存完了！")
