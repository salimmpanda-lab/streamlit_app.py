import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mfumo wa Kikundi", layout="wide")

# DATABASE
conn = sqlite3.connect("kikundi.db", check_same_thread=False)
c = conn.cursor()

# TABLES

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

c.execute("""
CREATE TABLE IF NOT EXISTS social_fund(
id INTEGER PRIMARY KEY AUTOINCREMENT,
member TEXT,
amount INTEGER,
date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS emergency_loans(
id INTEGER PRIMARY KEY AUTOINCREMENT,
member TEXT,
amount INTEGER,
date TEXT
)
""")

conn.commit()

st.title("Mfumo wa Kikundi cha Huduma Ndogo ya Fedha")

menu = st.sidebar.selectbox(
"Chagua Sehemu",
[
"Dashboard",
"Wanachama",
"Hisa",
"Mikopo",
"Mfuko wa Jamii",
"Ripoti"
]
)

# DASHBOARD
if menu == "Dashboard":

    st.header("Muhtasari wa Kikundi")

    members = pd.read_sql("SELECT * FROM members", conn)
    social = pd.read_sql("SELECT * FROM social_fund", conn)

    total_members = len(members)
    total_shares = members["shares"].sum() if total_members>0 else 0
    share_fund = total_shares * 5000
    social_fund_total = social["amount"].sum() if len(social)>0 else 0

    col1,col2,col3 = st.columns(3)

    col1.metric("Wanachama", total_members)
    col2.metric("Mfuko wa Hisa", f"TSh {share_fund}")
    col3.metric("Mfuko wa Jamii", f"TSh {social_fund_total}")

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

    if len(members)==0:

        st.warning("Hakuna wanachama bado")

    else:

        member = st.selectbox("Chagua Mwanachama", members["name"])

        shares = st.number_input("Idadi ya Hisa",1,20)

        if st.button("Nunua Hisa"):

            amount = shares * 5000

            c.execute("""
            UPDATE members
            SET shares = shares + ?
            WHERE name = ?
            """,(shares,member))

            conn.commit()

            st.success(f"{member} amenunua hisa {shares}")
            st.write("Thamani:", amount)

# LOANS
elif menu == "Mikopo":

    st.header("Maombi ya Mkopo")

    members = pd.read_sql("SELECT * FROM members", conn)

    if len(members) == 0:

        st.warning("Sajili wanachama kwanza")

    else:

        member = st.selectbox("Mwanachama", members["name"])

        amount = st.number_input("Kiasi cha Mkopo", min_value=1000)

        months = st.slider("Muda wa Mkopo (miezi)",1,4)

        if st.button("Hesabu Mkopo"):

            if datetime.now().month == 11:

                st.error("Hakuna mikopo mwezi Novemba")

            else:

                # calculations
                interest = amount * 0.05 * months
                insurance = amount * 0.02
                total_repayment = amount + interest
                monthly_payment = total_repayment / months
                receive_amount = amount - insurance

                st.subheader("Muhtasari wa Mkopo")

                st.write("Kiasi cha Mkopo:", amount)
                st.write("Bima (2%):", insurance)
                st.write("Kiasi atakachopokea Mkopaji:", receive_amount)
                st.write("Riba ya Jumla:", interest)
                st.write("Jumla ya kurejesha:", total_repayment)
                st.write("Malipo kwa mwezi:", monthly_payment)

                # repayment schedule
                schedule = []

                for i in range(1, months+1):

                    schedule.append({
                        "Mwezi": i,
                        "Malipo": monthly_payment
                    })

                df = pd.DataFrame(schedule)

                st.subheader("Ratiba ya Marejesho")

                st.table(df)

        if st.button("Hifadhi Mkopo"):

            interest = amount * 0.05 * months
            insurance = amount * 0.02
            total = amount + interest

            c.execute("""
            INSERT INTO loans
            (member,amount,months,interest,insurance,total,date)
            VALUES (?,?,?,?,?,?,?)
            """,
            (member,amount,months,interest,insurance,total,str(datetime.now()))
            )

            conn.commit()

            st.success("Mkopo umehifadhiwa kwenye mfumo")

# SOCIAL FUND
elif menu == "Mfuko wa Jamii":

    st.header("Michango ya Mfuko wa Jamii")

    members = pd.read_sql("SELECT * FROM members", conn)

    if len(members)==0:

        st.warning("Hakuna wanachama")

    else:

        member = st.selectbox("Mwanachama", members["name"])

        if st.button("Rekodi Mchango (1000)"):
            
            c.execute("""
            INSERT INTO social_fund
            (member,amount,date)
            VALUES (?,?,?)
            """,(member,1000,str(datetime.now())))

            conn.commit()

            st.success("Mchango umehifadhiwa")

    st.subheader("Mkopo wa Dharura")

    member2 = st.selectbox("Chagua Mwanachama wa Mkopo", members["name"])

    amount2 = st.number_input("Kiasi cha Mkopo",0,100000)

    if st.button("Toa Mkopo wa Dharura"):

        c.execute("""
        INSERT INTO emergency_loans
        (member,amount,date)
        VALUES (?,?,?)
        """,(member2,amount2,str(datetime.now())))

        conn.commit()

        st.success("Mkopo wa dharura umetolewa")

# REPORTS
elif menu == "Ripoti":

    st.header("Ripoti za Mikopo")

    loans = pd.read_sql("SELECT * FROM loans", conn)

    st.dataframe(loans)

    st.subheader("Michango ya Mfuko wa Jamii")

    social = pd.read_sql("SELECT * FROM social_fund", conn)

    st.dataframe(social)
