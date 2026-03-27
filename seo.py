# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json

# ใส่ API KEY
genai.configure(api_key="YOUR_API_KEY")

st.title("🚀 SEO AI TOOL (มือถือ)")

def analyze_seo(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else "No title"

        meta = soup.find("meta", attrs={"name": "description"})
        desc = meta["content"] if meta else "No description"

        h1 = [h.text for h in soup.find_all("h1")]

        content = soup.get_text()[:2000]

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Analyze SEO:

        Title: {title}
        Description: {desc}
        H1: {h1}
        Content: {content}

        Return JSON:
        {{
          "score": "",
          "issues": [],
          "better_title": "",
          "better_description": "",
          "keywords": []
        }}
        """

        response = model.generate_content(prompt)

        return title, desc, h1, response.text

    except Exception as e:
        return None, None, None, str(e)

url = st.text_input("ใส่ URL", "https://example.com")

if st.button("วิเคราะห์ SEO"):
    title, desc, h1, ai = analyze_seo(url)

    if title is None:
        st.error(ai)
    else:
        st.success("เสร็จแล้ว!")

        st.write("📌 Title:", title)
        st.write("📝 Description:", desc)
        st.write("🔎 H1:", h1)

        try:
            data = json.loads(ai)
            st.metric("SEO Score", data["score"])
            st.write("❗ Issues:", data["issues"])
            st.write("✨ Title ใหม่:", data["better_title"])
            st.write("📝 Description ใหม่:", data["better_description"])
            st.write("🔑 Keywords:", data["keywords"])
        except:
            st.code(ai)
