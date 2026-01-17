import streamlit as st
import requests
import json
from datetime import date
import google.generativeai as genai

# ==========================================
# 1. あなたの専用設定
# ==========================================
# 新しく作成したAPIキーをここに貼り付けてください
GEMINI_API_KEY = "AIzaSyCCecamXHkFXPT5J1gkIYXRjv5Sm4xkQDA"

# あなたのGAS（Google Apps Script）のURLをここに貼り付けてください
WEB_APP_URL = "ここにあなたのGASのURLを貼り付け"

# AIの設定：404エラーを回避するための最も標準的な記述
genai.configure(api_key=GEMINI_API_KEY)

# モデル名をシンプルに指定（これでも404が出る場合は 'gemini-1.5-flash' に戻すなど試せます）
model = genai.GenerativeModel('gemini-1.5-flash')

# 施設リスト
STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

st.set_page_config(page_title="軽井沢 施設実績システム", layout="wide")
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
                
                # 指示文（プロンプト）
                prompt = "この音声を解析し、施設名、大人人数、子供人数、冷蔵庫1温度、冷蔵庫2温度、メモを抽出して日本語で答えてください。"
                
                # AIへの依頼（最新のパーツ指定形式）
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
                
                st.success("解析成功！")
                st.markdown(f"**【解析結果】**\n\n{response.text}")
                
            except Exception as e:
                # 万が一のエラー表示
                st.error(f"解析エラー: {e}")
                st.info("APIキーが有効になるまで数分かかる場合があります。少し待ってから再度お試しください。")

# ==========================================
# 3. 入力フォーム
# ==========================================
st.divider()
st.subheader("ステップ2：最終確認と送信")

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
