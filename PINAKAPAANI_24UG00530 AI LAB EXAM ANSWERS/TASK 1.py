import os
import pandas as pd
import json
import numpy as np

class OmegaAI:
    def Omega_load_and_integreate(self):
        print("=== DEBUG OUTPUT START ===")
        print("Current Working Directory:", os.getcwd())
        print("Files in Folder:", os.listdir())

        # -------------------------
        # Load datasets
        # -------------------------
        zoo = pd.read_csv("zoo.csv", encoding="utf-8")
        class_df = pd.read_csv("class.csv", encoding="utf-8")

        # Load auxiliary JSON
        with open("auxiliary_metadata.json.txt", "r") as f:
            aux_data = json.load(f)

        print("\nDataset shapes:")
        print("Zoo:", zoo.shape)
        print("Class:", class_df.shape)

        print("\nMissing values in Zoo dataset:")
        print(zoo.isnull().sum())

        print("\nDuplicate rows in Zoo dataset:", zoo.duplicated().sum())

        print("\nFirst 3 rows of Zoo:")
        print(zoo.head(3))

        # -------------------------
        # Fix Class_Type for merge (bulletproof)
        # -------------------------
        zoo["class_type"] = pd.to_numeric(zoo["class_type"], errors="coerce").astype("Int64")

        class_df["Class_Type"] = pd.to_numeric(class_df["Class_Type"], errors="coerce").astype("Int64")
        class_df = class_df.dropna(subset=["Class_Type"])
        class_df["Class_Type"] = class_df["Class_Type"].astype("Int64")

        print("\nMerging Zoo + Class on 'class_type' ...")
        try:
            merged = pd.merge(
                zoo,
                class_df,
                left_on="class_type",
                right_on="Class_Type",
                how="left"
            )
            print("Merge successful!")
        except Exception as e:
            print("MERGE ERROR:", e)
            return

        # -------------------------
        # Task B: Roll number last digit = 0 → uppercase animal names
        # -------------------------
        roll_no = "24UG00530"
        if roll_no[-1] == "0":
            merged["animal_name"] = merged["animal_name"].str.upper()

        # -------------------------
        # Task C: Fix JSON inconsistencies
        # -------------------------
        for item in aux_data:
            # conversation_status
            if "conversation_sataus" in item:
                item["conversation_status"] = item.pop("conversation_sataus")
            if "conversation" in item:
                item["conversation_status"] = item.pop("conversation")
            if "status" in item:
                item["conversation_status"] = item.pop("status")
            # habitat
            if "habitas" in item:
                item["habitat_type"] = item.pop("habitas")
            if "habitat" in item:
                item["habitat_type"] = item.pop("habitat")
            # diet
            if "diet_type" in item:
                item["diet"] = item.pop("diet_type")
            if "diet" in item:
                item["diet"] = item["diet"]
            # Additional typo fixes can be added here

        aux_df = pd.DataFrame(aux_data)

        # -------------------------
        # Task D: Merge on animal_name
        # -------------------------
        merged = pd.merge(
            merged,
            aux_df,
            left_on="animal_name",
            right_on="animal_name",
            how="left"
        )

        # -------------------------
        # Task E: Handle missing values based on roll number second-to-last digit
        # -------------------------
        second_last_digit = roll_no[-2]
        if second_last_digit.isdigit():
            second_last_digit = int(second_last_digit)
            if second_last_digit % 2 == 0:
                # Drop rows with missing aux data
                merged = merged.dropna(subset=["diet", "habitat_type", "conversation_status"])
                # Fill remaining missing values
                for col in merged.select_dtypes(include=["object"]).columns:
                    merged[col].fillna("unknown", inplace=True)
                for col in merged.select_dtypes(include=[np.number]).columns:
                    merged[col].fillna(merged[col].median(), inplace=True)

        # -------------------------
        # Task F: Seat number = 52 → create 2 custom biological features
        # -------------------------
        seat_no = 52
        if seat_no == 52:
            # Feature 1: total_legs_tail = legs + tail
            merged["total_legs_tail"] = merged["legs"] + merged["tail"]
            # Feature 2: is_aquatic_predator = aquatic AND predator
            merged["is_aquatic_predator"] = merged["aquatic"] & merged["predator"]

        # -------------------------
        # Task G: Print outputs
        # -------------------------
        print(f"\nDataset shape: {merged.shape}")
        print(f"Missing values: {merged.isnull().sum().sum()}")
        print(f"Duplicate rows: {merged.duplicated().sum()}")
        print("\nFirst 3 rows:")
        print(merged.head(3))

        engineered_features = ["total_legs_tail", "is_aquatic_predator"]
        print(f"\nEngineered features: {engineered_features}")


# -------------------------
# Run the method
# -------------------------
obj = OmegaAI()
obj.Omega_load_and_integreate()
