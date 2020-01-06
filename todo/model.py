from todo import db,login_manager
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    todo=db.relationship('Todo',backref='user',lazy=True)
    def __repr__(self):
    	return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Todo(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	subject=db.Column(db.String(100),nullable=False)
	date=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
	content=db.Column(db.Text,nullable=False)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	task=db.relationship('Tasks',backref='todo',lazy=True)

	def __repr__(self):
		return f"Todo('{self.id}' '{self.title}','{self.subject}','{self.date}','{self.content}','{self.user_id}')"

class Tasks(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	date=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
	todo_id=db.Column(db.Integer,db.ForeignKey('todo.id'),nullable=False)
	tasksum=db.relationship('Tasksum',backref='todo',lazy=True)
	def __repr__(self):
		return f"Task('{self.title}','{self.date}','{self.todo_id}')"

class Tasksum(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	description=db.Column(db.Text(20000),nullable=False)
	date=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
	task_id=db.Column(db.Integer,db.ForeignKey('tasks.id'),nullable=False)

	def __repr__(self):
		return f"Task('{self.title}','{self.description}')"