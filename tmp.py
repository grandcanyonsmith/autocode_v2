import logging
import argparse
import asyncio

from file_handler import FileHandler
from file_type_handler import FileTypeHandler
from suggestion_handler import SuggestionHandler


class CodeImprover:
    """
    Initialize the CodeImprover class.

    Args:
        file_path_to_improve (str): The path to the file to improve.
    """    

    def __init__(self, *, file_path_to_improve: str):
        self.file_path_to_improve = file_path_to_improve
        self.file_handler = FileHandler(file_path_to_improve)
        self.file_type_handler = FileTypeHandler()
        self.suggestion_handler = SuggestionHandler()
        self.file_type = "Python Code"
        self.file_contents_before_improvement = []
        self.selected_suggestions = []
        self.file_contents_after_improvement = ""

    async def improve_code(self) -> None:
        logging.info(f"Starting code improvement for {self.file_path_to_improve}")
        await self.get_file_contents()
        await self.get_suggestions()
        await self.apply_suggestions()
        await self.write_file()
        
        logging.info(f"Code improvement finished for {self.file_path_to_improve}")

    async def get_file_contents(self) -> str:
        return await self.file_handler.read_file()
        
    async def apply_suggestions(self) -> str:
        return await self.suggestion_handler.get_suggestions(
        f'''#### Improve the following {self.file_type} using the instructions below\n\n### Old {self.file_type}\n"""\n{self.file_contents}\n"""\n\n### Instructions\n"""\n{self.selected_suggestions}\n"""\n\n### New {self.file_type}\n"""\n'''    
        )

    async def get_suggestions(self) -> str:
        return await self.suggestion_handler.get_suggestions(
        f"### Old {self.file_type}\n{self.file_contents}\n\nHow could I simplify this {self.file_type}?\n"
        )


async def run_code_improver(self, logging_level: int) -> None:
    logging.basicConfig(level=logging_level)
    code_improver = CodeImprover(file_path_to_improve=self)
    await code_improver.improve_code()


async def parse_arguments():
    parser = argparse.ArgumentParser(description="Code Improver")
    parser.add_argument(
        "--file_path_to_improve", type=str, default="t.py", help="file to improve"
    )
    parser.add_argument(
        "--logging-level", type=int, default=logging.INFO, help="logging level"
    )
    args = parser.parse_args()
    return args.file_path_to_improve, args.logging_level


def main():
    file_path_to_improve, logging_level = asyncio.run(parse_arguments())
    asyncio.run(run_code_improver(file_path_to_improve, logging_level))


if __name__ == "__main__":
    main()
