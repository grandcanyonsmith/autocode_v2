from typing import List


def get_prompt_from_text_file(file_name: str) -> List[str]:
    """Reads the file and returns a list of strings.

    :param file_name: The name of the file to be read.
    :return: A list of strings.
    """
    with open(file_name, "r") as file:
        return file.readlines()


def get_list_of_strings_from_prompt(prompt: List[str]) -> List[str]:
    """Removes the numbers from the prompt.

    :param prompt: A list of strings.
    :return: A list of strings.
    """
    return [string.strip("1234567890.") for string in prompt]


def get_list_of_strings_from_file(file_name: str) -> List[str]:
    """Returns a list of strings from the file.

    :param file_name: The name of the file to be read.
    :return: A list of strings.
    """
    return get_list_of_strings_from_file(file_name)


def get_prompt_from_file(file_name: str) -> List[str]:
    """Returns a list of strings from the file.

    :param file_name: The name of the file to be read.
    :return: A list of strings.
    """
    prompt = get_prompt_from_text_file(file_name)
    return get_list_of_strings_from_prompt(prompt)
