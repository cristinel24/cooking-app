from pydantic import BaseModel


class RecipeData(BaseModel):
    title: str
    description: str
    prepTime: int
    steps: list[str]
    ingredients: list[str]
    allergens: list[str]
    tags: list[str]
    thumbnail: str


class Recipe:
    id: str
    authorId: str
    title: str
    ratingSum: int
    ratingCount: int
    description: str
    prepTime: int
    steps: list[str]
    ingredients: list[str]
    allergens: list[str]
    tags: list[str]
    tokens: list[str]
    ratings: list[str]
    viewCount: int = 0
    thumbnail: str

    def __init__(self, recipe_data: RecipeData):
        self.ratingSum = 0
        self.ratingCount = 0
        self.tokens = []
        self.ratings = []
        self.viewCount = 0
        self.title = recipe_data.title
        self.description = recipe_data.description
        self.prepTime = recipe_data.prepTime
        self.steps = recipe_data.steps
        self.ingredients = recipe_data.ingredients
        self.allergens = recipe_data.allergens
        self.tags = recipe_data.tags
        self.thumbnail = recipe_data.thumbnail

