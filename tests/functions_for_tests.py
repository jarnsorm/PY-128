import asyncio
import os
import aiofiles


async def check_file_content(index):
    """проверка содержимого файла"""
    async with aiofiles.open(f"file_{index}.txt", mode='r') as f:
        content = await f.read()
    assert content == f"{index}"


async def check_multiple_files(index):
    """проверка всех заданных файлов"""
    tasks = [check_file_content(i) for i in range(1, index + 1)]
    results = await asyncio.gather(*tasks)
    return results


async def delete_file(filename):
    """удаление файла"""
    await asyncio.to_thread(os.remove, filename)


async def delete_multiple_files(index):
    """удаление всех файлов"""
    tasks = [delete_file(f"file_{i}.txt") for i in range(1, index + 1)]
    await asyncio.gather(*tasks)