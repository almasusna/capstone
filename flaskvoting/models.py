from flaskvoting import db, login_manager
from datetime import datetime
from flask_login import UserMixin
#imort scantegrityy

#scan = Scantegrity(1000,5,3)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	
	# codes = scan.table2[ ]
	# send them the form to 
	def __repr__(self):
		return "User('{}','{}')".format(self.username, self.email)
		
