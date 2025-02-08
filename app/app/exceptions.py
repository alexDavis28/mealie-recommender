class MealieRecommenderException(Exception):
    pass

class MealieError(MealieRecommenderException):
    pass

class MealieApiError(MealieRecommenderException):
    pass