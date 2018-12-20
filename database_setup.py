from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    desc = Column(String(400))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id' : self.id,
           'name' : self.name,
           'desc' : self.desc,
       }
 
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    author = Column(String(250))
    desc = Column(String(400))
    # user_id = Column(String(250), ForeignKey('user.id'))
    # user = relationship(User)
    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id' : self.id,
           'name' : self.name,
           'author' : self.author,
           'desc' : self.desc
       }

# class User(Base):
#     __tablename__ = 'user'

#     id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///books.db')
 

Base.metadata.create_all(engine)
