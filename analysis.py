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

if __name__ == "__main__":
    model = logit("has_grand_child ~ has_child", data_train).fit(method="bfgs")
    print(model.summary2())
