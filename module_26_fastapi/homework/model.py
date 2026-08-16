from sqlalchemy import Column, Integer, String, Float, JSON, Text
from sqlalchemy.orm import declarative_base


class Base(declarative_base):
    pass


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    count_look = Column(Integer, nullable=False, default=0)
    time_rice = Column(Integer, nullable=False)
    ingredients = Column(JSON, nullable=False)
    text = Column(Text, nullable=False)

    def add_view(self):
        self.count_look += 1
