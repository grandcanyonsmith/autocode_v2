import logging
import os
import unittest

import aiohttp
import openai
import termcolor

logger = logging.getLogger(__name__)


# Function to get the OpenAI API key from the environment
async def get_openai_api_key() -> str:
    """Retrieve the OpenAI API key from the environment and handle errors if it's not found"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("OpenAI API key not found in environment variables")
        logger.info(f"Successfully retrieved OpenAI API key: {api_key}")
        return api_key
    except Exception as e:
        logger.error(f"Error getting OpenAI API key: {e.args[0]}")
        raise e


# Function to get OpenAI engine from the environment
async def get_openai_engine() -> str:
    """Retrieves the OpenAI engine from the environment and handles errors if it's not found"""
    try:
        engine = os.getenv("OPENAI_ENGINE")
        if engine is None:
            raise ValueError("OpenAI engine not found in environment variables")
        logger.info(f"Successfully retrieved OpenAI engine: {engine}")
        return engine
    except Exception as e:
        logger.error(f"Error getting OpenAI engine: {e}")
        raise e


# Function to make the API call to the OpenAI engine and close the session
async def make_openai_api_call(engine: str, api_key: str, payload: dict) -> dict:
    """Makes an API call to the OpenAI engine and closes the session afterwards"""
    try:

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://api.openai.com/v1/engines/{engine}/completions",
                headers={"Authorization": f"Bearer {openai.api_key}"},
                json=payload,
            ) as resp:
                response = await resp.json()
                print(response)
                return response["choices"][0]["text"]

    finally:
        await session.close()


# Class to create a SuggestionHandler
class SuggestionHandler:

    # Initialize the class and set the OpenAI engine
    def __init__(self, engine: str = os.getenv("OPENAI_ENGINE")):
        self.engine = engine
        self.logger = logging.getLogger(__name__)

    # Function to make the API call to the OpenAI engine and close the session
    async def _make_openai_api_call(
        self, engine: str, api_key: str, payload: dict
    ) -> dict:
        """Makes an API call to the OpenAI engine and closes the session afterwards"""
        try:
            engine = await get_openai_engine()
            response = await make_openai_api_call(engine, api_key, payload)
            logger.info(f"Response received from OpenAI API: {response}")

            return response

        except Exception as e:
            logger.error(f"Error making API call to OpenAI: {e}")
            raise e

    # Function to get suggestions from OpenAI with keyword arguments for better readability
    async def get_suggestions(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int =1000,
        top_p: float = 1,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
        stop_words: list = None,
    ) -> str:
        """Makes an API call to the OpenAI API and returns the suggestions for improvement"""
        # Set default values for stop words if none are provided
        # if stop_words is None:
        #     stop_words = ["\n\n### Suggestions", "\n\n### New"]

        # Retrieve the OpenAI API key
        api_key = await get_openai_api_key()

        # Create a dictionary to store the payload data
        payload_data = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stop": stop_words,
        }

        try:
            # Make the API call to OpenAI
            response = await self._make_openai_api_call(
                self.engine, api_key, payload_data
            )
            logger.info(f"Successfully retrieved suggestions: {response}")
            return response

        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            raise e