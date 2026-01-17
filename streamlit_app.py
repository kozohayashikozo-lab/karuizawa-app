import streamlit as st
import pandas as pd
from datetime import date

# --- 基本設定 ---
STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

# ★【重要】ここにコピーしたスプレッドシートのURLを貼り付けてください！
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Q20YXlNFSqLbR6wnFeLjARGYxzlI686XpdzbJhBz8Ok/edit?usp=sharing"

st.set_page_config(page_title="軽井沢4施設管理", layout="wide")

st.title("📱 軽井沢4施設 実績入力")

# 支配人用の入力フォーム
with st.form("input_form"):
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
    memo = st.text_area("特記事項（欠勤・トラブル等）")
    
    submitted = st.form_submit_button("実績を送信する")
    
    if submitted:
        # ここでスプレッドシートへ送るデータを作る
        st.success(f"{facility}の実績を送信しました！")
        st.balloons()
        st.write("※データはスプレッドシートに保存される設定に移行します。")
