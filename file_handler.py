import os
import logging
import asyncio
import aiofiles
import aiohttp

class FileHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        try:
            self.file_size = os.stat(self.file_path).st_size
        except Exception as err:
            self.logger.error(f"Error initializing file handler: {err}")

    async def read_file(self) -> str:
        """Reads a file and returns its contents"""
        self.logger.info("Attempting to read file")
        if not os.path.isfile(self.file_path):
            self.logger.error("Error reading file: File does not exist")
            raise FileNotFoundError

        content = None
        try:
            async with aiofiles.open(self.file_path, "r", encoding="utf-8") as file:
                if self.file_size > 0:
                    content = await file.read(self.file_size)
        except Exception as err:
            self.logger.error(f"Error reading file: {err}")
        finally:
            self.logger.info("Finished reading file")
            return content

    async def write_file(self, content: str) -> bool:
        """Writes content to a file"""
        self.logger.info("Attempting to write file")
        success = False
        try:
            async with aiofiles.open(self.file_path, "w", encoding="utf-8") as file:
                await file.write(content)
            success = True
        except Exception as err:
            self.logger.error(f"Error writing file: {err}")
        finally:
            self.logger.info("Finished writing file")
            return success

    async def read_write_file(self, content: str) -> bool:
        """Reads and writes content to a file"""
        success = False
        try:
            await self.read_file()
            success = await self.write_file(content)
        except Exception as err:
            self.logger.error(f"Error reading and writing file: {err}")
        finally:
            return success

    async def make_http_request(self, url: str) -> str:
        """Makes an HTTP request to the specified URL and returns the response"""
        self.logger.info("Attempting to make HTTP request")
        content = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()
        except Exception as err:
            self.logger.error(f"Error making HTTP request: {err}")
        finally:
            self.logger.info("Finished making HTTP request")
            return content