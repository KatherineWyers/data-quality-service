import pandera.pandas as pa

TYPE_MAP = {
    "one_dim_integer": int,
    "alphatext": str,
}

class RulesService:
    def build_schema(self, rules: dict) -> pa.DataFrameSchema:
        columns = {}
        strict = rules.get("settings", {}).get("strict_columns")

        for col, config in rules["columns"].items():
            checks = []
            params = config.get("validation_params", {})
            col_type = config.get("type")

            if col_type not in TYPE_MAP:
                raise ValueError(f"Column '{col}' has unknown type: '{col_type}'. Valid types are: {list(TYPE_MAP.keys())}")

            if col_type == "one_dim_integer":
                if params.get("min") is not None:
                    checks.append(pa.Check.greater_than_or_equal_to(params["min"]))
                if params.get("max") is not None:
                    checks.append(pa.Check.less_than_or_equal_to(params["max"]))

            elif col_type == "alphatext":
                if params.get("min-length") is not None:
                    checks.append(pa.Check(lambda s, min_len=params["min-length"]: s.str.len() >= min_len))
                if params.get("max-length") is not None:
                    checks.append(pa.Check(lambda s, max_len=params["max-length"]: s.str.len() <= max_len))

            columns[col] = pa.Column(
                dtype=TYPE_MAP[col_type],
                nullable=config.get("required" != "true"),
                checks=checks,
            )

        return pa.DataFrameSchema(columns, strict=strict)



