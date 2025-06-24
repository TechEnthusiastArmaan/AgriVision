# from pathlib import Path
# import pandas as pd
# import joblib
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split

# # Correct relative path
# data_path = Path(__file__).parent / "resources" / "data" / "Extended_Fruits_Dataset2.csv"
# data = pd.read_csv(data_path)

# x = data.iloc[:, :-1].values
# y = data.iloc[:, -1].values

# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier(n_estimators=500, max_depth=5, random_state=42)
# model.fit(x_train, y_train)

# # Save the model in the same data folder
# model_output = Path(__file__).parent / "resources" / "data" / "fruit_model.pkl"
# joblib.dump(model, model_output)
# print("Model saved to:", model_output)
# # Evaluate the model
# accuracy = model.score(x_test, y_test)
# print(f"Model accuracy: {accuracy * 100:.2f}%")

from pathlib import Path
import pandas as pd
import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

# Correct relative path
data_path = Path(__file__).parent / "resources" / "data" / "Extended_Fruits_Dataset2.csv"
data = pd.read_csv(data_path)

# Split dataset into features and labels
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize and train LightGBM model
model = LGBMClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
model.fit(x_train, y_train)

# Save the model
model_output = Path(__file__).parent / "resources" / "data" / "fruit_model.pkl"
joblib.dump(model, model_output)
print("✅ Model saved to:", model_output)

# Evaluate model accuracy
accuracy = model.score(x_test, y_test)
print(f"📊 Model accuracy: {accuracy * 100:.2f}%")
