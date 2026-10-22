import pandas as pd
from sklearn.preprocessing import OneHotEncoder

NUMERIC_COLUMNS = [
    "length",
    "diameter",
    "height",
    "whole_weight",
    "shucked_weight",
    "viscera_weight",
    "shell_weight",
]


def preprocess(
    df: pd.DataFrame, encoder: OneHotEncoder | None = None
) -> tuple[pd.DataFrame, pd.Series | None, OneHotEncoder]:
    """Rename columns to snake_case, one-hot encode `sex` and split off the target.

    Fits a new encoder when `encoder` is None. `y` is None when there is no `rings` column.
    """
    df = df.rename(columns=lambda col: col.strip().lower().replace(" ", "_"))

    if encoder is None:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        encoder.fit(df[["sex"]])
    sex = pd.DataFrame(
        encoder.transform(df[["sex"]]),
        columns=encoder.get_feature_names_out(["sex"]),
        index=df.index,
    )

    X = pd.concat([df[NUMERIC_COLUMNS], sex], axis=1)
    y = df["rings"] if "rings" in df.columns else None
    return X, y, encoder
