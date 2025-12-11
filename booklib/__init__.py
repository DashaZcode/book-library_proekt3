"""
Пакет книжной библиотеки.

Этот пакет предоставляет функциональность для управления коллекцией книг,
включая добавление, удаление, поиск и сортировку книг.

Модули:
    models-классы данных для представления книг
    storage-работа с хранилищем данных (JSON/CSV)
    filters-поиск и сортировка книг
    commands-обработчики команд для интерфейса командной строки
"""

"""
Пакет книжной библиотеки.
"""

from .models import Book
from .storage import LibraryStorage  # Оставляем для обратной совместимости
from .db_storage import PostgreSQLStorage  # Добавлено: новое хранилище
from .filters import BookFilter
from .commands import LibraryCommands

__all__ = ['Book', 'LibraryStorage', 'PostgreSQLStorage', 'BookFilter', 'LibraryCommands']
