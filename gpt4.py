import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

code = '''
import argparse
import asyncio
import logging

from file_handler import FileHandler  # noqa: F401
from file_type_handler import FileTypeHandler  # noqa: F401
from suggestion_handler import SuggestionHandler  # noqa: F401


class CodeImprover:
    
    Initialize the CodeImprover class.

    Args:
        file_path_to_improve (str): The path to the file to improve.
    

    def __init__(self, *, file_path_to_improve: str):
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
        await self.get_file_contents()
        await self.get_suggestions()
        await self.apply_suggestions()
        await self.write_file()
        
        logging.info(f"Code improvement finished for {self.file_path_to_improve}")

    async def get_file_contents(self) -> str:
        return await self.file_handler.read_file()
        

    async def apply_suggestions(self) -> str:
    
        self.file_contents_after_improvement = await self.suggestion_handler.get_suggestions(f#### Improve the following {self.file_type} using the instructions below\n\n### Old {self.file_type}\n"""\n{self.file_contents_before_improvement}\n"""\n\n### Instructions\n"""\n{self.selected_suggestions}\n"""\n\n### New {self.file_type}\n)
        return self.file_contents_after_improvement
    
    async def get_suggestions(self) -> None:
        
        suggestions = await self.suggestion_handler.get_suggestions(
            f"### Old {self.file_type}\n{self.file_contents_before_improvement}\n\nHow could I simplify this {self.file_type}?\n"
        )
        return self.selected_suggestions

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
'''


completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a programmer and you are writing a program to help you write programs. You want to write a function that takes a list of numbers and returns the sum of the numbers. You are writing the function in Python. What is the name of the function?"},
    {"role": "user", "content": "Improve this code"},
    {"role": "assistant", "content": "What is the code?"},
    {"role": "user", "content": f"This is it:\n\n{code}\n now make it better"},

    ]
)

print(completion.choices[0].message)
