from sqlalchemy import Column, Integer, String, JSON, ARRAY, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Coffee(Base):
    __tablename__ = 'coffee'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(ARRAY(String))  # массив строк


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    has_sale = Column(Boolean, default=False)
    address = Column(JSON)  # JSON объект
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship('Coffee', backref='users')
    patronomic = Column(String(50), nullable=True)
