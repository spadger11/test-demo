from flask import Flask,  request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# MySQl所在的主机名
HOSTNAME = "127.0.0.1"
# MySQl监听的端口号，默认3306
PORT = "3306"
# 连接MySQl的用户名，读者用自己设置的
USERNAME = "root"
# 连接MySQl密码，读者用自己的
PASSWORD = "147258"
# MySQl上创建的数据库名称
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/" \
                                        f"{DATABASE}?charset=utf8mb4"
# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy（app）创建一个db对象
# SQLAlchemy会自动读取app.config中连接的数据库信息
db = SQLAlchemy(app)  # 数据库连接配置
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute("select 1")
#         print(rs.fetchone())  # (1,)
migrate = Migrate(app, db)


# ORM模型

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # author = db.relationship("Article", back_populates="articles")


# user = User(username="草莓糯米糍", password='11111')
# sql:insert user(username,password) value("法外狂徒张三", "11111");
class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者的外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # author = db.relationship("User", back_populates="articles")
    # backref：会自动的给User模型添加一个articles的属性，用来获取文章列表
    author = db.relationship("User", backref="articles")


article = Article(title="若风未拾花", content="陨星")
# article.author_id = user.id
# user = User.query.get(article.author_id) 自动做了
# print(article.author)
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return render_template("child1.html")


@app.route("/user/add")
def add_user():
    # 1、创建OMR对象
    user = User(username="草莓糯米糍", password='1111111')
    # 2、将ORM 对象添加到db.session中
    db.session.add(user)
    # 3、将db.session中的改变同步到数据库中
    db.session.commit()
    return "用户创建成功"


@app.route("/user/query")
def query_user():
    # 1、get 查找：根据主键查找
    # user = User.query.get(1)
    # print(f"{user.id}:{user.username}-{user.password}")
    # 2、filter_by查找
    # Query :类数组
    users = User.query.filter_by(username="草莓糯米糍")
    for user in users:
        print(user.username)
    return "数据查找成功"
# @app.route("/static")
# def static_demo():
#     return render_template("static.html")


@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="草莓糯米糍").first()
    user.password = "222222"
    db.session.commit()
    return "数据修改成功"


@app.route('/user/delate')
def delete_user():
    # 1、查找
    user = User.query.get(1)
    # 2、从db.session 中删除
    db.session.delete(user)
    # 3、将db.session中修改，同步到数据库中
    db.session.commit()
    print("")
    return "数据删除成功"


if __name__ == '__main__':
    app.run()
