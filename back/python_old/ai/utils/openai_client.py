from dotenv import load_dotenv

from openai import AsyncOpenAI
import os

load_dotenv()


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
    return AsyncOpenAI(api_key=str(os.getenv("AI_API_KEY", "")))
