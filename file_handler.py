import asyncio
import logging

import aiofiles
import aiohttp


class FileHandler:

    logger = logging.getLogger(__name__)

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_size = 0

    async def read_file(self, num_bytes_to_read: int = 0, encoding: str = "utf-8") -> str:
        return await self.__read_file_helper(num_bytes_to_read=num_bytes_to_read, encoding=encoding)

    async def write_file(self, content: str, append: bool = False, encoding: str = "utf-8") -> None:
        return await self.__write_file_helper(content=content, append=append, encoding=encoding)

    async def read_write_file(self, content: str, encoding: str = "utf-8") -> None:
        return await self.__read_write_file_helper(content=content, encoding=encoding)

    async def make_http_request(
        self,
        url: str,
        headers: dict = None,
        timeout: int = 60,
        encoding: str = "utf-8",
        **kwargs,
    ) -> str:
        if headers is None:
            headers = {}
        try:
            return await self.__make_http_request_helper(
                url=url, headers=headers, timeout=timeout, encoding=encoding, **kwargs
            )
        except Exception as err:
            self.logger.error(f"Error making HTTP request: {err}")
            raise err

    async def __read_write_file_helper_read_file_content(self, encoding: str) -> str:
        return await self.__read_file_helper_read_file(num_bytes_to_read=0, encoding=encoding)

    async def __read_write_file_helper_write_file_content(self, content: str, encoding: str) -> None:
        return await self.__write_file_helper(content=content, append=True, encoding=encoding)

    async def __make_http_request_helper_get_response_content(self, response, encoding: str) -> str:
        return await response.text(encoding=encoding)

    async def __write_file_helper_write_file(self, file, content: str) -> None:
        await file.write(content)

    async def __read_file_helper_read_file(self, file, num_bytes_to_read: int) -> str:
        return await file.read(num_bytes_to_read) if num_bytes_to_read > 0 else await file.read()


    async def __read_file_helper(self, num_bytes_to_read: int, encoding: str) -> str:
        async with aiofiles.open(self.file_path, "r", encoding=encoding) as file:
            return await self.__read_file_helper_read_file(
                file=file, num_bytes_to_read=num_bytes_to_read
            )

    async def __write_file_helper(
        self, content: str, append: bool, encoding: str
    ) -> None:
        async with aiofiles.open(
            self.file_path, "a" if append else "w", encoding=encoding
        ) as file:
            await self.__write_file_helper_write_file(file=file, content=content)

    async def __read_write_file_helper(self, content: str, encoding: str) -> None:
        content_from_file = await self.__read_write_file_helper_read_file(encoding=encoding)
        return await self.__read_write_file_helper_write_file(content=content_from_file + content, encoding=encoding)

    async def __make_http_request_helper(
        self, url: str, headers: dict, timeout: int, encoding: str, **kwargs
    ) -> str:
        content = None
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout, headers=headers, **kwargs) as response:
                if response.status == 200:
                    content = await self.__make_http_request_helper_get_content(response=response, encoding=encoding)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    file_handler = FileHandler(file_path="tmp.py")
    asyncio.run(file_handler.read_file())
