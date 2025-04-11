
class NewsItem:
    date=None
    header=None
    changes=None
    def __init__(self, date: str, header: str, changes: list):
        self.date = date
        self.header = header
        self.changes = changes
