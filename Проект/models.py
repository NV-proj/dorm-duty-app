from flask_sqlalchemy import SQLAlchemy

# Создаем объект базы данных, который потом привяжем к Flask-приложению
db = SQLAlchemy()

# 1. Таблица Пользователей (Студенты и Староста)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), default='student') # 'student' или 'admin'
    password_hash = db.Column(db.String(200), nullable=False)

    # Связь: один пользователь может иметь много записей о дежурствах
    # backref='student' позволит из записи дежурства получить объект пользователя
    schedules = db.relationship('Schedule', backref='student', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"


# 2. Таблица Зон уборки
class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Например, "Кухня 3 этаж"
    required_people = db.Column(db.Integer, default=1) # Сколько человек нужно

    schedules = db.relationship('Schedule', backref='zone', lazy=True)


# 3. Главная таблица: График дежурств
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='planned') # 'planned', 'done', 'overdue'
    photo_proof = db.Column(db.String(255), nullable=True) # Ссылка на фото

    def __repr__(self):
        return f"<Schedule {self.date} - {self.status}>"
