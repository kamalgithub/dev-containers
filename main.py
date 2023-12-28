from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from sqlalchemy import DateTime, Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URL')
app.secret_key = getenv('SECRET_KEY')

db = SQLAlchemy()

class Todos(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

db.init_app(app)
with app.app_context():
    db.create_all()

@app.get('/')
def home():
    return render_template('index.html', todos=Todos.query.all())

@app.post('/')
def todo():
    todo = Todos(title = request.form.get('title'), description = request.form.get('description'))
    db.session.add(todo)
    db.session.commit()
    return render_template('index.html', todos=Todos.query.all())

@app.get('/<int:id>/<status>')
def complete(id, status):
    status = True if status == 'true' else False
    todo = Todos.query.filter_by(id=id).first()
    if todo:
        todo.done = status
        db.session.commit()

    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)