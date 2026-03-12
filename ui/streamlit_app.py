import streamlit as st
import requests

BASE_URL = "http://localhost:8000/api"

st.title("Agent Marketplace")

tab1, tab2 = st.tabs(["Agent Directory", "Send Task"])

with tab1:

    st.header("Registered Agents")

    res = requests.get(f"{BASE_URL}/agents/list")
    agents = res.json()

    for a in agents:
        st.write(f"### {a['name']}")
        st.write(a["description"])
        st.write("Capabilities:", a["capabilities"])


with tab2:

    st.header("Send Task")

    capability = st.selectbox(
        "Select capability",
        ["math", "summarization", "search"]
    )

    text = st.text_area("Task input")

    if st.button("Send"):

        res = requests.post(
            f"{BASE_URL}/task",
            json={
                "capability": capability,
                "input": text
            }
        )


        st.json(res.json())