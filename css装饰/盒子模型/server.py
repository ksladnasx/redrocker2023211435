import sqlite3
from flask import Flask #引入flsak包中的Flask类
from flask import render_template #引入flsak包中的render_template类
app = Flask(__name__) #如果请求根目录url，就访问下面的方法
def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

app = Flask(__name__) #如果请求根目录url，就访问下面的方法
@app.route('/')
def index():#指定当前网页要使用的xxxx.html网页
    return render_template("边框圆角与案例.html")


if __name__ == '__main__':
    app.run("0.0.0.0")
@app.route('/about')
def about():
    return render_template('实战演练1.html')