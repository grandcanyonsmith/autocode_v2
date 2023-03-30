
# import asyncio
# import logging
# import os
# from typing import Dict, Optional, Any

# import aiofiles
# import aiohttp


# class FileHandler:

#     logger = logging.getLogger(__name__)

#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.file_size = 0

#     async def read_file(self, num_bytes_to_read: int = 0, encoding: str = "utf-8") -> str:
#         return await self.__read_file_helper(num_bytes_to_read=num_bytes_to_read, encoding=encoding)

#     async def write_file(self, content: str, append: bool = False, encoding: str = "utf-8") -> None:
#         return await self.__write_file_helper(content=content, append=append, encoding=encoding)

#     async def read_write_file(self, content: str, encoding: str = "utf-8") -> None:
#         return await self.__read_write_file_helper(content=content, encoding=encoding)

#     async def make_http_request(
#         self,
#         url: str,
#         headers: Optional[Dict[str, str]] = None,
#         timeout: int = 60,
#         encoding: str = "utf-8",
#         **kwargs: Any,
#     ) -> str:
#         """
#         Make an HTTP request and return the response text.

#         :param url: The URL to make the request to.
#         :param headers: A dictionary of headers to include in the request.
#         :param timeout: The timeout for the request in seconds.
#         :param encoding: The encoding to use for the response text.
#         :param kwargs: Additional keyword arguments to pass to the helper function.
#         :return: The response text.
#         :raises: RequestError if there is an error making the HTTP request.
#         """
#         if headers is None:
#             headers = {}

#         try:
#             return await self.__make_http_request_helper(
#                 url=url, headers=headers, timeout=timeout, encoding=encoding, **kwargs
#             )
#         except Exception as err:
#             self.logger.error(f"Error making HTTP request: {err}")
#             raise RequestError(f"Error making HTTP request: {err}") from err

#     async def __make_http_request_helper(
#         self, url: str, headers: Dict[str, str], timeout: int, encoding: str, **kwargs: Any
#     ) -> str:
#         # Implementation of the helper function
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=headers, timeout=timeout, **kwargs) as response:
#                 response.raise_for_status()
#                 return await response.text(encoding=encoding)


#     async def __read_write_file_helper_read_file(self, encoding: str) -> bytes:
#         return await self.__read_file_helper_read_file(num_bytes_to_read=0, encoding=encoding)

#     async def __make_http_request_helper_get_content(self, response, encoding: str) -> str:
#         return await response.text(encoding=encoding)

#     async def __write_file_helper_write_file(self, file, content: bytes) -> None:
#         await file.write(content)

#     async def __read_file_helper_read_file(self, file, num_bytes_to_read: int) -> bytes:
#         return await file.read(num_bytes_to_read) if num_bytes_to_read > 0 else await file.read()


#     async def __read_file_helper(self, num_bytes_to_read: int, encoding: str) -> bytes:
#         async with aiofiles.open(self.file_path, "r", encoding=encoding) as file:
#             return await self.__read_file_helper_read_file(
#                 file=file, num_bytes_to_read=num_bytes_to_read
#             )

#     async def __write_file_helper(
#         self, content: bytes, append: bool, encoding: str
#     ) -> None:
#         async with aiofiles.open(
#             self.file_path, "a" if append else "w", encoding=encoding
#         ) as file:
#             await self.__write_file_helper_write_file(file=file, content=content)

#     async def __read_write_file_helper(self, content: bytes, encoding: str) -> None:
#         content_from_file = await self.__read_write_file_helper_read_file(encoding=encoding)
#         return await self.__write_file_helper(content=content_from_file + content, append=True, encoding=encoding)

#     async def __make_http_request_helper(
#         self, url: str, headers: dict, timeout: int, encoding: str, **kwargs
#     ) -> str:
#         content = None
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, timeout=timeout, headers=headers, **kwargs) as response:
#                 if response.status == 200:
#                     content = await self.__make_http_request_helper_get_content(response=response, encoding=encoding)

