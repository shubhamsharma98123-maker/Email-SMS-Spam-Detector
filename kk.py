import pandas as pd
df = pd.read_csv("data.csv",encoding="latin-1")
print(df.head)

import pandas as pd
df = pd.read_csv("email.csv",encoding="latin-1")
print(df.head)

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# 1. Load the dataset
df = pd.read_csv("data.csv", encoding="latin-1")

# Keep only the two useful columns and rename them
# (Change 'v1' and 'v2' if your columns have different names)
df = df[["v1", "v2"]]
df.columns = ["label", "message"]

# 2. Convert labels to numbers (ham = 0, spam = 1)
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Drop any empty rows just in case
df.dropna(inplace=True)

# 3. Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["label"], test_size=0.2, random_state=42
)

# 4. Convert text words into numbers (Bag of Words)
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# 5. Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_counts, y_train)

# 6. Check accuracy
predictions = model.predict(X_test_counts)
print("Model Accuracy:", accuracy_score(y_test, predictions))

# 7. Test with your own custom email
my_email = ["Congratulations! You won a free $1000 gift card. Click here now!"]
my_email_counts = vectorizer.transform(my_email)
result = model.predict(my_email_counts)

print("Prediction:", "SPAM" if result[0] == 1 else "NOT SPAM")
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# 1. Load the dataset (update filename if needed)
df = pd.read_csv("data.csv", encoding="latin-1")

# Print columns to verify their exact names
print("Columns found:", df.columns.tolist())

# Keep only the first two columns automatically, regardless of their names
df = df.iloc[:, :2]
df.columns = ["label", "message"]

# 2. Convert labels to lowercase, strip spaces, and map to numbers
df["label"] = (
    df["label"].astype(str).str.strip().str.lower().map({"ham": 0, "spam": 1})
)
df.dropna(inplace=True)

# 3. Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["label"], test_size=0.2, random_state=42
)

# 4. Convert text words into numbers (Bag of Words)
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# 5. Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_counts, y_train)

# 6. Check accuracy
predictions = model.predict(X_test_counts)
print("Model Accuracy:", accuracy_score(y_test, predictions))

# 7. Test with your own custom email
my_email = ["Congratulations! You won a free $1000 gift card. Click here now!"]
my_email_counts = vectorizer.transform(my_email)
result = model.predict(my_email_counts)

print("Prediction:", "SPAM" if result[0] == 1 else "NOT SPAM")

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# 1. Load the dataset (update filename if needed)
df = pd.read_csv("data.csv", encoding="latin-1")

# Print columns to verify their exact names
print("Columns found:", df.columns.tolist())

# Keep only the first two columns automatically, regardless of their names
df = df.iloc[:, :2]
df.columns = ["label", "message"]

# 2. Convert labels to lowercase, strip spaces, and map to numbers
df["label"] = (
    df["label"].astype(str).str.strip().str.lower().map({"ham": 0, "spam": 1})
)
df.dropna(inplace=True)

# 3. Split data into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["label"], test_size=0.2, random_state=42
)

# 4. Convert text words into numbers (Bag of Words)
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# 5. Train the Naive Bayes model
model = MultinomialNB()
model.fit(X_train_counts, y_train)

# 6. Check accuracy
predictions = model.predict(X_test_counts)
print("Model Accuracy:", accuracy_score(y_test, predictions))

# 7. Test with your own custom email
my_email = ["Congratulations! You won a free $1000 gift card. Click here now!"]
my_email_counts = vectorizer.transform(my_email)
result = model.predict(my_email_counts)

print("Prediction:", "SPAM" if result[0] == 1 else "NOT SPAM")

import re
import joblib
import streamlit as st

model = joblib.load("spam_classifier_pipeline.pkl")


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " url ", text)
    text = re.sub(r"\d+", " num ", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


st.set_page_config(page_title="Email Spam Detector", page_icon="📧")
st.title("📧 Email & SMS Spam Detector")
st.write(
    "Paste an email or message below to check whether it is **Spam** or **Legitimate (Ham)**."
)

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

        ham_prob = probabilities[0] * 100
        spam_prob = probabilities[1] * 100

        if prediction == 1:
            st.error(f"🚨 **SPAM DETECTED** (Confidence: {spam_prob:.2f}%)")
        else:
            st.success(
                f"✅ **NOT SPAM (Legitimate)** (Confidence: {ham_prob:.2f}%)"
            )
