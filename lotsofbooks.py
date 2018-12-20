from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Category, Book
 
engine = create_engine('sqlite:///books.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Books for big data
category1 = Category(name="big data")

session.add(category1)
session.commit()

book1 = Book(name="Designing Data-Intensive Applications", author="Martin Kleppmann", category=category1)

session.add(book1)
session.commit()

book2 = Book(name="High Performance Spark", author="Holden Karau & Rachel Warren", category=category1)

session.add(book2)
session.commit()


# Books for Javascript
category1 = Category(name="JavaScript")

session.add(category1)
session.commit()

book1 = Book(name="High Performance JavaScript", author="Nicholas C. Zakas", category=category1)

session.add(book1)
session.commit()

book2 = Book(name="You Don't Know JS: Async & Performance", author="Kyle Simpson", category=category1)

session.add(book2)
session.commit()



print "added books!"

