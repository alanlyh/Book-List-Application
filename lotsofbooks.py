from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Book, User

engine = create_engine('postgresql:///books')
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

user = User(id="112992310265322312899", name="Yuanhao Lu")

session.add(user)
session.commit()

# Books for big data
category1 = Category(name="big data", desc="big data book list", user=user)

session.add(category1)
session.commit()

desc1 = '''
Data is at the center of many challenges in system design today.
Difficult issues need to be figured out, such as scalability,
consistency, reliability, efficiency, and maintainability.
In addition, we have an overwhelming variety of tools, including
relational databases, NoSQL datastores, stream or batch
processors, and message brokers. What are the right choices
for your application? How do you make sense
of all these buzzwords?\n

In this practical and comprehensive guide, author Martin Kleppmann
helps you navigate this diverse landscape by examining the pros
and cons of various technologies for processing and storing data.
Software keeps changing, but the fundamental principles remain
the same. With this book, software engineers and architects will
learn how to apply those ideas in practice, and how to make
full use of data in modern applications.\n

Peer under the hood of the systems you already use, and learn
how to use and operate them more effectively\n
Make informed decisions by identifying the strengths and
weaknesses of different tools\n
Navigate the trade-offs around consistency, scalability,
fault tolerance, and complexity\n
Understand the distributed systems research upon which modern
databases are built\n
Peek behind the scenes of major online services, and learn
from their architectures
'''

book1 = Book(
    name="Designing Data-Intensive Applications",
    author="Martin Kleppmann",
    category=category1,
    desc=desc1,
    user=user
)

session.add(book1)
session.commit()

desc2 = '''
Apache Spark is amazing when everything clicks. But if you
haven't seen the performance improvements you expected, or
still don't feel confident enough to use Spark in production,
this practical book is for you. Authors Holden Karau and
Rachel Warren demonstrate performance optimizations to
help your Spark queries run faster and handle
larger data sizes, while using fewer resources.\n

Ideal for software engineers, data engineers, developers,
and system administrators working with large-scale data
applications, this book describes techniques that can
reduce data infrastructure costs and developer hours.
Not only will you gain a more comprehensive understanding
of Spark, you'll also learn how to make it sing.\n

With this book, you'll explore:\n

How Spark SQL's new interfaces improve performance
over SQL's RDD data structure\n
The choice between data joins in Core Spark and Spark SQL\n
Techniques for getting the most out of standard RDD transformations\n
How to work around performance issues in Spark's key/value pair paradigm\n
Writing high-performance Spark code without Scala or the JVM\n
How to test for functionality and performance when
applying suggested improvements\n
Using Spark MLlib and Spark ML machine learning libraries\n
Spark's Streaming components and external community packages
'''

book2 = Book(
    name="High Performance Spark",
    author="Holden Karau & Rachel Warren",
    category=category1,
    desc=desc2,
    user=user
)

session.add(book2)
session.commit()

# Books for Javascript
category1 = Category(name="JavaScript", desc="JS book list", user=user)

session.add(category1)
session.commit()

desc1 = '''
If you're like most developers, you rely heavily on
JavaScript to build interactive and quick-responding web
applications. The problem is that all of those lines of
JavaScript code can slow down your apps. This book reveals
techniques and strategies to help you eliminate performance
bottlenecks during development. You'll learn how to
improve execution time, downloading, interaction with
the DOM, page life cycle, and more.\n

Yahoo! frontend engineer Nicholas C. Zakas and five
other JavaScript experts-Ross Harmes, Julien Lecomte,
Steven Levithan, Stoyan Stefanov, and Matt Sweeney-demonstrate
optimal ways to load code onto a page, and offer programming
tips to help your JavaScript run as efficiently and quickly
as possible. You'll learn the best practices
to build and deploy your files to a production environment,
and tools that can help you find problems once your site goes live.\n

Identify problem code and use faster alternatives to
accomplish the same task\n
Improve scripts by learning how JavaScript stores and accesses data\n
Implement JavaScript code so that it doesn't slow down
interaction with the DOM\n
Use optimization techniques to improve runtime performance\n
Learn ways to ensure the UI is responsive at all times\n
Achieve faster client-server communication\n
Use a build system to minify files, and HTTP compression to
deliver them to the browser
'''

book1 = Book(
    name="High Performance JavaScript",
    author="Nicholas C. Zakas",
    category=category1,
    desc=desc1,
    user=user
)

session.add(book1)
session.commit()

desc2 = '''
No matter how much experience you have with JavaScript,
odds are you don't fully understand the language. As part of
the "You Don't Know JS" series, this concise yet in-depth
guide focuses on new asynchronous features and performance
techniques-including Promises, generators, and Web Workers-that
let you create sophisticated single-page web applications and
escape callback hell in the process.\n

Like other books in this series, You Don't Know JS: Async & Performance
dives into trickier parts of the language that many JavaScript
programmers simply avoid. Armed with this knowledge, you can
become a true JavaScript master.\n

With this book you will:\n

Explore old and new JavaScript methods for handling
asynchronous programming\n
Understand how callbacks let third parties control your
program's execution\n
Address the "inversion of control" issue with JavaScript Promises\n
Use generators to express async flow in a sequential,
synchronous-looking fashion\n
Tackle program-level performance with Web Workers, SIMD, and asm.js\n
Learn valuable resources and techniques for benchmarking and
tuning your expressions and statements
'''


book2 = Book(
    name="You Don't Know JS: Async & Performance",
    author="Kyle Simpson",
    category=category1,
    desc=desc2,
    user=user
)

session.add(book2)
session.commit()

print "added books!"
