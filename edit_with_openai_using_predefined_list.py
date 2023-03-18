import json
import logging
import re
import openai

logging.basicConfig(level=logging.INFO)

# File functions

def read_jsonl_file(filename):
    with open(filename, "r") as f:
        return [json.loads(line)["text"] for line in f]
def edit_file(filename, code_instruction):
    with open(filename, "r+") as f:
        code = f.read()
        code = remove_comments(code)
        new_code = openai_edit(code, code_instruction)
        f.seek(0)
        f.truncate()
        f.write(new_code)
    logging.info(f"Edited code with suggestion: {code_instruction}")


# Code functions


def remove_comments(code):
    return re.sub(r"#[^\r]*", "", code)


def extract_function_calls(code):
    return re.findall(r"\w+\(.*\)", code)



def openai_edit(code, code_instruction):
    response = openai.Edit.create(
        instruction=code_instruction,
        model="code-davinci-edit-001",
        input=code,
        n=2,
        temperature=0.1,
        top_p=1,
    )
    print(response)
    return response["choices"][0]["text"]


# Main function
def main():
    logging.info("Starting program")
    code_instructions = read_jsonl_file("code_list.jsonl")
    code_filename = "t.py"
    for code_instruction in code_instructions:
        try:
            edit_file(code_filename, code_instruction)
        except Exception as e:
            logging.exception(f"Error editing code with suggestion: {code_instruction}")
    logging.info("Finished program")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception("Error in main")