# import asyncio
# import logging
# import os
# from typing import Dict, Optional, Any

# import aiofiles
# import aiohttp


# class FileHandler:
#     logger = logging.getLogger(__name__)

#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.file_size = 0

#     async def read_file(self, num_bytes_to_read: int = 0, encoding: str = "utf-8") -> str:
#         async with aiofiles.open(self.file_path, "r", encoding=encoding) as file:
#             return await (file.read(num_bytes_to_read) if num_bytes_to_read > 0 else file.read())

#     async def write_file(self, content: str, append: bool = False, encoding: str = "utf-8") -> None:
#         async with aiofiles.open(
#             self.file_path, "a" if append else "w", encoding=encoding
#             ) as file:
#             await file.write(content)
# async def read_write_file(self, content: str, encoding: str = "utf-8") -> None:
#     content_from_file = await self.read_file(encoding=encoding)
#     await self.write_file(content=content_from_file + content, append=True, encoding=encoding)

# async def make_http_request(
#     self,
#     url: str,
#     headers: Optional[Dict[str, str]] = None,
#     timeout: int = 60,
#     encoding: str = "utf-8",
#     **kwargs: Any,
# ) -> str:
#     if headers is None:
#         headers = {}

#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers, timeout=timeout, **kwargs) as response:
#             response.raise_for_status()
#             return await response.text(encoding=encoding)

#     try:
#         return await self.__make_http_request_helper(
#             url=url, headers=headers, timeout=timeout, encoding=encoding, **kwargs
#         )
#     except Exception as err:
#         self.logger.error(f"Error making HTTP request: {err}")
#         raise RequestError(f"Error making HTTP request: {err}") from err

# class RequestError(Exception):
#     pass

# 85 80 85 75 80


# import asyncio
# import logging
# import os
# from typing import Dict, Optional, Any

# import aiofiles
# import aiohttp


# class FileHandler:
#     """A class to handle file read and write operations asynchronously."""

#     logger = logging.getLogger(__name__)

#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.file_size = 0

#     async def read_file(self, num_bytes_to_read: int = 0, encoding: str = "utf-8") -> str:
#         """Read the contents of a file asynchronously.

#         Args:
#             num_bytes_to_read (int): Number of bytes to read from the file. If 0, read the entire file.
#             encoding (str): The encoding to use when reading the file.

#         Returns:
#             str: The contents of the file.
#         """
#         async with aiofiles.open(self.file_path, "r", encoding=encoding) as file:
#             return await (file.read(num_bytes_to_read) if num_bytes_to_read > 0 else file.read())

#     async def write_file(self, content: str, append: bool = False, encoding: str = "utf-8") -> None:
#         """Write content to a file asynchronously.

#         Args:
#             content (str): The content to write to the file.
#             append (bool): Whether to append the content to the existing file or overwrite it.
#             encoding (str): The encoding to use when writing the file.
#         """
#         async with aiofiles.open(
#             self.file_path, "a" if append else "w", encoding=encoding
#             ) as file:
#             await file.write(content)

#     async def read_write_file(self, content: str, encoding: str = "utf-8") -> None:
#         """Read the contents of a file and then append new content to it asynchronously.

#         Args:
#             content (str): The content to append to the file.
#             encoding (str): The encoding to use when reading and writing the file.
#         """
#         content_from_file = await self.read_file(encoding=encoding)
#         await self.write_file(content=content_from_file + content, append=True, encoding=encoding)


# class HttpRequestHandler:
#     """A class to handle HTTP requests asynchronously."""

#     logger = logging.getLogger(__name__)

#     async def make_http_request(
#         self,
#         url: str,
#         headers: Optional[Dict[str, str]] = None,
#         timeout: int = 60,
#         encoding: str = "utf-8",
#         **kwargs: Any,
#     ) -> str:
#         """Make an HTTP GET request asynchronously.

