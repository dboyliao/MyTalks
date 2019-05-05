import numpy as np
import pandas as pd

from statsmodels.formula.api import logit

family_data = pd.read_csv("family.csv")
data_train = (
    family_data.join(
        (
            family_data.rename(columns={"parent": "child", "child": "grand_child"})
            .copy()
            .set_index("child")
        ),
        on="child",
        how="left",
    )[["child", "grand_child"]]
    .notna()
    .applymap(int)
    .rename(columns={"child": "has_child", "grand_child": "has_grand_child"})
)
idx_has_grand = np.where(data_train.has_grand_child > 0)[0]
idx_no_grand = np.where(data_train.has_grand_child == 0)[0]
idx = np.concatenate(
    [
        np.random.choice(
            idx_has_grand,
            size=(data_train.has_grand_child == 0).astype(int).sum(),
            replace=True,
        ),
        idx_no_grand,
    ]
)
data_balanced = data_train.iloc[idx, :]

if __name__ == "__main__":
    model = logit("has_grand_child ~ has_child", data_balanced).fit(method="bfgs")
    print(model.summary2())
