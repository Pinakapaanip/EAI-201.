import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

df = pd.read_csv(r"C:\Users\LUCKY\OneDrive\Desktop\Y31\Documents\Desktop\cleaned_fifa_dataset.csv")

possible_targets = ['Winner', 'Winning_Team', 'Team', 'Result', 'Label', 'Outcome', 'target']
target_col = None
for col in df.columns:
    if col.strip() in possible_targets:
        target_col = col
        break

if target_col is None:
    raise ValueError(f"Target column not found. Columns: {list(df.columns)}")

le = LabelEncoder()
df[target_col] = le.fit_transform(df[target_col])
for col in df.columns:
    if df[col].dtype == 'object' and col != target_col:
        df[col] = le.fit_transform(df[col])

X = df.drop(target_col, axis=1)
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_reg = LogisticRegression(max_iter=5000)
log_reg.fit(X_train_scaled, y_train)
y_pred_lr = log_reg.predict(X_test_scaled)
predicted_team_lr = le.inverse_transform([y_pred_lr[0]])[0]
accuracy_lr = accuracy_score(y_test, y_pred_lr)

print("Logistic Regression predicts the winner:", predicted_team_lr)
print("Accuracy:", round(accuracy_lr, 3))
print(classification_report(y_test, y_pred_lr))

param_grid = {'n_estimators': [100], 'max_depth': [15], 'min_samples_split': [2]}
rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(rf, param_grid, cv=5)
grid_search.fit(X_train, y_train)

best_rf = grid_search.best_estimator_
y_pred_rf = best_rf.predict(X_test)
predicted_team_rf = le.inverse_transform([y_pred_rf[0]])[0]
accuracy_rf = accuracy_score(y_test, y_pred_rf)

print("Random Forest predicts the winner:", predicted_team_rf)
print("Best Parameters:", grid_search.best_params_)
print("Accuracy:", round(accuracy_rf, 3))
print(classification_report(y_test, y_pred_rf))

importances = best_rf.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(10, 6))
sns.barplot(x=importances[indices], y=X.columns[indices])
plt.title("Feature Importance in Random Forest")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.tight_layout()
plt.show()

cm = confusion_matrix(y_test, y_pred_rf)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", cbar=False)
plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

comparison_df = pd.DataFrame({'Actual': y_test.values, 'Predicted': y_pred_rf})
plt.figure(figsize=(10, 5))
sns.countplot(data=comparison_df, x='Actual', hue='Predicted')
plt.title("Actual vs Predicted Team Outcomes")
plt.xlabel("Team (Actual)")
plt.ylabel("Count")
plt.legend(title='Predicted')
plt.tight_layout()
plt.show()