#         Args:
#             url (str): The URL to request.
#             headers (Optional[Dict[str, str]]): Headers to include in the request.
#             timeout (int): Timeout for the request in seconds.
#             encoding (str): The encoding to use when decoding the response text.
#             **kwargs: Additional keyword arguments for the aiohttp request.

#         Returns:
#             str: The response text.

#         Raises:
#             RequestError: If there is an error making the HTTP request.
#         """
#         if headers is None:
#             headers = {}

#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url, headers=headers, timeout=timeout, **kwargs) as response:
#                     response.raise_for_status()
#                     return await response.text(encoding=encoding)
#         except Exception as err:
#             self.logger.error(f"Error making HTTP request: {err}")
#             raise RequestError(f"Error making HTTP request: {err}") from err


# class RequestError(Exception):
#     """A custom exception class for HTTP request errors."""
#     pass


# 1. Readability: 90
# 2. Efficiency: 85
# 3. Maintainability: 90
# 4. Robustness: 80
# 5. Reusability: 85
# 90 85 90 80 85


import asyncio
import logging
import os
from typing import Dict, Optional, Any

import aiofiles
import aiohttp


class FileHandler:
    """A class to handle file read and write operations asynchronously."""

    logger = logging.getLogger(__name__)

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_size = 0

    async def read_file(self,num_bytes_to_read: int = 0, encoding: str = "utf-8") -> str:
        """Read the contents of a file asynchronously.

        Args:
            num_bytes_to_read (int): Number of bytes to read from the file. If 0, read the entire file.
            encoding (str): The encoding to use when reading the file.

        Returns:
            str: The contents of the file.
        """
        if num_bytes_to_read < 0:
           raise ValueError("num_bytes_to_read must be non-negative")

        async with aiofiles.open(self.file_path, "r", encoding=encoding) as file:
            return await (file.read(num_bytes_to_read) if num_bytes_to_read > 0 else file.read())

    async def write_file(self, content: str, append: bool = False, encoding: str = "utf-8") -> None:
        """Write content to a file asynchronously.

        Args:
            content (str): The content to write to the file.
            append (bool): Whether to append the content to the existing file or overwrite it.
            encoding (str): The encoding to use when writing the file.
        """
        if content is None:
            raise ValueError("content must not be None")

        async with aiofiles.open(
            self.file_path, "a" if append else "w", encoding=encoding
        ) as file:
            await file.write(content)

    async def read_write_file(self, content: str, encoding: str = "utf-8") -> None:
        """Read the contents of a file and then append new content to it asynchronously.

        Args:
            content (str): The content to append to the file.
            encoding (str): The encoding to use when reading and writing the file.
        """
        if content is None:
            raise ValueError("content must not be None")

        content_from_file = await self.read_file(encoding=encoding)
        await self.write_file(content=content_from_file + content, append=True, encoding=encoding)


class HttpRequestHandler:
    """A class to handle HTTP requests asynchronously."""

    logger = logging.getLogger(__name__)

    async def make_http_request(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 60,
        encoding: str = "utf-8",
        **kwargs: Any,
    ) -> str:
        """Make an HTTP GET request asynchronously.

        Args:
            url (str): The URL to request.
            headers (Optional[Dict[str, str]]): Headers to include in the request.
            timeout (int): Timeout for the request in seconds.
            encoding (str): The encoding to use when decoding the response text.
            **kwargs: Additional keyword arguments for the aiohttp request.

        Returns:
            str: The response text.

        Raises:
            RequestError: If there is an error making the HTTP request.
        """
        if not url:
            raise ValueError("url must not be empty")

        if headers is None:
            headers = {}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=timeout, **kwargs) as response:
                    response.raise_for_status()
                    return await response.text(encoding=encoding)
        except Exception as err:
            self.logger.error(f"Error making HTTP request: {err}")
            raise RequestError(f"Error making HTTP request: {err}") from err


class RequestError(Exception):
    """A custom exception class for HTTP request errors."""
    pass