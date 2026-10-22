import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def preprocess(
    df: pd.DataFrame, encoder: OneHotEncoder | None = None
) -> tuple[pd.DataFrame, pd.Series | None, OneHotEncoder]:
    """Return the features X, the target y and the fitted encoder."""
    df = df.rename(columns=lambda name: name.lower().replace(" ", "_"))
    if encoder is None:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        encoder.fit(df[["sex"]])
    sex_encoded = pd.DataFrame(
        encoder.transform(df[["sex"]]),
        columns=encoder.get_feature_names_out(),
        index=df.index,
    )
    # errors="ignore" so the API can preprocess a row that has no `rings`
    X = pd.concat(
        [df.drop(columns=["sex", "rings"], errors="ignore"), sex_encoded], axis=1
    )
    y = df["rings"] if "rings" in df.columns else None
    return X, y, encoder
