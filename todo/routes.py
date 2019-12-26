from flask import render_template,flash,url_for,redirect,request
from todo import app,db,bcrypt
from todo.model import User,Todo,Tasks
from todo.forms import RegistrationForm,LoginForm,PostForm,TaskForm,SearchForm
from flask_login import login_user,current_user,login_required,logout_user
from apiclient.discovery import build

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/account')
@login_required
def account():
	curr_user = current_user.id
	todo=Todo.query.filter_by(user_id=curr_user).all()
	#print(todo)
	skills=[]
	for i in todo:
		if(i.subject=='skill'):
			skills.append(i)
	print(skills)
	return render_template('account.html',todo=todo,skills=skills)


@app.route('/login',methods=['GET','POST'])
def login():
	if(current_user.is_authenticated):
		return	redirect(url_for('home'))
	form=LoginForm()
	print(form.validate_on_submit())
	if(request.method=='POST'):
		print(request.form.get('username'))
		user=User.query.filter_by(email=request.form.get('username')).first()
		#print(user)
		if user and bcrypt.check_password_hash(user.password,request.form.get('password')):
				login_user(user)
				next_page=request.args.get('next')
				#print(next_page)
				#print(user.todo)
				return redirect(next_page) if next_page else redirect(url_for('skill',var=user.todo))	
	return render_template('login.html',form=form)


@app.route('/register',methods=['GET','POST'])
def register():
	if(current_user.is_authenticated):
		return	redirect(url_for('home'))
	form=RegistrationForm()
	if(request.method=='POST'):
		username=request.form.get('username')
		email=request.form.get('email')
		password=request.form.get('password')
		confirm=request.form.get('confirm')
		hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
		user=User(username=username,email=email,password=hashed_password)
		db.session.add(user)
		db.session.commit()	
		print('account created')
		return redirect(url_for('login'))
	return render_template('register.html',form=form)
	
	
@app.route("/skill",methods=['GET','POST'])
@login_required
def skill():
	
	return render_template('skill.html')


@app.route("/recm",methods=['GET','POST'])
@login_required
def recm_skill():
	form=SearchForm()
	key_word=''
	if(request.method=='POST'):
		key_word=request.form.get('key_word')
	api_key='AIzaSyBwDMpvqtUxZ6ZsAZ_VxspbuATh-CncRWA'
	youtube=build('youtube','v3',developerKey=api_key)
	req=youtube.search().list(q=key_word,part='snippet',type='video',maxResults=10)
	result=req.execute()
	links=[]
	for i in result['items']:
		link='https://www.youtube.com/watch?v='+i['id']['videoId']
		links.append(link)
	for j in links:
		print(link)
	return render_template('recm_skill.html',links=links,form=form)


@app.route("/skill/insert",methods=['GET','POST'])
@login_required
def insert_todo():
	form=PostForm()
	if(request.method=='POST'):
		title=request.form.get('title')
		subject=request.form.get('subject')
		content=request.form.get('content')
		user=Todo(title=title,subject=subject,content=content,user_id=current_user.id)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('insert_todo.html',form=form)

@app.route("/todo/add_task",methods=['GET','POST'])
@login_required
def add_task():
	form=TaskForm()
	if(request.method=='POST'):
		title=request.form.get('title')
		time=request.form.get('appt')
		user=Tasks(title=title,time=time,todo_id=1)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('add_task.html',form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')