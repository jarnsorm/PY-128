import asyncio
import os
from pathlib import Path

import aiofiles

files_dir = Path(__file__).resolve().parent.parent / 'main' / 'files'
files_dir.mkdir(parents=True, exist_ok=True)


async def check_file_content(count, diff=False, filename=None):
    """проверка содержимого файла"""
    expected_content = "\n".join([f"Request {i}: Status 200" for i in range(1, count + 1)]) + "\n"
    if diff and filename is not None:
        async with aiofiles.open(files_dir / filename, mode='r') as f:
            content = await f.read()
        assert content == expected_content
    else:
        async with aiofiles.open(files_dir / f"file_{count}.txt", mode='r') as f:
            content = await f.read()
        assert content == f"{count}"


async def check_multiple_files(index):
    """проверка всех заданных файлов"""
    tasks = [check_file_content(count=i) for i in range(1, index + 1)]
    results = await asyncio.gather(*tasks)
    return results


async def delete_file(filename):
    """удаление файла"""
    await asyncio.to_thread(os.remove, files_dir / filename)


async def delete_multiple_files(index):
    """удаление всех файлов"""
    tasks = [delete_file(f"file_{i}.txt") for i in range(1, index + 1)]
    await asyncio.gather(*tasks)