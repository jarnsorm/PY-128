Практическое задание к учебному блоку PY-128.

Список всех зависимостей содержится в requirements.txt

Пакеты:
    main: содержит папку files для хранения созданных файлов; functions.py - основной модуль, содержащий функции
для решения правктического задания.
    tests: модули test_asyncio.py - основной модуль тестирования и functions_for_tests.py - модуль, содержащий логику
    тестов.

Запуск основного модуля производится через вызов функций:
    asyncio.run(find_divisors(20_000_000))
    asyncio.run(create_files(10))
    asyncio.run(make_requests_to_google())
    asyncio.run(make_requests_to_example('https://example.com/', 50, 10, 'xmpl.txt'))

Запуск тестов производится через терминал:
    python -m pytest -vv --cov=main tests

