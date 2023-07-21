from flask import Flask, jsonify, request, render_template
from datetime import datetime
import sqlite3

created_on = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

app = Flask(__name__, '/assets', 'assets')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/post')
def all_post():
    blog_data = []
    with sqlite3.connect('myblog.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM posts')
        rows = cursor.fetchall()

        if rows is None:
            return "Post not found.", 404

        for row in rows:
            blog_data.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
            })

    return render_template('index.html', posts=blog_data)


@app.route('/post/<int:post_id>')
def post_id(post_id):
    blog_data = []
    with sqlite3.connect('myblog.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
        row = cursor.fetchone()

        if row is None:
            return "Post not found.", 404

        blog_data = {
            'title': row[2],
            'content': row[3],
            'created_on': row[4]
        }

    return render_template('post.html', blog_data=blog_data)







@app.route('/contact')
def contact():
    return render_template('contact.html')







@app.route('/admin')
def admin():
    return render_template('admin.html')



@app.route('/admin-add', methods=['GET', 'POST'])
def blog_add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        created_on = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO post (title, description, created_on) VALUES (?, ?, ?)',(title, description, created_on))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    return render_template('admin.html')
