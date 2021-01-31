from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib
import pyodbc
from sqlalchemy import Column, Integer, String, TEXT
from flask_cors import CORS
import random

from sqlalchemy.sql.expression import false


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# conn_str = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=.\SQLEXPRESS;DATABASE=PostDB;Trusted_Connection=yes;')
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={conn_str}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(TEXT, nullable=False)
    author = Column(String(50), nullable=False, default='N/A')
    date_posted = Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Blog post {self.id}"

try:
    db.create_all()
except Exception as ex:
    print(ex)


# db.session.add(BlogPost(title = 'Post 2', content='Content of post 2', author = 'Aaron'))
# db.session.commit()

# print(BlogPost.query.all())
# print(BlogPost.query.all()[0].date_posted)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home/user/<string:name>/posts/<int:id>')
def hello(name, id):
    return f'hello {name} : {id}'


@app.route('/onlyget', methods=['GET'])
def get_req():
    return 'Only allow get request'


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=request.form['author'] or 'AAA')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        # posts = BlogPost.query.filter_by(title='Post 2').order_by(BlogPost.date_posted).all()
        posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=posts)


@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("edit.html", post=post) 
jobs = [
        { 'title': "Niinja UX Designer", 'id': 1, 'details': "lorem" },
        { 'title': "Niinja Web Developer", 'id': 2, 'details': "lorem" },
        { 'title': "Niinja Vue Developer", 'id': 3, 'details': "lorem" },
        { 'title': "Niinja", 'id': 4, 'details': "lorem" },
        { 'title': "Nijia", 'id': 5, 'details': "loram"}
    ]

@app.route('/jobs', methods=['GET'])
def get_jobs():
    return jsonify(jobs)
    
@app.route('/jobs/<int:id>', methods=['GET'])
def get_jobs_by_id(id):
    print('get_jobs_by_id')
    # job = filter(lambda x: x['id'] == id, jobs)
    # return jsonify(list(job)[0])
    job = next(x for x in jobs if x['id'] == id)
    return jsonify(job)

@app.route('/quick-math/<int:total>/<int:sum>', methods=['GET'])
def get_quick_math(total, sum):
    count = 0
    lst = []
    while count < total:
        a = random.randint(2, sum - 2)
        b = random.randint(2, sum - a)
        r = a + b
        lst.append({'a': a, 'b': b, 'r': r, 'id': count, 'p': 0 })
        count += 1
    return jsonify(lst)
    


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
