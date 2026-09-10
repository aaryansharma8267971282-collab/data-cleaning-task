import os
import pandas as pd


# ==========================================
# DATA CLEANING TASK
# ==========================================

print("=" * 60)
print("        WEBSITE TRAFFIC DATA CLEANING")
print("=" * 60)


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "website_traffic.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "cleaned_website_traffic.csv"
)


# Create outputs folder if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# 2. LOAD DATASET
# ==========================================

print("\n1. Loading dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully.")


# ==========================================
# 3. DISPLAY ORIGINAL DATA INFORMATION
# ==========================================

print("\n2. Original Dataset Information")
print("-" * 40)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# 4. REMOVE EMPTY ROWS
# ==========================================

print("\n3. Removing empty rows...")

df.dropna(how="all", inplace=True)

print("Empty rows removed.")


# ==========================================
# 5. REMOVE DUPLICATE ROWS
# ==========================================

print("\n4. Checking duplicate rows...")

duplicate_count = df.duplicated().sum()

print("Duplicate rows found:", duplicate_count)

df.drop_duplicates(inplace=True)

print("Duplicate rows removed.")


# ==========================================
# 6. CLEAN COLUMN NAMES
# ==========================================

print("\n5. Cleaning column names...")

df.columns = df.columns.str.strip()

print("Column names cleaned.")


# ==========================================
# 7. CLEAN TEXT DATA
# ==========================================

print("\n6. Cleaning text columns...")

text_columns = [
    "Source",
    "Page"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

print("Text data cleaned.")


# ==========================================
# 8. CONVERT DATE COLUMN
# ==========================================

print("\n7. Converting Date column...")

if "Date" in df.columns:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

print("Date column converted.")


# ==========================================
# 9. CONVERT NUMERIC COLUMNS
# ==========================================

print("\n8. Converting numeric columns...")

numeric_columns = [
    "Visitors",
    "PageViews",
    "Conversions",
    "BounceRate",
    "SessionDuration"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

print("Numeric columns converted.")


# ==========================================
# 10. CHECK MISSING VALUES
# ==========================================

print("\n9. Missing values before cleaning")
print("-" * 40)

print(df.isnull().sum())


# ==========================================
# 11. HANDLE MISSING NUMERIC VALUES
# ==========================================

print("\n10. Handling missing numeric values...")

for column in numeric_columns:

    if column in df.columns:

        if df[column].isnull().any():

            df[column] = df[column].fillna(
                df[column].median()
            )

print("Missing numeric values handled.")


# ==========================================
# 12. HANDLE MISSING TEXT VALUES
# ==========================================

print("\n11. Handling missing text values...")

for column in text_columns:

    if column in df.columns:

        df[column] = df[column].fillna(
            "Unknown"
        )

print("Missing text values handled.")


# ==========================================
# 13. HANDLE INVALID DATE VALUES
# ==========================================

print("\n12. Removing invalid dates...")

if "Date" in df.columns:

    df.dropna(
        subset=["Date"],
        inplace=True
    )

print("Invalid dates removed.")


# ==========================================
# 14. REMOVE INVALID NUMERIC VALUES
# ==========================================

print("\n13. Checking invalid numeric values...")


if "Visitors" in df.columns:

    df = df[df["Visitors"] >= 0]


if "PageViews" in df.columns:

    df = df[df["PageViews"] >= 0]


if "Conversions" in df.columns:

    df = df[df["Conversions"] >= 0]


if "BounceRate" in df.columns:

    df = df[
        (df["BounceRate"] >= 0)
        &
        (df["BounceRate"] <= 100)
    ]


if "SessionDuration" in df.columns:

    df = df[
        df["SessionDuration"] >= 0
    ]


print("Invalid numeric values removed.")


# ==========================================
# 15. CHECK CONVERSION LOGIC
# ==========================================

print("\n14. Checking conversion consistency...")

if (
    "Conversions" in df.columns
    and
    "Visitors" in df.columns
):

    df = df[
        df["Conversions"]
        <=
        df["Visitors"]
    ]

print("Conversion consistency checked.")


# ==========================================
# 16. SORT DATA BY DATE
# ==========================================

print("\n15. Sorting data by date...")

if "Date" in df.columns:

    df.sort_values(
        by="Date",
        inplace=True
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

print("Data sorted successfully.")


# ==========================================
# 17. FINAL MISSING VALUE CHECK
# ==========================================

print("\n16. Missing values after cleaning")
print("-" * 40)

print(df.isnull().sum())


# ==========================================
# 18. FINAL DATASET SIZE
# ==========================================

print("\n17. Final Dataset Information")
print("-" * 40)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# 19. SAVE CLEANED DATA
# ==========================================

print("\n18. Saving cleaned dataset...")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nCleaned dataset saved successfully!")

print("\nOutput file:")
print(OUTPUT_FILE)


# ==========================================
# 20. COMPLETION MESSAGE
# ==========================================

print("\n" + "=" * 60)
print("       DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)