import streamlit as st

st.set_page_config(page_title="Mfumo wa Kikundi", layout="wide")

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

    col1,col2,col3 = st.columns(3)

    col1.metric("Wanachama",17)
    col2.metric("Mfuko wa Hisa","TSh 0")
    col3.metric("Mfuko wa Jamii","TSh 0")

    st.success("Karibu kwenye mfumo wa kikundi")

# MEMBERS
elif menu == "Wanachama":

    st.header("Orodha ya Wanachama")

    members = [
    "PAUL COSMAS MWENDA",
    "SALIM YUSUPH MPANDA",
    "DAUDI MWAMBENJA",
    "JOYCE JUMA MHENDE",
    "FRANCIS JOHN SANGA",
    "BLANDINA ALOYCE KESSY",
    "ESTER BETHUEL WAITARA",
    "JOSEPH K. MGIMWA",
    "ODRIA S. SINDAMENYA",
    "ANDERSON LINUSY KISAVA",
    "PENDO JOHN MGIMWA",
    "ANDREW KISAVA WILIAM",
    "PROSISTA KIWANGO",
    "FROLA METHOD NGOMOI",
    "MARY STEPHEN LUGISA",
    "SALOME S. KISHOSHA",
    "EDINA MTOMO NHONYA"
    ]

    for m in members:
        st.write(m)

# SHARES
elif menu == "Hisa":

    st.header("Ununuzi wa Hisa")

    name = st.text_input("Jina la Mwanachama")

    shares = st.number_input(
    "Idadi ya Hisa",
    min_value=1,
    max_value=20
    )

    if st.button("Hifadhi"):

        amount = shares * 5000

        st.success(
        f"Hisa {shares} zimehifadhiwa. Jumla TSh {amount}"
        )

# LOANS
elif menu == "Mikopo":

    st.header("Maombi ya Mkopo")

    member = st.text_input("Jina la Mwanachama")

    amount = st.number_input("Kiasi cha Mkopo")

    months = st.slider(
    "Muda wa Mkopo (Miezi)",
    1,
    4
    )

    if st.button("Hesabu Mkopo"):

        interest = amount * 0.05 * months
        insurance = amount * 0.02
        total = amount + interest

        st.write("Riba:", interest)
        st.write("Bima:", insurance)
        st.write("Jumla ya Marejesho:", total)

# SOCIAL FUND
elif menu == "Mfuko wa Jamii":

    st.header("Michango ya Mfuko wa Jamii")

    name = st.text_input("Jina la Mwanachama")

    if st.button("Rekodi Mchango"):

        st.success("TSh 1000 imehifadhiwa")

# REPORTS
elif menu == "Ripoti":

    st.header("Ripoti za Kikundi")

    st.write("Ripoti zitaonekana hapa")
