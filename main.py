import argparse
from booklib.commands import LibraryCommands

def main():
    parser = argparse.ArgumentParser(description='Книжная библиотека (PostgreSQL)')
    # Убираем --file

    subparsers = parser.add_subparsers(dest='command')

    # Команда добавления книги
    add_parser = subparsers.add_parser('add', help='Добавить книгу')
    add_parser.add_argument('--title', required=True)
    add_parser.add_argument('--author', required=True)
    add_parser.add_argument('--year', required=True, type=int)
    add_parser.add_argument('--genre', required=True)

    remove_parser = subparsers.add_parser('remove', help='Удалить книгу')
    remove_parser.add_argument('--title', help='Название')
    remove_parser.add_argument('--author', help='Автор')

    list_parser = subparsers.add_parser('list', help='Список книг')
    list_parser.add_argument('--sort-by', choices=['title', 'author', 'year', 'genre'], default='title')
    list_parser.add_argument('--reverse', action='store_true')

    search_parser = subparsers.add_parser('search', help='Поиск')
    search_parser.add_argument('--author', help='Автор')
    search_parser.add_argument('--title', help='Название')
    search_parser.add_argument('--year', type=int, help='Год')
    search_parser.add_argument('--genre', help='Жанр')

    add_quote_parser = subparsers.add_parser('add-quote', help='Добавить цитату')
    add_quote_parser.add_argument('--title', required=True)
    add_quote_parser.add_argument('--author', required=True)
    add_quote_parser.add_argument('--quote', required=True)

    remove_quote_parser = subparsers.add_parser('remove-quote', help='Удалить цитату')
    remove_quote_parser.add_argument('--title', required=True)
    remove_quote_parser.add_argument('--author', required=True)
    remove_quote_parser.add_argument('--quote-index', type=int, help='Номер цитаты')

    show_quotes_parser = subparsers.add_parser('show-quotes', help='Показать цитаты')
    show_quotes_parser.add_argument('--title', help='Название')
    show_quotes_parser.add_argument('--author', help='Автор')

    # Команда: создать БД
    create_db_parser = subparsers.add_parser('create-db', help='Создать базу данных')

    # Команда: проверить БД
    check_parser = subparsers.add_parser('check', help='Проверить БД')

    # Команда: экспорт в CSV
    export_parser = subparsers.add_parser('export', help='Экспорт в CSV')
    export_parser.add_argument('--file', default='library_export.csv', help='Имя файла')

    # Команда: удалить БД
    drop_db_parser = subparsers.add_parser('drop-db', help='Удалить базу данных (ОПАСНО!)')
    drop_db_parser.add_argument('--confirm', action='store_true', help='Подтвердить удаление')

    # Команда: очистить данные
    clear_parser = subparsers.add_parser('clear-db', help='Очистить все данные из таблиц (безопасно)')
    clear_parser.add_argument('--confirm', action='store_true', help='Подтвердить очистку')

    # Команда: редактировать книгу
    edit_parser = subparsers.add_parser('edit', help='Редактировать книгу')
    edit_parser.add_argument('--title', required=True, help='Текущее название')
    edit_parser.add_argument('--author', required=True, help='Текущий автор')
    edit_parser.add_argument('--new-title', help='Новое название')
    edit_parser.add_argument('--new-author', help='Новый автор')
    edit_parser.add_argument('--new-year', type=int, help='Новый год')
    edit_parser.add_argument('--new-genre', help='Новый жанр')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'create-db':
        from create_db import create_database
        create_database()
        return

    if args.command == 'check':
        try:
            from booklib.storage import LibraryStorage
            storage = LibraryStorage()
            print(f"База данных подключена")
            print(f"Книг в базе: {len(storage.books)}")
        except Exception as e:
            print(f"Ошибка: {e}")
        return

    if args.command == 'export':
        import csv
        from booklib.storage import LibraryStorage
        storage = LibraryStorage()

        with open(args.file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'author', 'year', 'genre', 'quotes'])
            for book in storage.books:
                quotes_str = '|'.join(book.quotes)
                writer.writerow([book.title, book.author, book.year, book.genre, quotes_str])

        print(f"Экспортировано {len(storage.books)} книг в {args.file}")
        return

    # Обработка остальных команд
    commands = LibraryCommands()  # Без параметра

    if args.command == 'add':
        commands.add_book(args.title, args.author, args.year, args.genre)
    elif args.command == 'remove':
        commands.remove_book(args.title, args.author)
    elif args.command == 'list':
        commands.list_books(args.sort_by, args.reverse)
    elif args.command == 'search':
        commands.search_books(author=args.author, title=args.title, year=args.year, genre=args.genre)
    elif args.command == 'add-quote':
        commands.add_quote(args.title, args.author, args.quote)
    elif args.command == 'remove-quote':
        commands.remove_quote(args.title, args.author, args.quote_index)
    elif args.command == 'show-quotes':
        commands.show_quotes(args.title, args.author)
    elif args.command == 'drop-db':
        if args.confirm:
            commands.drop_database()
        else:
            print("⚠️  ОПАСНО: Эта команда удалит ВСЮ базу данных!")
            print("Используйте: python main.py drop-db --confirm")
    elif args.command == 'clear-db':
        if args.confirm:
            commands.clear_database()
        else:
            print("⚠️  Эта команда удалит ВСЕ данные из таблиц!")
            print("Используйте: python main.py clear-db --confirm")
    elif args.command == 'edit':  # ← ДОБАВЬ ЭТОТ БЛОК В НУЖНОМ МЕСТЕ!
        commands.edit_book(
            args.title, args.author,
            args.new_title, args.new_author,
            args.new_year, args.new_genre
        )

if __name__ == '__main__':
    main()