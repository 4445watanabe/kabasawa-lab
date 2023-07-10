from flask import Flask, render_template, request, Response, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# ライブラリの追加
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "db"
DB_NAME = "flask_app"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO']=True
app.secret_key = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# ログイン機能の有効化
login = LoginManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    age = db.Column(db.Integer)
    # 認証を行うためメールアドレスとパスワードカラムを追加
    mail = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(128), nullable=False)
    # パスワードをハッシュ化
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
    def check_password(self, password):
            return check_password_hash(self.password, password)
#問題用のDB
class Question(db.Model):
    __tablename__="questions"
    id = db.Column(db.Integer, primary_key = True)
    question_text = db.Column(db.String(128), unique=True, nullable=False)
    choices = db.relationship('Choice', backref='question', lazy=True) 

#答え用のDB
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    choice_text = db.Column(db.String(128), unique=True, nullable=False)
    is_correct = db.Column(db.Boolean)
    question = db.relationship('Question', backref='choices')

@login.user_loader
def load_user(id):
    # ログイン機能からidを受け取った際、DBからそのユーザ情報を検索し、返す
    return User.query.get(int(id))



@app.route("/",methods=['GET'])
@login_required
def index_get():
    #ユーザーが教員か生徒か
    if current_user.role == 'teacher':
        return redirect('/index_teacher')
    elif current_user.role == 'student':
        return redirect('/index_student')
    return render_template('index.html')
    


@app.route('/login', methods=['GET'])
def login_get():
  # 現在のユーザーがログイン済みの場合
  if current_user.is_authenticated:
    # トップページに移動
    return redirect(url_for('index_get'))
    #ユーザーが教員か生徒か
    if user.role == 'teacher':
        return redirect('/index_teacher')
    elif user.role == 'student':
        return redirect('/index_student')
  
  # loginページのテンプレートを返す
  return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    user = User.query.filter_by(mail=request.form["mail"]).one_or_none()
    
    # ユーザが存在しない or パスワードが間違っている時
    if user is None or not user.check_password(request.form["password"]):
        # メッセージの表示
        flash('メールアドレスかパスワードが間違っています')
        # loginページへリダイレクト
        return redirect(url_for('login_get'))

    # ログインを承認
    login_user(user)
    # トップページへリダイレクト
    return redirect(url_for('index_get'))


#教員・生徒でログイン後の画面を切り分ける
@app.route('/index_teacher')
@login_required
def teacher_page():
    return render_template('index_teacher.html')

@app.route('/index_student')
@login_required
def student_page():
    return render_template('index_student.html')

@app.route('/logout')
def logout():
  # logout_user関数を呼び出し
  logout_user()
  # トップページにリダイレクト
  return redirect(url_for('index_get'))


@app.route("/users",methods=['GET'])
def users_get():
    users = User.query.all()
    return render_template('users_get.html', users=users)


@app.route("/users",methods=['POST'])
def users_post():
    #mailカラムの追加
    user = User(
        name=request.form["user_name"],
        age=request.form["user_age"],
        mail=request.form["mail"],
        role=request.form["user_role"]
    )
    #パスワードを安全に保存
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users_get'))


#クイズ作成
@app.route("/quiz",methods=['POST'])
def quiz_post():
    questions = Question(
        question_text = request.form["a"]
    )
    questions.choices=[
        Choice(
            question_id = request.form["b"],
            choice_text = request.form["c"],
            is_correct = request.form["d"]
        ),
        Choice(
            question_id = request.form["a"],
            choice_text = request.form["a"],
            is_correct = request.form["a"]
        ),
        Choice(
            question_id = request.form["a"],
            choice_text = request.form["a"],
            is_correct = request.form["a"]
        ),
        Choice(
            question_id = request.form["a"],
            choice_text = request.form["a"],
            is_correct = request.form["a"]
        ),
    ]
    db.session.add(questions)
    db.session.commit()
    return render_template('quiz.html')
    
@app.route("/question",methods=['GET'])
def questions_get():
    question = Question.query.all()
    return render_template()

@app.route("/users/<id>",methods=['GET'])
@login_required
def users_id_get(id):
    # ログインユーザのIDを取得し、自分の個別ページのみ開けるようにする
    if str(current_user.id) != str(id):
        return Response(response="他人の個別ページは開けません", status=403)
    user = User.query.get(id)
    return render_template('users_id_get.html', user=user)

@app.route("/users/<id>/edit",methods=['POST'])
def users_id_post_edit(id):
    user = User.query.get(id)
    user.name = request.form["user_name"]
    user.age = request.form["user_age"]
    user.role = request.form["user_role"]
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('users_get'))

@app.route("/users/<id>/delete",methods=['POST'])
def users_id_post_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_get'))

@app.route("/question")
def question():
    return render_template('question.html')

@app.route("/results")
def results():
    return render_template('results.html')

@app.route("/quiz")
def quiz_page():
    return render_template('quiz.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)