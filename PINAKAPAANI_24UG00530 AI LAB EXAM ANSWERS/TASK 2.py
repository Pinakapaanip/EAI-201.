import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class OmegaAI_EDA:
    def __init__(self, file_path="TASK1_merged.csv"):
        self.data = pd.read_csv(file_path)
        # Strip spaces from column names and lowercase them for consistency
        self.data.columns = self.data.columns.str.strip()

    def Omega_edaand_cleaning(self):
        seat_no = 52
        roll_no = "24UG00530"
        data = self.data.copy()

        print("\n--- TASK 2: EXPLORATORY DATA ANALYSIS ---\n")

        # Standardize column names for plotting
        col_class = None
        col_conversation = None
        col_leg = None
        col_catsize = None

        for col in data.columns:
            if col.lower() == "class_type":
                col_class = col
            if col.lower() == "conversation_status":
                col_conversation = col
            if col.lower() == "legs":
                col_leg = col
            if col.lower() == "catsize":
                col_catsize = col

        if seat_no == 52:
            # 1) Bar plot with error bars for class counts
            if col_class:
                plt.figure(figsize=(8,5))
                sns.countplot(x=col_class, data=data, palette="viridis")
                plt.title("Class Counts with Error Bars")
                plt.show()
            else:
                print("Warning: Class_Type column not found for bar plot.")

            # 2) Hexbin plot for two continuous features
            if col_leg and col_catsize and col_class:
                plt.figure(figsize=(8,6))
                for cls in sorted(data[col_class].dropna().unique()):
                    subset = data[data[col_class] == cls]
                    plt.hexbin(subset[col_leg], subset[col_catsize], gridsize=20, cmap='Blues', alpha=0.5)
                plt.xlabel('Legs')
                plt.ylabel('Catsize')
                plt.title("Hexbin Plot of Legs vs Catsize by Class")
                plt.show()
            else:
                print("Warning: Required columns for hexbin plot not found.")

            # 3) Swarm plot for conversation_status
            if col_conversation and col_class:
                plt.figure(figsize=(10,6))
                sns.swarmplot(x=col_class, y=col_conversation, data=data)
                plt.title("Swarm Plot: Conversation Status Across Classes")
                plt.show()
            else:
                print("Warning: Required columns for swarm plot not found.")

            # 4) Clustermap for all numeric features
            numeric_cols = data.select_dtypes(include=np.number)
            if not numeric_cols.empty:
                sns.clustermap(numeric_cols.corr(), cmap="coolwarm", annot=True)
                plt.title("Cluster Map of Numerical Features Correlation")
                plt.show()
            else:
                print("Warning: No numeric columns for clustermap.")

        # ------------------ B) Statistical Analysis ------------------
        print("\nPerforming statistical analysis...\n")
        if col_class:
            class_counts = data[col_class].value_counts()
            imbalance_ratio = class_counts.max() / class_counts.min()
            print(f"Class imbalance ratio (largest/smallest): {imbalance_ratio:.2f}")
            print("Class counts:\n", class_counts)
        else:
            print("Class_Type column not found; skipping class stats.")
            class_counts = pd.Series()
            imbalance_ratio = None

        # Low variance features
        numeric_cols = data.select_dtypes(include=np.number)
        low_variance_features = numeric_cols.var()[numeric_cols.var() < 0.01].index.tolist()
        print("Low variance features (<0.01):", low_variance_features)

        # Highly correlated pairs
        corr_matrix = numeric_cols.corr().abs()
        high_corr_pairs = [(i,j) for i in corr_matrix.columns for j in corr_matrix.columns 
                           if i != j and corr_matrix.loc[i,j] > 0.8]
        print("Highly correlated pairs (|corr| > 0.8):", high_corr_pairs)

        # ------------------ C) Markdown-style Answers ------------------
        print("\n--- Markdown-style Answers ---\n")
        roll_last2 = int(roll_no[-2:])
        print(f"Based on last 2 digits of roll number ({roll_last2}):\n")
        if imbalance_ratio is not None:
            print(f"*Class imbalance:* largest = {class_counts.max()}, smallest = {class_counts.min()}, ratio = {imbalance_ratio:.2f}")
        print(f"*Low variance features:* {low_variance_features}")
        print(f"*Highly correlated feature pairs:* {high_corr_pairs}")
        print("*Evidence:* Refer to bar plot, hexbin plot, swarm plot, and clustermap visualizations above.")

# ------------------ Run Task 2 ------------------
eda_obj = OmegaAI_EDA()
eda_obj.Omega_edaand_cleaning()
