from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class ValidationError(Exception):
    pass


class ResponseValidator:
    def validate(self, response, response_data):
        pass


class DefaultValidation(ResponseValidator):
    def validate(self, response, response_data):
        if "notification" in response_data and response_data["notification"]:
            if response_data["notification"]["type"] == "error":
                msg = "ERROR::-" + response_data["notification"]["message"]
                response.failure(msg)
                raise ValidationError("ERROR::-" + response_data["notification"]["message"])
        if "exception" in response_data:
            msg = "ERROR::exception error--" + response_data['exception']
            response.failure(msg)
            raise ValidationError(msg)


@dataclass
class ElementValidator:
    key: str

    def validate(self, data):
        error = self._validate(data.get(self.key))
        if error:
            raise ValidationError(f"Validation failed for {self.key}: {error}")

    def _validate(self, item) -> str | None:
        pass


@dataclass
class EqualityValidator(ElementValidator):
    value: Any

    def _validate(self, item) -> str | None:
        if item != self.value:
            return f"Expected {self.value}, got {item}"


@dataclass
class LengthValidator(ElementValidator):
    min: int = None
    max: int = None

    def _validate(self, item) -> str | None:
        if not isinstance(item, list):
            return f"Expected a list, got: {item}"
        item_len = len(item)
        if self.min is not None and item_len < self.min:
            return f"Expected at least {self.min} items, got {item_len}"
        if self.max is not None and item_len > self.max:
            return f"Expected at most {self.max} items, got {item_len}"


class ValidateResponseJson(ResponseValidator):
    def __init__(self, validators: list[ElementValidator]):
        self.validators = validators

    def validate_response(self, response, response_data):
        for validator in self.validators:
            try:
                validator.validate(response_data)
            except ValidationError as e:
                response.failure(str(e))
                raise e


class ValidateTitle(ValidateResponseJson):
    def __init__(self, expected_title):
        super().__init__(validators=[EqualityValidator(key="title", value=expected_title)])


class SubmitResponseMessage(ValidateResponseJson):
    def __init__(self, expected_response_message):
        super().__init__(validators=[EqualityValidator(key="submitResponseMessage", value=expected_response_message)])


class HasEntityCount(ValidateResponseJson):
    def __init__(self, min: int = None, max: int = None):
        super().__init__(validators=[LengthValidator(key="entities", min=min, max=max)])
