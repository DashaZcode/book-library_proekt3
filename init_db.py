"""
Скрипт для инициализации базы данных.
Запускать только один раз!
"""

print("=== Инициализация PostgreSQL для книжной библиотеки ===")
print("Запускайте этот скрипт только один раз!")
print("")

try:
    from booklib.db_storage import PostgreSQLStorage

    print("Создаю подключение к базе данных...")
    storage = PostgreSQLStorage()

    print("\n✅ База данных успешно инициализирована!")
    print("\nТеперь можно использовать команды:")
    print("python main.py add --title 'Война и мир' --author 'Толстой' --year 1869 --genre 'Роман'")
    print("python main.py list")
    print("python main.py check")
    print("python main.py export")

except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    print("\nПроверьте:")
    print("1. PostgreSQL установлен и запущен")
    print("2. Пароль по умолчанию '12345' или исправьте в db_storage.py")
    print("3. Пользователь 'postgres' существует")