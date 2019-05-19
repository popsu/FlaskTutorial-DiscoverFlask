from project import db
from models import User

# insert data
db.session.add(User('tommi', 'tommi@testdomain.com', 'salasana'))
db.session.add(User('testuser2', 'test@user2.com', 'salasana'))
db.session.add(User('admin', 'ad@min.com', 'admin'))

# commit the changes
db.session.commit()
