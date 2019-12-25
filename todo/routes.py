from flask import render_template,flash,url_for,redirect,request
from todo import app,db,bcrypt
from todo.model import User,Todo
from todo.forms import RegistrationForm,LoginForm,PostForm
from flask_login import login_user,current_user,login_required,logout_user


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/account')
@login_required
def account():
	curr_user = current_user.id
	todo=Todo.query.filter_by(user_id=curr_user).all()
	#print(todo)
	return render_template('account.html',todo=todo)


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
				return redirect(next_page) if next_page else redirect(url_for('account',var=user.todo))	
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
	
	
@app.route("/todo/insert",methods=['GET','POST'])
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')