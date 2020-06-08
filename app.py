"""
Commands used - 
python -m venv venv
venv\Scripts\activate.bat
pip install flask
pip install flask-sqlalchemy

creating the db related files:
1. first start python env by typing "python"
2. execute "from app import db"
3. db.create_all()

This will  create the db file and we are good to go
"""



from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)


#how to get variable values from the URL - DYNAMIC URL
# @app.route('/home/<string:name>', methods=['GET','POST'])
# def welcome(name):
#     return "Welcome to my web app "+ name

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        
        return addToDB(post_title,post_content,post_author)
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts = all_posts)

#delete an existing post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

#create a new post
@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        
        return addToDB(post_title,post_content,post_author)
    else:
        return render_template('new_post.html')

#edit an existing post
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']    
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)

# add the post to DB
def addToDB(p_title, p_content,p_author):
    new_post = BlogPost(title= p_title, content = p_content, author = p_author)
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')


if __name__ == "__main__":
    app.run(debug=True)