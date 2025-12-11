import psycopg2
from .models import Book


class LibraryStorage:
    def __init__(self):
        # Убираем параметр filename
        self.books = self.load_books()

    def _connect(self):
        return psycopg2.connect(
            dbname="book_library",
            user="postgres",
            password="11111",
            host="localhost",
            port="5432"
        )

    def load_books(self):
        books = []
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("SELECT id, title, author, year, genre FROM books ORDER BY id")
            books_data = cur.fetchall()

            for book_data in books_data:
                book_id, title, author, year, genre = book_data

                cur.execute("SELECT quote FROM quotes WHERE book_id = %s", (book_id,))
                quotes_data = cur.fetchall()
                quotes = [q[0] for q in quotes_data]

                book = Book(title, author, year, genre, quotes)
                book.id = book_id
                books.append(book)

            cur.close()
            conn.close()

        except Exception as e:
            print(f"Ошибка загрузки: {e}")

        return books

    # ДОБАВЬ ЭТОТ МЕТОД!
    def get_all_books(self):
        """Возвращает все книги."""
        return self.books

    def save_books(self):
        pass

    def add_book(self, book):
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO books (title, author, year, genre)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (book.title, book.author, book.year, book.genre))

            book_id = cur.fetchone()[0]

            for quote in book.quotes:
                cur.execute("""
                    INSERT INTO quotes (book_id, quote)
                    VALUES (%s, %s)
                """, (book_id, quote))

            conn.commit()
            cur.close()
            conn.close()

            book.id = book_id
            self.books.append(book)

        except Exception as e:
            print(f"Ошибка добавления: {e}")

    # ИЗМЕНИ ЭТОТ МЕТОД! (принимает book_id, а не book)
    def remove_book(self, book_id):
        """Удаляет книгу по ID."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
            conn.commit()

            cur.close()
            conn.close()

            # Удаляем из локального списка
            self.books = [b for b in self.books if b.id != book_id]

        except Exception as e:
            print(f"Ошибка удаления: {e}")

    # ДОБАВЬ ЭТОТ МЕТОД!
    def add_quote_to_book(self, book_id, quote):
        """Добавляет цитату к книге."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO quotes (book_id, quote)
                VALUES (%s, %s)
            """, (book_id, quote))

            conn.commit()
            cur.close()
            conn.close()

            # Обновляем локальный список
            for book in self.books:
                if book.id == book_id:
                    book.quotes.append(quote)
                    break

        except Exception as e:
            print(f"Ошибка добавления цитаты: {e}")

    # ДОБАВЬ ЭТОТ МЕТОД!
    def remove_quote(self, book_id, quote_index):
        """Удаляет цитату по индексу."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            # Получаем все цитаты книги
            cur.execute("SELECT id FROM quotes WHERE book_id = %s ORDER BY id", (book_id,))
            quotes = cur.fetchall()

            if 0 <= quote_index < len(quotes):
                quote_id = quotes[quote_index][0]
                cur.execute("DELETE FROM quotes WHERE id = %s", (quote_id,))
                conn.commit()
                success = True
            else:
                success = False

            cur.close()
            conn.close()

            if success:
                # Обновляем локальный список
                for book in self.books:
                    if book.id == book_id and quote_index < len(book.quotes):
                        book.quotes.pop(quote_index)
                        break

            return success

        except Exception as e:
            print(f"Ошибка удаления цитаты: {e}")
            return False

    # ДОБАВЬ ЭТОТ МЕТОД!
    def export_to_csv(self, filename='library_export.csv'):
        """Экспортирует данные в CSV файл."""
        import csv

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'author', 'year', 'genre', 'quotes'])

            for book in self.books:
                quotes_str = '|'.join(book.quotes)
                writer.writerow([book.title, book.author, book.year, book.genre, quotes_str])

        print(f"Экспортировано {len(self.books)} книг в {filename}")

    def update_book(self, old_book, new_book):
        """Обновляет книгу в БД."""
        try:
            conn = self._connect()
            cur = conn.cursor()

            cur.execute("""
                UPDATE books 
                SET title = %s, author = %s, year = %s, genre = %s
                WHERE id = %s
            """, (new_book.title, new_book.author, new_book.year, new_book.genre, old_book.id))

            conn.commit()
            cur.close()
            conn.close()

            # Обновляем в локальном списке
            for i, book in enumerate(self.books):
                if book.id == old_book.id:
                    self.books[i] = new_book
                    break

        except Exception as e:
            print(f"Ошибка обновления: {e}")