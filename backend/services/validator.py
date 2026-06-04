import pandas as pd
import pandera.pandas as pa
from models.validation import ValidationResult, ValidationIssue
from .rules import RulesService

class ValidatorService:
    def run(self, data: pd.DataFrame, rules_json) -> ValidationResult:

        rules_service = RulesService()

        try:
            rules = rules_service.build_schema(rules_json)
        except ValueError as e:
            return ValidationResult(
                success=False,
                message=str(e),
                issues=[],
                error_count=1,
            )

        try:
            rules.validate(data, lazy=True)  # Lazy is Pandera term for loading all errors before returning
            return ValidationResult(success=True, message="All rows valid", error_count=0, issues=[])

        except pa.errors.SchemaErrors as e:
            errors = e.failure_cases[["column", "index", "failure_case", "check"]]
            errors = errors.rename(columns={"index": "row", "failure_case": "bad_value"})

            issues = [
                ValidationIssue(
                    column=row["column"],
                    row=row["row"],
                    message=row["check"],
                    bad_value=row["bad_value"],
                )
                for _, row in errors.iterrows()
            ]

            return ValidationResult(success=False, message="There is invalid data", error_count=len(issues), issues=issues)