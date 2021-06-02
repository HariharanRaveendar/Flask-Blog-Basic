from flask import Flask,render_template,request,redirect,url_for
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login,Article
from datetime import datetime
import base64
 
app = Flask(__name__)
app.secret_key = 'xyz'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()


@app.route("/")
def index():
    all_posts = Article.query.order_by(Article.date).all()
    return render_template('index.html',posts=all_posts)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')
    return render_template('login.html')
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
        if password == password2:
            user = UserModel(firstname=firstname,lastname=lastname,email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html')

@app.route('/post')
def post():
    return render_template('dashboard.html')

@app.route('/addpost/<int:id>')
def addpost(id):
    all_posts = Article.query.order_by(Article.date).filter_by(user_id=id).all()
    return render_template('addarticle.html', posts=all_posts)

@app.route('/update/<int:id>')
def update(id):
    update=Article.query.get_or_404(id)
    return render_template('updatearticle.html',update=update)
@app.route('/updatearticle/<int:id>',methods=['POST'])
def updatearticle(id):
    if request.method == 'POST':
        data = Article.query.get_or_404(id)
        data.Title = request.form['title']
        data.SubTitle = request.form['subtitle']
        data.Subject = request.form['subject']
        data.Body = request.form['body']
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    data_del = Article.query.get_or_404(id)
    db.session.delete(data_del)
    db.session.commit()
    return redirect(url_for('index'))
@app.route('/addarticle/<int:id>', methods=['POST'])
def addarticle(id):
    data = UserModel.query.get_or_404(id)
    print(data.firstname)
    if request.method == 'POST':
        Title = request.form['title']
        SubTitle = request.form['subtitle']
        Subject = request.form['subject']
        Body = request.form['body']
        articleimg = request.files['img'].read()
        post = Article(Title=Title, SubTitle=SubTitle, Subject=Subject, Body=Body,articleimg=articleimg, date=datetime.now(),user_id=id,FirstName=data.firstname,LastName=data.lastname)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

@app.route("/read/<int:id>")
def read(id):
    read = Article.query.get_or_404(id)
    return render_template('read.html',read=read)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.template_filter('img')
def img(a):
    # print(str(base64.b64encode(a),'utf-8'))
    return str(base64.b64encode(a),'utf-8')