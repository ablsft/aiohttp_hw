import pydantic

from errors import BadRequest
from schema import SCHEMA_MODEL


def validate(validation_model: SCHEMA_MODEL, input_data: dict):
    try:
        model_item = validation_model(**input_data)
        return model_item.model_dump(exclude_none=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop('ctx', None)
        raise BadRequest(error)
    