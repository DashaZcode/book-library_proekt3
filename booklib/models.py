class Book:
    def __init__(self, title, author, year, genre, quotes=None):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.quotes = quotes or []
        self.id = None

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'genre': self.genre,
            'quotes': self.quotes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            genre=data['genre'],
            quotes=data.get('quotes', [])
        )

    def __str__(self):
        return f"'{self.title}' - {self.author} ({self.year})"