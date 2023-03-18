import argparse
import asyncio
import logging
from file_handler import FileHandler
from file_type_handler import FileTypeHandler
from suggestion_handler import SuggestionHandler


class CodeImprover:
    def __init__(self, file_path_to_improve: str):
        self.file_path_to_improve = file_path_to_improve
        self.file_handler = FileHandler(file_path_to_improve)
        self.file_type_handler = FileTypeHandler()
        self.suggestion_handler = SuggestionHandler()
        self.file_type = "Python Code to graph the best performing stocks"
        self.file_contents_before_improvement = []
        self.selected_suggestions = []
        self.file_contents_after_improvement = ""

    async def improve_code(self) -> None:
        logging.info(f"Starting code improvement for {self.file_path_to_improve}")
        self.file_contents_before_improvement = await self.get_file_contents()
        self.selected_suggestions = await self.get_suggestions()
        self.file_contents_after_improvement = await self.apply_suggestions()
        await self.write_file()
        logging.info(f"Code improvement finished for {self.file_path_to_improve}")

    async def get_file_contents(self) -> str:
        return await self.file_handler.read_file()

    async def apply_suggestions(self) -> str:
        self.file_contents_after_improvement = await self.suggestion_handler.get_suggestions(
            f"Improve the following {self.file_type} using the suggestions provided."
            f"\nOld {self.file_type}\n{self.file_contents_before_improvement}"
            f"\nInstructions\n{self.selected_suggestions}"
            f"\nNew {self.file_type}"
        )
        return self.file_contents_after_improvement

    async def get_suggestions(self) -> None:
        return await self.suggestion_handler.get_suggestions(
            f"Old {self.file_type}\n{self.file_contents_before_improvement}"
            f"How could I simplify this {self.file_type}?"
        )

    async def write_file(self) -> None:
        await self.file_handler.write_file(self.file_contents_after_improvement)


def main():
    parser = argparse.ArgumentParser(description="Improve the code in a file.")
    parser.add_argument("file_path_to_improve", help="The path to the file to improve.")
    args = parser.parse_args()

    code_improver = CodeImprover(file_path_to_improve=args.file_path_to_improve)
    asyncio.run(code_improver.improve_code())


if __name__ == "__main__":
    main()