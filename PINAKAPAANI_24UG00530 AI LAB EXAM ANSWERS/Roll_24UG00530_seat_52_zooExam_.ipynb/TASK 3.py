import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint

class OmegaAI:
    def __init__(self):
        self.df = None
        self.engineered_features = ["total_legs_tail", "is_aquatic_predator"]

    def load_merge_clean(self):
        roll_no = "24UG00530"
        seat_no = 52
        zoo = pd.read_csv("zoo.csv")
        class_df = pd.read_csv("class.csv")
        with open("auxiliary_metadata.json.txt", "r") as f:
            aux_data = json.load(f)
        aux_df = pd.DataFrame(aux_data)
        zoo["class_type"] = pd.to_numeric(zoo["class_type"], errors="coerce").astype("Int64")
        class_df["Class_Type"] = pd.to_numeric(class_df["Class_Type"], errors="coerce").astype("Int64")
        class_df = class_df.dropna(subset=["Class_Type"])
        class_df["Class_Type"] = class_df["Class_Type"].astype("Int64")
        merged = pd.merge(zoo, class_df, left_on="class_type", right_on="Class_Type", how="left")
        if roll_no[-1] == "0":
            merged["animal_name"] = merged["animal_name"].str.upper()
        for item in aux_data:
            if "conversation_sataus" in item:
                item["conversation_status"] = item.pop("conversation_sataus")
            if "conversation" in item:
                item["conversation_status"] = item.pop("conversation")
            if "status" in item:
                item["conversation_status"] = item.pop("status")
            if "habitas" in item:
                item["habitat_type"] = item.pop("habitas")
            if "habitat" in item:
                item["habitat_type"] = item.pop("habitat")
            if "diet_type" in item:
                item["diet"] = item.pop("diet_type")
            if "diet" in item:
                item["diet"] = item["diet"]
        aux_df = pd.DataFrame(aux_data)
        merged = pd.merge(merged, aux_df, on="animal_name", how="left")
        second_last_digit = int(roll_no[-2])
        if second_last_digit % 2 == 0:
            merged = merged.dropna(subset=["diet","habitat_type","conversation_status"])
            for col in merged.select_dtypes(include="object"):
                merged[col].fillna("unknown", inplace=True)
            for col in merged.select_dtypes(include=[np.number]):
                merged[col].fillna(merged[col].median(), inplace=True)
        if seat_no == 52:
            merged["total_legs_tail"] = merged["legs"] + merged["tail"]
            merged["is_aquatic_predator"] = merged["aquatic"] & merged["predator"]
        self.df = merged

class OmegaAI_Model:
    def __init__(self, df, target_column="class_type", engineered_features=None):
        self.df = df.copy()
        self.target_column = target_column
        if engineered_features is None:
            self.engineered_features = ["total_legs_tail","is_aquatic_predator"]
        else:
            self.engineered_features = engineered_features

    def prefix_train_and_evalute(self):
        X = self.df.drop(columns=[self.target_column])
        y = self.df[self.target_column]

        num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        eng_cols = [f for f in self.engineered_features if f in X.columns]
        X_numeric = X[num_cols + eng_cols]

        cat_cols = X.select_dtypes(include=["object","category"]).columns
        if len(cat_cols) > 0:
            X_encoded = pd.get_dummies(X_numeric.join(X[cat_cols]), drop_first=True)
        else:
            X_encoded = X_numeric.copy()

        X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=789)

        rf = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=5, random_state=789)
        rf.fit(X_train, y_train)
        train_acc = rf.score(X_train, y_train)
        test_acc = rf.score(X_test, y_test)
        print(f"Training accuracy: {train_acc:.4f}")
        print(f"Testing accuracy: {test_acc:.4f}")
        print(f"Overfitting gap: {train_acc - test_acc:.4f}")

        y_pred = rf.predict(X_test)
        cls_report = classification_report(y_test, y_pred, output_dict=True)
        print("\nClassification Report:\n")
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8,6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y), yticklabels=np.unique(y))
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title("Random Forest Confusion Matrix")
        plt.show()

        importances = rf.feature_importances_
        feature_df = pd.DataFrame({"feature": X_encoded.columns, "importance": importances})
        top_features = feature_df.sort_values(by="importance", ascending=False).head(12)
        plt.figure(figsize=(10,6))
        colors = ["orange" if f in self.engineered_features else "skyblue" for f in top_features["feature"]]
        plt.barh(top_features["feature"][::-1], top_features["importance"][::-1], color=colors)
        plt.xlabel("Importance")
        plt.title("Top 12 Feature Importances (Orange = Engineered Features)")
        plt.show()

        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)
        knn_acc = knn.score(X_test, y_test)
        print(f"KNN Test Accuracy: {knn_acc:.4f}")

        top_feature = top_features.iloc[0]["feature"]
        top_value = top_features.iloc[0]["importance"]
        f1_scores = {cls: cls_report[cls]["f1-score"] for cls in cls_report if cls not in ["accuracy","macro avg","weighted avg"]}
        best_class = max(f1_scores, key=f1_scores.get)
        worst_class = min(f1_scores, key=f1_scores.get)
        eng_feature_rank = None
        eng_feature_name = None
        for ef in self.engineered_features:
            if ef in top_features["feature"].values:
                eng_feature_rank = top_features[top_features["feature"] == ef].index[0] + 1
                eng_feature_name = ef
                break

        pprint("\n== Model Analysis ==")
        print(f"1. Most important feature: {top_feature} (importance: {top_value:.3f})")
        print(f"2. Worst performing class: {worst_class} (F1: {f1_scores[worst_class]:.3f})")
        print(f"3. Best performing class: {best_class} (F1: {f1_scores[best_class]:.3f})")
        if eng_feature_rank:
            print(f"4. Engineered feature '{eng_feature_name}' ranked: {eng_feature_rank}")
        print(f"5. Model comparison: KNN={knn_acc:.3f} vs RF={test_acc:.3f}")

if __name__ == "__main__":
    omega_obj = OmegaAI()
    omega_obj.load_merge_clean()
    merged_df = omega_obj.df
    model_obj = OmegaAI_Model(merged_df, target_column="class_type")
    model_obj.prefix_train_and_evalute()
