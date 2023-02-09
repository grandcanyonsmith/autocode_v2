import argparse
import asyncio
import logging
import os
import unittest

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
        """Improves the code in the given file"""
        logging.info(f"Starting code improvement for {self.file_path}")
        self.file_contents = await self.get_file_contents()
        self.file_type = self.file_type_handler.get_file_type(self.file_path)
        self.selected_suggestions = await self.get_suggestions()
        self.applied_suggestions = await self.apply_suggestions()
        await self.file_handler.write_file(self.applied_suggestions)
        logging.info(f"Code improvement finished for {self.file_path}")

    async def get_file_contents(self) -> str:
        """Retrieve the file contents from the file handler"""
        return await self.file_handler.read_file()

    async def apply_suggestions(self) -> str:
        """Apply the suggestions to improve the code from the suggestion handler"""
        return await self.suggestion_handler.get_suggestions(
            f'''#### Improve the following {self.file_type} using the instructions below\n\n### Old {self.file_type}\n"""\n{self.file_contents}\n"""\n\n### Instructions\n"""\n{self.selected_suggestions}\n"""\n\n### New {self.file_type}\n"""\n'''
        )

    async def get_suggestions(self) -> str:
        """Get the suggestions to improve the code from the suggestion handler"""
        return await self.suggestion_handler.get_suggestions(
            f"### Old {self.file_type}\n{self.file_contents}\n\nHow could I simplify this {self.file_type}?\n"
            # f"#### List how to improve this {self.file_type}\n\n### Old {self.file_type}\n{self.file_contents}\n\n\nHow could I improve this {self.file_type}?\n"
        )


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
