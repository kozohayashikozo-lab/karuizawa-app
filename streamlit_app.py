import streamlit as st
import pandas as pd
from datetime import date
from io import StringIO
import requests

# --- 基本設定 ---
STATIONS = {"トランス軽井沢": 8, "軽井沢清風荘": 10, "ゆうせん軽井沢": 9, "オリックス軽井沢": 14}

# ★【重要】ご自身のスプレッドシートURLを貼り付けてください
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Q20YXlNFSqLbR6wnFeLjARGYxzlI686XpdzbJhBz8Ok/edit?usp=sharing"

# Google Apps Script 等を使わずに簡易的に連携する設定
st.set_page_config(page_title="軽井沢4施設管理システム", layout="wide")

st.title("📱 軽井沢4施設 実績入力フォーム")

# 入力フォーム
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
        # 本来はここにAPI連携のコードを書きますが、
        # まずは「送信データ」が正しく作られているか画面に表示します
        st.success(f"【送信確認】{facility} のデータを正常に受け付けました。")
        
        # 入力内容のサマリーを表示
        st.write(f"送信内容：{target_date} / 客室:{rooms} / 客数:{adults+children} / 夕食:{meals} / 仕入れ:{cost}円")
        st.balloons()

st.info("💡 データの蓄積について：現在、セキュリティを保ちながらスプレッドシートへ直接書き込むための『橋渡し役（Google Apps Script）』の準備を推奨しています。")
