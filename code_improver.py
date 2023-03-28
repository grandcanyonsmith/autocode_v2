import argparse
import asyncio
import logging
import os
import unittest
import textwrap


import aiofiles
import aiohttp
import openai

from file_handler import FileHandler
from file_type_handler import FileTypeHandler
from suggestion_handler import SuggestionHandler


class CodeImprover:
    """Class for improving code"""

    def __init__(self, *, file_path: str):
        """
        Initializes the CodeImprover class

        Parameters:
            file_path (str): The path to the file to be improved
        """
        self.file_path = file_path
        self.file_handler = FileHandler(file_path)
        self.file_type_handler = FileTypeHandler()
        self.suggestion_handler = SuggestionHandler()
        self.file_type = None
        self.file_contents = None
        self.selected_suggestions = None
        self.applied_suggestions = None

    async def improve_code(self) -> None:
        """
        Improves the code in the given file.
        """
        logging.info(f"Starting code improvement for {self.file_path}")

        await self.read_file()
        self.detect_file_type()
        await self.fetch_suggestions()
        await self.apply_suggestions_to_code()
        await self.write_improved_code()

        logging.info(f"Code improvement finished for {self.file_path}")

    async def read_file(self) -> None:
        """
        Reads the contents of the file.
        """
        self.file_contents = await self.get_file_contents()

    def detect_file_type(self) -> None:
        """
        Detects the file type of the given file.
        """
        self.file_type = self.file_type_handler.get_file_type(self.file_path)

    async def fetch_suggestions(self) -> None:
        """
        Fetches suggestions to improve the code.
        """
        self.selected_suggestions = await self.get_suggestions()

    async def apply_suggestions_to_code(self) -> None:
        """
        Applies the suggestions to the code.
        """
        if self.file_contents is not None:
            self.applied_suggestions = await self.apply_suggestions()
        else:
            logging.warning("File contents are not available. Skipping code improvement.")

    async def write_improved_code(self) -> None:
        """
        Writes the improved code back to the file.
        """
        if self.applied_suggestions is not None:
            await self.file_handler.write_file(self.applied_suggestions)
        else:
            logging.warning("Applied suggestions are not available. Skipping file write.")

    async def get_file_contents(self) -> str:
        """Retrieve the file contents from the file handler"""
        return await self.file_handler.read_file()

    async def apply_suggestions(self) -> str:
        """
        Apply the suggestions to improve the code from the suggestion handler.

        Returns:
            str: The improved code as a string.
        """
        formatted_file = self.format_file_contents()
        formatted_suggestions = self.format_suggestions()
        
        suggestions_request = textwrap.dedent(f"""\
            #### Improve the following {self.file_type} using the instructions below

            ### Old {self.file_type}
            ```
            {formatted_file}
            ```

            ### Instructions
            ```
            {formatted_suggestions}
            ```

            ### New {self.file_type}
            ```
            {{new_code}}
            ```
            """)
        
        return await self.suggestion_handler.get_suggestions(suggestions_request)

    def format_file_contents(self) -> str:
        """
        Format the file contents for the suggestions request.

        Returns:
            str: The formatted file contents.
        """
        return textwrap.indent(self.file_contents, "    ")

    def format_suggestions(self) -> str:
        """
        Format the selected suggestions for the suggestions request.

        Returns:
            str: The formatted selected suggestions.
        """
        return textwrap.indent(self.selected_suggestions, "    ")


    async def get_suggestions(self) -> str:
        """
        Get the suggestions to improve the code from the suggestion handler.

        Returns:
            str: The suggestions as a string.
        """
        suggestions_request = textwrap.dedent(f"""\
            #### List how to improve this {self.file_type}

            ### Old {self.file_type}
            ```
            {self.file_contents}
            ```

            How could I improve this {self.file_type}?
            """)
        
        return await self.suggestion_handler.get_suggestions(suggestions_request)



async def run_code_improver(file_path: str, logging_level: int) -> None:
    """Run the code improver with the given file path and logging level"""
    logging.basicConfig(level=logging_level)
    code_improver = CodeImprover(file_path=file_path)
    await code_improver.improve_code()


async def parse_arguments() -> (str, int):
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description="Code Improver")
    parser.add_argument(
        "--file", type=str, default="read.py", help="file to improve" # type: ignore
    )
    parser.add_argument(
        "--logging-level", type=int, default=logging.INFO, help="logging level"
    )
    args = parser.parse_args()
    return args.file, args.logging_level


def main() -> None:
    """Main function"""
    file_path, logging_level = asyncio.run(parse_arguments())
    asyncio.run(run_code_improver(file_path, logging_level))


if __name__ == "__main__":
    while True:
        main()
