from openai import AsyncOpenAI

from constants import AI_API_KEY


def function_singleton(original_function):
    instance = None

    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = original_function(*args, **kwargs)
        return instance

    return wrapper


@function_singleton
def openai_client():
    return AsyncOpenAI(api_key=AI_API_KEY)
