import json
import logging
import openai

logging.basicConfig(level=logging.INFO)


def read_jsonl_file(filename):
    with open(filename, "r") as f:
        return [json.loads(line)["text"] for line in f]


def openai_edit(code, suggestion):
    response = openai.Edit.create(
        instruction=suggestion,
        model="code-davinci-edit-001",
        input=code,
        n=2,
        temperature=0.1,
        top_p=1,
    )
    return response["choices"][0]["text"]


def main():
    suggestions = read_jsonl_file("code_list.jsonl")
    code_filename = "read.py"
    for suggestion in suggestions:
        try:
            with open(code_filename, "r+") as f:
                code = f.read()
                new_code = openai_edit(code, suggestion)
                f.seek(0)
                f.truncate()
                f.write(new_code)
            logging.info(f"Edited code with suggestion: {suggestion}")
        except Exception as e:
            logging.exception(f"Error editing code with suggestion: {suggestion}")


if __name__ == "__main__":
    main()
