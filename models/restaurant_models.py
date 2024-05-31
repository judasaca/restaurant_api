from typing import Literal

from pydantic import BaseModel, Field

from models.common_models import BaseModelInDB


class CreateRestaurantBody(BaseModel):
    name: str = Field(..., description="Name of the restaurant")
    stars: int = Field(
        ..., description="Stars should be an integer between 0 and 5", ge=0, le=5
    )
    country: str = Field(..., description="Country of ubication of the restaurant")
    city: str = Field(..., description="City of ubication of the restaurant")
    food_type: Literal[
        "mexican", "japanese", "peruvian", "international", "sea", "others"
    ]
    is_public: bool = Field(
        ...,
        description="Boolean value. If true, any user will be able to see the restaurant information. If false, only you will be able to see the restaurant information",
    )


class RestaurantInDB(BaseModelInDB, CreateRestaurantBody):
    """
    This model represents the restaurant in the database and adds the created_by field and the id field.
    """

    created_by: str


class RestaurantFront(BaseModelInDB):
    """This model is the public representation of the restaurant. This helps us to avoid showing sensitive data."""

    name: str = Field(..., description="Name of the restaurant")
    stars: int = Field(
        ..., description="Stars should be an integer between 0 and 5", ge=0, le=5
    )
    country: str = Field(..., description="Country of ubication of the restaurant")
    city: str = Field(..., description="City of ubication of the restaurant")
    food_type: Literal[
        "mexican", "japanese", "peruvian", "international", "sea", "others"
    ]
