
class NewsItem:
    date=None
    header=None
    changes=None
    isVersionUpdate=True
    andMore=True
    def __init__(self, date: str, header: str, changes: list, isVersionUpdate: bool = True, andMore: bool = True):
        self.date = date
        self.header = header
        self.changes = changes
        self.isVersionUpdate = isVersionUpdate
        self.andMore = andMore
