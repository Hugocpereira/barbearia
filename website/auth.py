from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from .models import User
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

 
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha1 = request.form.get('senha1', '')
        
        user = User.query.filter_by(email=email).first()
        if user and senha1 and check_password_hash(user.senha1, senha1):
            flash('Login feito com sucesso', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))  
        else:
            flash('Usuário não cadastrado', category='error')    
    return render_template('login.html')


@auth.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')
        
        
        email_exists = User.query.filter_by(email=email).first()
        
        if email_exists:
            flash('E-mail já cadastrado', category='error')
        elif senha1 != senha2:
            flash('As senhas devem ser iguais', category='error')
        
        else:
            new_user = User(email=email, nome=nome, senha1 = generate_password_hash(senha1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Cadastrado com sucesso')
            return redirect(url_for('views.home'))
    return render_template('cadastro.html')