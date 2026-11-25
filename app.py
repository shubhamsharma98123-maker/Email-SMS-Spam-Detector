import pandas as pd
df = pd.read_csv("data.csv",encoding="latin-1")
print(df.head)

import pandas as pd
df = pd.read_csv("email.csv",encoding="latin-1")
print(df.head)

import re
import joblib
import streamlit as st

import joblib

model = joblib.load("spam_classifier_pipeline.pkl")


# Load the saved ML pipeline from Desktop
model = joblib.load(
    r"C:\Users\Shubham\OneDrive\Desktop\spam_classifier_pipeline.pkl"
)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " url ", text)
    text = re.sub(r"\d+", " num ", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Page UI setup
st.set_page_config(page_title="Email Spam Detector", page_icon="📧")
st.title("📧 Email & SMS Spam Detector")
st.write(
    "Paste an email or message below to check whether it is *Spam* or *Legitimate (Ham)*."
)

# User input box
user_input = st.text_area(
    "Enter Email Content:",
    height=150,
    placeholder="Congratulations! You've won a free iPhone...",
)

if st.button("Analyze Email"):
    if user_input.strip() == "":
        st.warning("Please enter some text first.")
    else:
        cleaned = clean_text(user_input)
        prediction = model.predict([cleaned])[0]
        probabilities = model.predict_proba([cleaned])[0]

        ham_prob = float(probabilities[0]) * 100
        spam_prob = float(probabilities[1]) * 100

        if prediction == 1:
            st.error(f"🚨 *SPAM DETECTED* (Confidence: {spam_prob:.2f}%)")
        else:
            st.success(
                f"✅ *NOT SPAM (Legitimate)* (Confidence: {ham_prob:.2f}%)"
            )




