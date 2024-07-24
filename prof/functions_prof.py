import asyncio
import cProfile
import io
import pstats
from functools import wraps
import aiofiles
import aiohttp
from pathlib import Path

files_dir = Path(__file__).resolve().parent.parent / 'files'
files_dir.mkdir(parents=True, exist_ok=True)


def profile_async_function(function):
    """Декоратор для профилирования асинхронных функций"""
    @wraps(function)
    async def wrapper(*args, **kwargs):
        f_profile = cProfile.Profile()
        f_profile.enable()
        result = await function(*args, **kwargs)
        f_profile.disable()
        str_ = io.StringIO()
        profile_stats = pstats.Stats(f_profile, stream=str_).sort_stats('cumulative')
        profile_stats.print_stats()
        print(str_.getvalue())
        return result
    return wrapper


# поиск делителей числа. главная функция - find_divisors()
async def find_divisors_in_range(n, start, end):
    """Находим все делители в заданном диапазоне"""
    divisors = []
    for i in range(start, end):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return divisors


@profile_async_function
async def find_divisors(n: int):
    """Создаем диапазоны, вызываем "поиск делителя в заданных диапазонах" параллельно в
    потоках, выводим отсортированный результат"""
    if not (1_000_000 <= n <= 20_000_000):
        raise ValueError("Заданное число вне диапазона")
    chunk = 100_000
    tasks = []
    for start in range(1, int(n ** 0.5) + 1, chunk):
        end = min(start + chunk, int(n ** 0.5) + 1)
        tasks.append(find_divisors_in_range(n, start, end))
    results = await asyncio.gather(*tasks)
    divisors = set()
    for result in results:
        divisors.update(result)
    print(*sorted(divisors))
    return sorted(divisors)


# создание и наполнение файлов. главная функция - create_files()
def write_to_file(filename, content):
    file_path = files_dir / filename
    with file_path.open('w') as f:
        f.write(content)

    print(filename, "created")


async def create_file(index):
    """Создание номерованного файла и наполнение его контентом"""
    filename = f"file_{index}.txt"
    content = f"{index}"
    await asyncio.to_thread(write_to_file, filename, content)


@profile_async_function
async def create_files(n: int):
    """Создание и наполнение контентом n файлов параллельно"""
    if not (n > 0):
        raise ValueError("Заданное число вне диапазона")
    tasks = [create_file(i) for i in range(1, n + 1)]
    await asyncio.gather(*tasks)


# Отправка запросов на http://google.com с ограничениями 10/сек и 50 всего. главная функция - make_requests_to_google()
# Отправка запросов на https://example.com/ и запись параметров в файл с ограничениями 10/сек и 50 всего.
# главная функция - make_requests_to_example()
async def fetch(session, url):
    """Выполнение HTTP-запроса на url"""
    async with session.get(url) as response:
        return await response.text()


async def limited_fetch(sem, session, url):
    """Ограничение количества одновременных запросов"""
    async with sem:
        async with session.get(url) as response:
            return response.status


@profile_async_function
async def make_requests_to_google():
    """Создание семафора, параллельное выполнение HTTP-запросов, вывод результатов"""
    url = "http://google.com"
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch(sem, session, url) for _ in range(50)]
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results, 1):
            print(f"Response {i}: {result}...")


@profile_async_function
async def make_requests_to_example(url, count, limit, filename):
    """По заданным параметрам создает HTTP-запросы, записывает ответы в файл и сверяет кол-во запросов"""
    sem = asyncio.Semaphore(limit)
    file_path = files_dir / filename
    async with aiohttp.ClientSession() as session:
        tasks = [limited_fetch(sem, session, url) for _ in range(count)]
        responses = await asyncio.gather(*tasks)
        async with aiofiles.open(file_path, 'w') as f:
            for i, status in enumerate(responses, 1):
                await f.write(f"Request {i}: Status {status}\n")
        if len(responses) == count:
            return {"massage": f"OK: Completed {len(responses)} requests"}
        return {"massage": f"WARNING: Completed {count} requests"}


if __name__ == "__main__":
    """Запуск функций с профилированием через cProfile с использованием декоратора"""
    print("GO!")
    # asyncio.run(find_divisors(20_000_000))
    asyncio.run(create_files(10))
    # asyncio.run(make_requests_to_google())
    # asyncio.run(make_requests_to_example('https://example.com/', 50, 10, 'xmpl.txt'))