import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# 1) Data load
df = pd.read_csv("app/data/dataset.csv")

# 2) Features (input) aur target (output)
X = df[["distance", "traffic"]]
y = df["delay"]

# 3) Model banana aur train karna
model = DecisionTreeClassifier()
model.fit(X, y)

# 4) Model save karna
joblib.dump(model, "app/data/model/model.pkl")

print("Model trained & saved successfully ✅")