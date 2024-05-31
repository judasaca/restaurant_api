from typing import Any

from pydantic import BaseModel, model_validator


class BaseModelInDB(BaseModel):
    """
    This Model represents objects in the database. It transforms the object '_id' mongodb field to 'id' string.
    """

    id: str

    @model_validator(mode="before")
    @classmethod
    def rename_id_field(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("_id") is not None:
                data["id"] = str(data["_id"])
                del data["_id"]
                return data
        return data


class RandomNumberResponse(BaseModel):
    random_number: int
