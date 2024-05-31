from models.auth_models import UserSignUp
from models.restaurant_models import CreateRestaurantBody

SEED_FIRST_USER = UserSignUp(email="test@user.com", password="testing!USER")

SEED_RESTAURANTS = [
    CreateRestaurantBody(
        name="The best food",
        city="New York",
        country="USA",
        food_type="international",
        stars=3,
        is_public=True,
    ),
    CreateRestaurantBody(
        name="Picante",
        city="DF",
        country="Mexico",
        food_type="mexican",
        stars=5,
        is_public=True,
    ),
    CreateRestaurantBody(
        name="Sushi Master",
        city="Osaka",
        country="Japan",
        food_type="japanese",
        stars=5,
        is_public=True,
    ),
    CreateRestaurantBody(
        name="Tiburon",
        city="Santiago",
        country="Chile",
        food_type="sea",
        stars=4,
        is_public=True,
    ),
    CreateRestaurantBody(
        name="Pisco",
        city="Lima",
        country="Peru",
        food_type="peruvian",
        stars=4,
        is_public=True,
    ),
    CreateRestaurantBody(
        name="Hot Dogs Locos",
        city="New York",
        country="USA",
        food_type="others",
        stars=1,
        is_public=True,
    ),
    CreateRestaurantBody(
        name="Burger King",
        city="Lima",
        country="Peru",
        food_type="others",
        stars=2,
        is_public=True,
    ),
]
