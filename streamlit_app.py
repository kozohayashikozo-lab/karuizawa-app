import streamlit as st
import requests
import json
from datetime import date

# --- 設定 ---
# ここに「デプロイ」で取得したURLを貼り付けます
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz7Zm-RxqCfRhZGLrhzslqdGgb0QvG2v8YpqQo_-jTdIpedcF7J0x9BdIjVX2Tqop3j3g/exec"

STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

st.set_page_config(page_title="軽井沢実績管理", layout="wide")
st.title("🏨 軽井沢4施設 実績入力")

with st.form("input_form", clear_on_submit=True):
    target_date = st.date_input("日付", date.today())
    facility = st.selectbox("施設名", list(STATIONS.keys()))
    col1, col2 = st.columns(2)
    with col1:
        rooms = st.number_input("稼働客室数", 0, STATIONS[facility])
        adults = st.number_input("大人人数", 0)
        children = st.number_input("子供人数", 0)
    with col2:
        meals = st.number_input("夕食提供数", 0)
        cost = st.number_input("本日の仕入れ額(円)", 0)
    
    help_status = st.select_slider("サービス人員の状況", ["余裕あり", "適正", "ヘルプ必要"])
    memo = st.text_area("特記事項")
    
    submitted = st.form_submit_button("実績を送信する")
    
    if submitted:
        data = {
            "date": str(target_date),
            "facility": facility,
            "rooms": rooms,
            "adults": adults,
            "children": children,
            "meals": meals,
            "cost": cost,
            "help_status": help_status,
            "memo": memo
        }
        
        try:
            response = requests.post(WEB_APP_URL, data=json.dumps(data))
            if "Success" in response.text:
                st.success(f"{facility}のデータを保存しました！スプレッドシートを確認してください。")
                st.balloons()
            else:
                st.error("保存に失敗しました。窓口（GAS）の設定を確認してください。")
        except Exception as e:
            st.error(f"接続エラーが発生しました。URLを再確認してください。")
