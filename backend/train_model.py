import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import resample

# Load datasets
fake_df = pd.read_csv("datasets/Fake.csv")
true_df = pd.read_csv("datasets/True.csv")

# Labels
fake_df["label"] = 0
true_df["label"] = 1

# Combine
df = pd.concat([fake_df, true_df], ignore_index=True)

# Balance dataset
fake = df[df.label == 0]
real = df[df.label == 1]

fake_downsampled = resample(
    fake,
    replace=False,
    n_samples=len(real),
    random_state=42
)

df = pd.concat([fake_downsampled, real])

# Shuffle
df = df.sample(frac=1, random_state=42)

# Clean
df["text"] = df["text"].astype(str)

# Features
X = df["text"]
y = df["label"]

# Vectorizer (IMPROVED)
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.7,
    ngram_range=(1, 2),
    min_df=5
)

X_vectorized = vectorizer.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

# Model (BEST FOR TEXT)
model = MultinomialNB()
model.fit(X_train, y_train)

# Accuracy check
print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))

# Save
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model + Vectorizer saved")