import streamlit as st

st.title("Mfumo wa Kikundi cha Huduma Ndogo ya Fedha")

st.header("Karibu kwenye Mfumo wa Kikundi")

st.write("Huu ni mfumo wa kusimamia:")
st.write("- Wanachama")
st.write("- Hisa")
st.write("- Mikopo")
st.write("- Michango ya Jamii")
st.write("- Ripoti za Kikundi")

st.subheader("Dashboard")

st.metric("Wanachama", 17)
st.metric("Mfuko wa Hisa", "TSh 0")
st.metric("Mfuko wa Jamii", "TSh 0")

st.success("Mfumo umeanza kufanya kazi!")
