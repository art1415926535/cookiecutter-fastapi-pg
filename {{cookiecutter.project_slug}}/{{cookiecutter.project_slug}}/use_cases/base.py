from databases import Database


class DatabaseUseCase:
    def __init__(self, db: Database):
        self.db = db
