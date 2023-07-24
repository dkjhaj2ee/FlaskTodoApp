from flask import Flask, render_template, request
from db.db import db, Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()

    return render_template('index.html', todos = allTodo)

@app.route('/edit/<int:sno>')
def edit(sno):
    current_item = Todo.query.filter_by(sno=sno).first()
    allTodo = Todo.query.all()

    return render_template('index.html', todos = allTodo, current_item=current_item)

@app.route('/update/', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        sno = request.form['sno']

        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()

    return render_template('index.html', todos = allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    allTodo = Todo.query.all()

    return render_template('index.html', todos = allTodo)


if __name__ == "__main__":
    app.run(debug=True)