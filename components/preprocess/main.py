import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedKFold


def run(src_csv_path: str, n_splits: int, dataset_uri: str) -> None:
    df = pd.read_csv(src_csv_path)
    print(f"Load CSV from: {src_csv_path}")

    df["target"] = df["category"].map({"cs.CV": 0, "cs.CL": 1, "cs.RO": 2})

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    idx_train, idx_val = next(cv.split(df, df["target"]))
    df_train = df.iloc[idx_train]
    df_val = df.iloc[idx_val]

    dataset_dir = Path(dataset_uri)
    dataset_dir.mkdir(parents=True, exist_ok=True)
    df_train.to_csv(dataset_dir / "train.csv", index=False)
    df_val.to_csv(dataset_dir / "val.csv", index=False)
    print(f"Save train/val data in: {dataset_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess")
    parser.add_argument("--src-csv-path", type=str)
    parser.add_argument("--n-splits", type=int)
    parser.add_argument("--dataset-uri", type=str)
    args = parser.parse_args()

    run(**vars(args))