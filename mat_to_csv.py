"""
mat_to_csv.py

Converts a .mat file to a .csv file and inserts a column of 'A'
between the 2nd and 3rd columns of the data.

Requirements:
    pip install scipy numpy pandas
"""

import numpy as np
import pandas as pd
from scipy.io import loadmat

# ── CONFIG ────────────────────────────────────────────────────────────────────
INPUT_MAT  = "/Users/ZHash/Downloads/file_name.mat"   # <-- change this to your .mat file path
OUTPUT_CSV = "output.csv"      # <-- change this to your desired output path
# ─────────────────────────────────────────────────────────────────────────────


def load_mat_as_dataframe(path: str) -> pd.DataFrame:
    """
    Load a .mat file and return its primary numeric array as a DataFrame.

    Handles both legacy (.mat v4–v7.2) and HDF5-based (.mat v7.3) files.
    For legacy files, scipy.io.loadmat is used.
    For v7.3 files, h5py is used as a fallback.
    """
    try:
        mat = loadmat(path)
    except NotImplementedError:
        # v7.3 .mat files are HDF5 — use h5py
        try:
            import h5py
        except ImportError:
            raise ImportError(
                "This .mat file is v7.3 (HDF5 format). "
                "Install h5py to read it:  pip install h5py"
            )
        with h5py.File(path, "r") as f:
            # Grab the first non-metadata key
            keys = [k for k in f.keys() if not k.startswith("#")]
            if not keys:
                raise ValueError("No data variables found in the .mat file.")
            key = keys[0]
            print(f"  Using variable: '{key}'")
            data = np.array(f[key]).T   # h5py stores in column-major order
        return pd.DataFrame(data)

    # Filter out scipy metadata keys (start with '__')
    data_keys = [k for k in mat.keys() if not k.startswith("__")]
    if not data_keys:
        raise ValueError("No data variables found in the .mat file.")

    key = data_keys[0]
    print(f"  Using variable: '{key}'")
    return pd.DataFrame(mat[key])


def insert_column_of_A(df: pd.DataFrame, position: int = 2) -> pd.DataFrame:
    """
    Insert a column of the letter 'A' at `position` (0-indexed).
    Default position=2 places it between the 2nd and 3rd columns.
    """
    df.insert(loc=position, column="label", value="A")
    return df


def main():
    print(f"Loading: {INPUT_MAT}")
    df = load_mat_as_dataframe(INPUT_MAT)
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    print("Inserting 'A' column between columns 2 and 3 ...")
    df = insert_column_of_A(df, position=2)
    print(f"  New shape: {df.shape[0]} rows × {df.shape[1]} columns")

    print(f"Saving to: {OUTPUT_CSV}")
    df.to_csv(OUTPUT_CSV, index=False, header=False)
    print("Done!")


if __name__ == "__main__":
    main()
