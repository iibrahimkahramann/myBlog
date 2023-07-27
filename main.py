from flask import Flask, jsonify, request, render_template
from datetime import datetime
import sqlite3

created_on = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

app = Flask(__name__, '/assets', 'assets')

@app.route('/')
def home():
    return render_template('index.html')




@app.route('/blog/<int:post_id>')
def blog(post_id):
    blog_data = []
    with sqlite3.connect('myblog.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
        row = cursor.fetchone()

        if row is None:
            return "Post not found.", 404

        blog_data = {
            'title': row[1],
            'content': row[3],
            'created_on': row[5]
        }

    return render_template('post.html', blog_data=blog_data)



@app.route('/project')
def project():
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
                'summary': row[2],
                'content': row[3],
                'img': row[4]
            })
    return render_template('project.html', posts=blog_data)




@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['msg']
        if name == '' or email == '' or msg == '':
            return jsonify({'message': 'error'})
        else: 
            created_on = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            conn = sqlite3.connect('myblog.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contacts (name, email, msg, created_on) VALUES (?, ?, ?, ?)', (name, email, msg, created_on))
            conn.commit()
            conn.close()
            return jsonify({'message': 'success'})
    return render_template('contact.html')


@app.route('/contact-add', methods=['POST'])
def contactMeUser():
    name = request.form['name']
    email = request.form['email']
    msg = request.form['msg']
    created_on = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    conn = sqlite3.connect('myblog.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, email, msg, created_on) VALUES (?, ?, ?, ?)', (name, email, msg, created_on))
    conn.commit()
    conn.close()
    return render_template('contact.html')

   






@app.route('/admin')
def admin():
    return render_template('admin.html')



@app.route('/admin-add', methods=['GET', 'POST'])
def blog_add():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        img = request.form['img']
        content = request.form['content']
        created_on = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        conn = sqlite3.connect('myblog.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title,summary,img, content, created_on) VALUES (?, ?, ?)',(title,summary,img, content, created_on))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    return render_template('admin.html')


if __name__ == '__main__':
    app.run()