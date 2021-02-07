from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
import random
import config

app = Flask(__name__)
app.config.from_object(config)
# db = SQLAlchemy(app)

# class Dictionaries(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, default=datetime.utcnow())
#     words = db.relationship('Words', backref='dictionary')
#
#     def __init__(self, *args, **kwargs):
#         super(Dictionaries, self).__init__(*args, **kwargs)
#
#     def __repr__(self):
#         return f'<Dict id: {self.id}, date: {self.date}>'
#
#
# class Words(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     eng = db.Column(db.String(100), unique=True, nullable=True)
#     rus = db.Column(db.String(100), nullable=True)
#     dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionaries.id'))
#
#     def __init__(self, *args, **kwargs):
#         super(Words, self).__init__(*args, **kwargs)
#
#     def __repr__(self):
#         return f'<eng: {self.eng}, rus: {self.rus}>'
#
# class SQLAlchemyDataBase:
#     def __init__(self, db):
#         self.db = db
#
#     def check_existence(self, value):
#         if value.isdecimal():
#             value = self.db.session.query(Dictionaries).filter_by(id=value).first()
#         else:
#             value = self.db.session.query(Words).filter_by(eng=value).first()
#
#         if value:
#             return True
#         else:
#             return False
#
#     def check_limit(self, num):
#         amount = self.db.session.query(Words).filter_by(dictionary_id=num).count()
#         if amount >= 30:
#             return True
#         else:
#             return False
#
#     def create_dict(self, num):
#         d = Dictionaries(id=num)
#         self.db.session.add(d)
#         self.db.session.commit()
#
#     def add_word(self, num, eng, rus):
#         w = Words(eng=eng, rus=rus, dictionary_id=num)
#         self.db.session.add(w)
#         self.db.session.commit()
#
#     def get_words(self, num):
#         words = self.db.session.query(Words).filter_by(dictionary_id=num).all()
#         return words


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'mode' in request.form:
            session['mode'] = request.form['mode']
        elif 'num' in request.form:
            if request.form['num'].isdecimal():
                session['num'] = request.form['num']
                num = session['num']
                words = dbase.get_words(num)
                words = [[w.eng, w.rus] for w in words]
                words = [['hello', 'world']]

                if not words:
                    session.pop('num')
                    flash('Ошибка: Словаря с таким номером не существует.', category='error')
                    return redirect('/#popup-dictionary')
                else:
                    random.shuffle(words)
                    session['words'] = words
                    session['n'] = 0
            else:
                flash('Ошибка: Разрешено вводить только цифры.', category='error')
                return redirect('/#popup-dictionary')

    if 'mode' in session:
        mode = session['mode']
    else:
        mode = ''

    if 'num' in session:
        num = session['num']
        words = session['words']
        n = session['n']

        if mode == 'English-Russian':
            session['ask'] = words[n][0]
            session['answer'] = words[n][1]

        elif mode == 'Russian-English':
            session['ask'] = words[n][1]
            session['answer'] = words[n][0]

        else:
            session['ask'] = ''
            session['answer'] = ''

        ask = session['ask']
        answer = session['answer']
        help = answer[:2]
        if ', ' in ask:
            answer = answer[:-1]

        if 'translate' in request.form:
            if answer == request.form['translate'].lower():
                flash('Верно.', category='success')
                if n < len(words) - 1:
                    session['n'] += 1
                else:
                    random.shuffle(session['words'])
                    session['n'] = 0
                return redirect(url_for('api.index'))
            else:
                flash('Wrong.', category='error')

    else:
        num = ''
        ask = ''
        answer = ''
        help = ''

    return render_template('index.html', mode=mode, num=num, ask=ask, help=help,
                           answer=answer)

# @app.route('/add_words', methods=['POST', 'GET'])
# def add_words():
#     if request.method == 'POST':
#         if 'ctr_num' in request.form:
#             if request.form['ctr_num'].isdecimal():
#                 crt_num = request.form['ctr_num']
#                 if not dbase.check_existence(crt_num):
#                     dbase.create_dict(crt_num)
#                     flash('Словать под номером "' + crt_num + '" создан.',
#                           category='success')
#                 else:
#                     flash("Словарь с таким именем уже существует", category='error')
#             else:
#                 flash('Ошибка: Разрешено вводить только цифры.', category='error')
#                 return redirect('/add_words#popup-create-dictionary')
#
#         elif 'num' in request.form:
#             if request.form['num'].isdecimal():
#                 session['num'] = request.form['num']
#                 num = session['num']
#                 if not dbase.check_existence(num):
#                     session.pop('num')
#                     flash('Словаря с таким номером не существует.', category='error')
#                     return redirect('/add_words#popup-dictionary')
#             else:
#                 flash('Ошибка: Разрешено вводить только цифры.', category='error')
#                 return redirect('/add_words#popup-dictionary')
#
#     if 'num' in session:
#         num = session['num']
#         if 'eng' in request.form and 'rus' in request.form:
#             if not dbase.check_limit(num):
#                 eng = request.form['eng']
#                 rus = request.form['rus']
#                 if not dbase.check_existence(eng):
#                     dbase.add_word(num, eng, rus)
#                     flash('Слово успешно добавлено', category='success')
#                 else:
#                     flash('Слово уже существует.', category='error')
#             else:
#                 flash('Количество слов в словаре достигло предела.', category='error')
#
#     else:
#         num = ''
#
#     return render_template('add_words.html', num=num)


if __name__ == '__main__':
    app.run(debug=True)
