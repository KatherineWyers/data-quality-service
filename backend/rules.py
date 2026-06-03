import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema, Check

RULES = DataFrameSchema(
    columns={
        "id": Column(
            int,
            checks=Check.greater_than(0),
            nullable=False,
        ),
        "name": Column(
            str,
            checks=Check.str_length(min_value=1, max_value=100),
            nullable=False,
        ),
        "age": Column(
            int,
            checks=Check.in_range(0, 150),
            nullable=False,
        ),
    },

    strict=True,#Flag columns not listed above
    ordered=False,#Row order does not matter
)