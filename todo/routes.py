from flask import render_template,flash,url_for,redirect,request
from todo import app,db,bcrypt
from todo.model import User
from todo.forms import RegistrationForm,LoginForm
from flask_login import login_user,current_user,login_required,logout_user

todo={
	'title':'solve one question',
	'priority':'urgent'
}

@app.route('/')
def home():
	return render_template('home.html',todo=todo)

@app.route('/account')
@login_required
def account():
	return render_template('account.html')


@app.route('/login',methods=['GET','POST'])
def login():
	if(current_user.is_authenticated):
		return	redirect(url_for('home'))
	form=LoginForm()
	if(request.method=='POST'):
		#print(request.form.get('username'))
		user=User.query.filter_by(email=request.form.get('username')).first()
		#print(user)
		if user and bcrypt.check_password_hash(user.password,request.form.get('password')):
				login_user(user)
				next_page=request.args.get('next')
				return redirect(next_page) if nextpage else redirect(url_for('account'))	
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
	
	
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')
	
	
	
