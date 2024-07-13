import pytest

from main.functions import find_divisors, create_files
from tests.functions_for_tests import check_multiple_files, delete_multiple_files


#1 Параметризация и тестирование на нахождение делителей
@pytest.mark.parametrize('num, expected_set', [
    (1000, [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, 500, 1000]),
    (150000, [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 25, 30, 40, 48, 50, 60, 75, 80, 100, 120, 125, 150, 200,
              240, 250, 300, 375, 400, 500, 600, 625, 750, 1000, 1200, 1250, 1500, 1875, 2000, 2500, 3000, 3125, 3750,
              5000, 6000, 6250, 7500, 9375, 10000, 12500, 15000, 18750, 25000, 30000, 37500, 50000, 75000, 150000]),
    (20000000, [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 80, 100, 125, 128, 160, 200, 250, 256, 320, 400, 500,
                625, 640, 800, 1000, 1250, 1280, 1600, 2000, 2500, 3125, 3200, 4000, 5000, 6250, 6400, 8000, 10000,
                12500, 15625, 16000, 20000, 25000, 31250, 32000, 40000, 50000, 62500, 78125, 80000, 100000, 125000,
                156250, 160000, 200000, 250000, 312500, 400000, 500000, 625000, 800000, 1000000, 1250000, 2000000,
                2500000, 4000000, 5000000, 10000000, 20000000]),
])
@pytest.mark.asyncio
async def test_find_divisors(num, expected_set):
    """Тестирование функции find_divisors(n) с набором параметров"""
    result_set = await find_divisors(num)
    assert result_set == expected_set


#2 Параметризация и тестирование на создание? проверку и удаление файлов
@pytest.mark.parametrize('index', [1, 5, 10])
@pytest.mark.asyncio
async def test_create_files(index):
    """Тестирование функции create_files(n) с набором параметров, сравнение имен и содержимого созданных файлов,
    удаление созданных файлов"""
    await create_files(index)
    print(f'{index} files has been created')
    await check_multiple_files(index)
    print(f'{index} files has been checked')
    await delete_multiple_files(index)
    print(f'{index} files has been deleted')

#3


#4
