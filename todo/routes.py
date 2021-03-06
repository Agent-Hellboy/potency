import datetime
import os
import secrets

from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user, current_user, login_required, logout_user
from apiclient.discovery import build

from PIL import Image
from todo.scrap import scrape_google
from todo import app, db, bcrypt
from todo.model import User, Todo, Tasks, Tasksum
from todo.forms import RegistrationForm, LoginForm, PostForm, TaskForm, SearchForm
from pyytdata import pyytdata

allowed_extensions = ["jpg", "png", "ppm"]


@app.route("/")
def home():
    print(scrape_google("flask", 3, "en"))
    curr_skill = set()
    todo = Todo.query.all()
    print(todo)
    for i in todo:
        if i.subject == "skill":
            curr_skill.add(i)
    print(curr_skill)
    return render_template("home.html", curr_skill=curr_skill)


def save_and_upload(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    output_size = (125, 125)
    i = Image.open(file)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    pro_pic = url_for("static", filename="profile_pics/" + current_user.image_file)
    if request.method == "POST":
        file = request.files.get("file")
        picture_file = save_and_upload(file)
        current_user.image_file = picture_file
        db.session.commit()
        return redirect(url_for("account"))
    return render_template("account.html", pro_pic=pro_pic)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()

    if request.method == "POST":
        print(request.form.get('username'))
        print(User.query.all())
        print(request.form.get("username"))
        user = User.query.filter_by(email=request.form.get("username")).first()
        print(user)
        if user and bcrypt.check_password_hash(
            user.password, request.form.get("password")
        ):
            login_user(user)
            return redirect(url_for("skills"))
            # print(next_page)
            # print(user.todo)

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # print('account created')
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/skill", methods=["GET", "POST"])
@login_required
def skill():
    curr_user = current_user.id
    todo = Todo.query.filter_by(user_id=curr_user).all()
    skills = []
    for i in todo:
        if i.subject == "skill":
            skills.append(i)
    return render_template("skill.html", skills=skills)


@app.route("/recm", methods=["GET", "POST"])
@login_required
def recm_skill():
    form = SearchForm()
    key_word = ""
    val = request.form.get("val")
    
    if request.method == "POST" and val == "val1":
        key_word = request.form.get("key_word")
        data = pyytdata.PyYtData(key_word,10)
        
        # list to contain info of the video
        items = []
        
        titles = data.get_titles()
        descriptions = data.get_descriptions()
        get_urls = data.get_image_urls()
        get_links = data.get_links()
        data1 = zip(titles,descriptions,get_urls,get_links)
        
        for i in data1:
            var = dict()
            var["title"] = i[0]
            var["description"] = i[1]
            var["image"] = i[2]
            var["link"] = i[3]
            items.append(var)
        # for j in items:
        # 	print(j)
        return render_template("recm_skill.html", val=val, items=items, form=form)
        
    if request.method == "POST" and val == "val2":
        
        key_word = request.form.get("key_word")
        result = scrape_google(key_word, 10, "en")
        items = []
        for i in result:
            var = dict()
            link = i["link"]
            var["title"] = i["title"]
            var["description"] = i["description"]
            var["image"] = None
            items.append(var)
        return render_template("recm_skill.html", items=items, val=val, form=form)
    if request.method == "GET":
        return render_template("recm_skill.html", form=form)
    return render_template("recm_skill.html", form=form)


@app.route("/skills", methods=["GET", "POST"])
@login_required
def skills():
    curr_user = current_user.id
    todo = Todo.query.filter_by(user_id=curr_user).all()
    # print(todo)
    todorev = []
    for i in todo:
        if (
            i.date.day + 7 == datetime.datetime.now().date().day
            or i.date.day + 3 == datetime.datetime.now().date().day
            or i.date.day % 15 == datetime.datetime.now().date().day
        ):
            todorev.append(i)

    #
    return render_template("skills.html", todo=todo, todorev=todorev)


@app.route("/skill/insert", methods=["GET", "POST"])
@login_required
def insert_todo():
    form = PostForm()
    if request.method == "POST":
        title = request.form.get("title")
        subject = request.form.get("subject")
        content = request.form.get("content")
        user = Todo(
            title=title, subject=subject, content=content, user_id=current_user.id
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("insert_todo.html", form=form)


@app.route("/skills/tasks", methods=["GET", "POST"])
@login_required
def about_task():
    var = request.args.get("my_var")
    task = Tasks.query.filter_by(todo_id=var).all()
    print(var)
    return render_template("about_task.html", task=task, var=var)


@app.route("/todo/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    var = request.args.get("my_var")
    if request.method == "POST":
        title = request.form.get("title")
        user = Tasks(title=title, todo_id=var)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html")


@app.route("/todo/task_desc", methods=["GET", "POST"])
@login_required
def task_desc():
    var = request.args.get("my_var")
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        taskdesc = Tasksum(title=title, description=description, task_id=var)
        db.session.add(taskdesc)
        db.session.commit()
        return render_template("task_desc.html")
    return render_template("task_desc.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
