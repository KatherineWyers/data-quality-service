import pytest
import pandas as pd
from services.validator import ValidatorService

validator_service = ValidatorService()

RULES_JSON = {
    "settings": {
        "strict_columns": True
    },
    "columns": {
        "id": {
            "required": "true",
            "type": "one_dim_integer",
            "validation_params": {"min": 1},
        },
        "name": {
            "required": "true",
            "type": "alphatext",
            "validation_params": {"min-length": 3, "max-length": 30},
        },
        "age": {
            "required": "true",
            "type": "one_dim_integer",
            "validation_params": {"min": 0, "max": 150},
        },
    }
}

VALID_DF = pd.DataFrame({
    "id":   [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age":  [25, 30, 45],
})

INVALID_DF = pd.DataFrame({
    "id":   [-1, 2, 3],        # -1 fails min: 1
    "name": ["Alice", "Bo", "Charlie"],  # "Bo" fails min-length: 3
    "age":  [25, 30, 200],     # 200 fails max: 150
})


def test_valid_data_returns_success():
    result = validator_service.run(VALID_DF, RULES_JSON)
    assert result.success is True
    assert result.issues == []

def test_invalid_data_returns_failure():
    result = validator_service.run(INVALID_DF, RULES_JSON)
    assert result.success is False
    assert len(result.issues) == 3

def test_unknown_column_type_returns_error():
    rules_with_invalid_column_name = {**RULES_JSON, "columns": {"id": {"type": "unknown_type", "validation_params": {}}}}
    result = validator_service.run(VALID_DF, rules_with_invalid_column_name)
    assert result.success is False
    assert ("unknown type" in result.message)