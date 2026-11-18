from flask_sqlalchemy import SQLAlchemy

# Создаем объект базы данных
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True) # Имя (логин)
    room_number = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), default='student') # 'student' или 'admin'
    password_hash = db.Column(db.String(200), nullable=False) # Хеш пароля

    def __repr__(self):
        return f"<User {self.name}>"