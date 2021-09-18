from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Todos
from . import db

views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
	return render_template('index.html', user = current_user, todos = Todos.query.all())


@views.route('/add-todo', methods = ['GET', 'POST'])
@login_required
def add_todo():
	if request.method == 'POST':
		todo = request.form.get('todo')
		if not todo:
			flash('It can not be left empty!!')
		else:
			new_todo = Todos(todo = todo, author = current_user.id)
			db.session.add(new_todo)
			db.session.commit()
			flash('Added Successfully!')
			return redirect(url_for('views.home'))

	return render_template('todos.html', user = current_user, todos = Todos.query.all())

@views.route('/delete-todo/<id>')
def delete_todo(id):
	todo = Todos.query.filter_by(id=id).first()
	if not todo:
		flash('Todo does not exist!!')
	elif current_user.id != todo.author:
		flash('permission denied!!')
	else:
		db.session.delete(todo)
		db.session.commit()
		flash('Todo deleted successfully!')

	return redirect(url_for('views.home'))