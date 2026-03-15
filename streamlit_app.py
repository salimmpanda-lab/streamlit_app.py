import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mfumo wa Kikundi", layout="wide")

# DATABASE
conn = sqlite3.connect("kikundi.db", check_same_thread=False)
c = conn.cursor()

# CREATE TABLES
c.execute("""
CREATE TABLE IF NOT EXISTS members(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
shares INTEGER DEFAULT 0
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS loans(
id INTEGER PRIMARY KEY AUTOINCREMENT,
member TEXT,
amount INTEGER,
months INTEGER,
interest INTEGER,
insurance INTEGER,
total INTEGER,
date TEXT
)
""")

conn.commit()

st.title("Mfumo wa Kikundi cha Huduma Ndogo ya Fedha")

menu = st.sidebar.selectbox(
"Chagua Sehemu",
["Dashboard","Wanachama","Hisa","Mikopo","Ripoti"]
)

# DASHBOARD
if menu == "Dashboard":

    st.header("Muhtasari wa Kikundi")

    df = pd.read_sql("SELECT * FROM members", conn)

    total_members = len(df)

    total_shares = df["shares"].sum() if total_members > 0 else 0

    share_fund = total_shares * 5000

    col1,col2,col3 = st.columns(3)

    col1.metric("Wanachama", total_members)
    col2.metric("Jumla ya Hisa", total_shares)
    col3.metric("Mfuko wa Hisa", f"TSh {share_fund}")

# MEMBERS
elif menu == "Wanachama":

    st.header("Usajili wa Wanachama")

    name = st.text_input("Jina la Mwanachama")

    if st.button("Sajili Mwanachama"):

        c.execute("INSERT INTO members (name) VALUES (?)",(name,))
        conn.commit()

        st.success("Mwanachama ameongezwa")

    st.subheader("Orodha ya Wanachama")

    df = pd.read_sql("SELECT * FROM members", conn)

    st.dataframe(df)

# SHARES
elif menu == "Hisa":

    st.header("Ununuzi wa Hisa")

    members = pd.read_sql("SELECT * FROM members", conn)

    if len(members) == 0:

        st.warning("Hakuna wanachama bado
