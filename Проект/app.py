from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# --- Настройки ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dorm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-dorm-key'  # Нужен для сессий

db.init_app(app)


# --- Маршруты ---

@app.route('/')
def index():
    # Защита: если нет сессии, кидаем на логин
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return f"<h1>Привет, {session['user_name']}!</h1><p>Ты в системе.</p><a href='/logout'>Выйти</a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        if user and check_password_hash(user.password_hash, password):
            # Создаем сессию
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            return redirect(url_for('index'))
        else:
            flash('Неверное имя или пароль', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room_number']
        password = request.form['password']

        # Проверка на существование
        if User.query.filter_by(name=name).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return redirect(url_for('register'))

        # Хеширование пароля и сохранение
        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, room_number=room, password_hash=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация успешна! Теперь войдите.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()  # Очищаем сессию
    return redirect(url_for('login'))


# --- Инициализация БД (Запускается один раз при старте) ---
def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.first():
            admin = User(name="admin", room_number="301", role="admin",
                         password_hash=generate_password_hash("12345"))
            db.session.add(admin)
            db.session.commit()
            print("База создана. Тестовый юзер: admin / 12345")


if __name__ == '__main__':
    init_db()
    app.run(debug=True)