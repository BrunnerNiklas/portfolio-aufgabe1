from sqlalchemy import Column, Integer, String
from base import Base


class Searchresult(Base):
    __tablename__ = "searchresults"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    title = Column(String)
    text = Column(String)

    # Print-Methode der Klasse; Für die Datenbank/Tabelle nicht notwendig.
    def printSearchresult(self):
        print(self.id)
        print(self.date)
        print(self.title)
        print(self.text)