import re
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " url ", text)
    text = re.sub(r"\d+", " num ", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Load dataset (keep data.csv on your Desktop)
df = pd.read_csv(
    r"C:\Users\Shubham\OneDrive\Desktop\data.csv", encoding="latin-1"
)
df = df.iloc[:, :2]
df.columns = ["label", "message"]

df["label"] = (
    df["label"].astype(str).str.strip().str.lower().map({"ham": 0, "spam": 1})
)
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df["clean_message"] = df["message"].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df["clean_message"],
    df["label"],
    test_size=0.2,
    random_state=42,
    stratify=df["label"],
)

models = {
    "Naive Bayes": MultinomialNB(alpha=0.1),
    "Logistic Regression": LogisticRegression(
        max_iter=1000, class_weight="balanced"
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, random_state=42, n_jobs=-1
    ),
}

best_pipeline = None
best_f1 = 0

for name, clf in models.items():
    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                stop_words="english", ngram_range=(1, 2), max_features=5000
            ),
        ),
        ("classifier", clf),
    ])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    f1 = f1_score(y_test, preds)
    print(f"{name} -> F1-Score: {f1:.4f}")

    if f1 > best_f1:
        best_f1 = f1
        best_pipeline = pipeline

# Save the file directly to your Desktop
save_path = r"C:\Users\Shubham\OneDrive\Desktop\spam_classifier_pipeline.pkl"
joblib.dump(best_pipeline, save_path)
print("SUCCESS! Model saved to:", save_path)
