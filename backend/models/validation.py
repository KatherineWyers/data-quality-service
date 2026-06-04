from dataclasses import dataclass, field, asdict

@dataclass
class ValidationResult:
    success: bool
    message: str
    issues: list = field(default_factory=list)
    error_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class ValidationIssue:
    column: str
    row: int
    message: str
    bad_value: str