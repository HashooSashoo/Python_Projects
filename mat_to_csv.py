"""
mat_to_csv.py

Converts three .mat files to CSVs, inserts a label column (A/B/C) between
the 2nd and 3rd columns of each, then interleaves them in chunks of 4 rows:
4 from file 1 (A), 4 from file 2 (B), 4 from file 3 (C), repeat.

Requirements:
    pip install scipy numpy pandas
"""

import numpy as np
import pandas as pd
from scipy.io import loadmat

# ── CONFIG ────────────────────────────────────────────────────────────────────
INPUT_MAT_A  = "/Users/ZHash/Downloads/P804 Code 9 XYZ _ Fiber 1 MidCostal.mat"   # <-- rows with 7,8,9,10
INPUT_MAT_B  = "/Users/ZHash/Downloads/P804 Code 9 XYZ _ Fiber 2 MidCostal.mat"   # <-- rows with 11,12,13,14
INPUT_MAT_C  = "/Users/ZHash/Downloads/P804 Code 9 XYZ _ Fiber 3 MidCostal.mat"   # <-- rows with 15,16,17,18
OUTPUT_CSV   = "output.csv"
# ─────────────────────────────────────────────────────────────────────────────


def load_mat_as_dataframe(path: str) -> pd.DataFrame:
    """Load a .mat file and return its primary numeric array as a DataFrame."""
    try:
        mat = loadmat(path)
    except NotImplementedError:
        try:
            import h5py
        except ImportError:
            raise ImportError(
                "This .mat file is v7.3 (HDF5 format). "
                "Install h5py to read it:  pip install h5py"
            )
        with h5py.File(path, "r") as f:
            keys = [k for k in f.keys() if not k.startswith("#")]
            if not keys:
                raise ValueError("No data variables found in the .mat file.")
            key = keys[0]
            print(f"  Using variable: '{key}'")
            data = np.array(f[key]).T
        return pd.DataFrame(data)

    data_keys = [k for k in mat.keys() if not k.startswith("__")]
    if not data_keys:
        raise ValueError("No data variables found in the .mat file.")

    key = data_keys[0]
    print(f"  Using variable: '{key}'")
    return pd.DataFrame(mat[key])


def insert_label_column(df: pd.DataFrame, label: str, position: int = 2) -> pd.DataFrame:
    """Insert a column of `label` at `position` (0-indexed)."""
    df.insert(loc=position, column="label", value=label)
    return df


def interleave(df_a: pd.DataFrame, df_b: pd.DataFrame, df_c: pd.DataFrame,
               chunk: int = 4) -> pd.DataFrame:
    """
    Interleave three DataFrames in chunks of `chunk` rows:
    chunk from A, chunk from B, chunk from C, repeat until all rows are used.
    """
    frames = []
    max_len = max(len(df_a), len(df_b), len(df_c))

    for start in range(0, max_len, chunk):
        end = start + chunk
        for df in (df_a, df_b, df_c):
            slice_ = df.iloc[start:end]
            if not slice_.empty:
                frames.append(slice_)

    return pd.concat(frames, ignore_index=True)


def main():
    configs = [
        (INPUT_MAT_A, "A"),
        (INPUT_MAT_B, "B"),
        (INPUT_MAT_C, "C"),
    ]

    dataframes = []
    for path, label in configs:
        print(f"Loading: {path}")
        df = load_mat_as_dataframe(path)
        print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        df = insert_label_column(df, label, position=2)
        print(f"  Inserted '{label}' label column. New shape: {df.shape}")
        dataframes.append(df)

    df_a, df_b, df_c = dataframes

    print("Interleaving CSVs in chunks of 4 rows (A → B → C → repeat) ...")
    result = interleave(df_a, df_b, df_c, chunk=4)
    print(f"  Final shape: {result.shape[0]} rows × {result.shape[1]} columns")

    print(f"Saving to: {OUTPUT_CSV}")
    result.to_csv(OUTPUT_CSV, index=False, header=False)
    print("Done!")


if __name__ == "__main__":
    main()
