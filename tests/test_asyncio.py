import pytest

from main.functions import find_divisors, create_files
from tests.functions_for_tests import check_multiple_files, delete_multiple_files


#1 Параметризация и тестирование на нахождение делителей
@pytest.mark.parametrize('num, expected_set', [
    (1000000, [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 80, 100, 125, 160, 200, 250, 320, 400, 500, 625, 800,
               1000, 1250, 1600, 2000, 2500, 3125, 4000, 5000, 6250, 8000, 10000, 12500, 15625, 20000, 25000, 31250,
               40000, 50000, 62500, 100000, 125000, 200000, 250000, 500000, 1000000]),
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


@pytest.mark.parametrize('num', [999999, 20000001])
@pytest.mark.asyncio
async def test_find_divisors_out_of_range(num):
    """Тестирование функции find_divisors(n) для значений вне диапазона"""
    with pytest.raises(ValueError, match='Заданное число вне диапазона'):
        await find_divisors(num)


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
