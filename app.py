from flask import Flask, render_template, request
import pymysql.cursors
from ImageWrite import scale_image
from mail import send_mail
from datetime import datetime

# Создаем экземпляр Flask App
app = Flask(__name__)


# Соединяемся с базой данных
con = pymysql.connect(host='localhost',
                      user='root',
                      password='12345678',
                      db='kontakt',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)


@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
def index():
    # Проверяем использование метода отправки данных
    if request.method == "POST":
        cur = con.cursor()

        b = request.form['inputFamily'].strip()
        a = request.form['inputName'].strip()
        c = request.form['inputLastName'].strip()
        d = request.form['inputPhone'].strip()
        e = request.form['inputDateBirthsday'].strip()
        f = request.form['inputShool'].strip()
        g = request.form['inputNumberShool'].strip()
        h = request.form['inputClass'].strip()
        j = request.form['inputCity'].strip()
        k = request.form['inputRaion'].strip()
        l = request.form['inputTupeStreet'].strip()
        m = request.form['inputNameStreet'].strip()
        u = request.form['inputHome'].strip()
        r = request.form['inputCorpus'].strip()
        mr = request.form['inputRoom'].strip()
        fr = request.form['inputFatherFamyli'].strip()
        gr = request.form['inputFatherName'].strip()
        hr = request.form['inputFatherLastName'].strip()
        nr = request.form['inputFatherPhone'].strip()
        br = request.form['inputMatherFamyli'].strip()
        ar = request.form['inputMatherName'].strip()
        tr = request.form['inputMatherLastName'].strip()
        ur = request.form['inputMatherPhone'].strip()
        qr = request.files['SendPhoto']



        user_name = str(b + '_' + a + '_' + c)
        # загрузка изображений на сервер через приложение ImageWrite
        scale_image(qr, user_name)

        # отправка письма с данными на электронную почту
        data_send = str('РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ В БАЗЕ ДАННЫХ ВАШЕГО ОТДЕЛА:''\n''\n''\n'
        + b + ' ' + a + ' ' + c + ', телефон: ' + d + ', дата рождения: ' + e + '\n'
        'Личная информация:  ' + f + ' № ' + g + ', класс/группа ' + h + ' ' + ', Адрес: ' + j + ' ' + k + ' ' + l + ' ' + m + ' ' + u + ', ' + r + ' Квартира ' + mr + '\n''\n'
        'Иформация о родителях:' + '\n''\n'
        'Ф.И.О. Отца, телефон:  ' + fr + ' ' + gr + ' ' + hr + ', ' + nr + '\n'
        'Ф.И.О. Матери, телефон:  ' + br + ' ' + ar + ' ' + tr + ', ' + ur + '\n''\n' + 'Дата регистрации: ' + datetime.now().strftime("%d-%B-%Y %X")).encode('utf-8')

        send_mail(data_send)

        # Ввод значений полей в базу данных
        cur.execute(
            """INSERT INTO user_kontakt (inputFamily, inputName, inputLastName, inputPhone, inputDateBirthsday, inputShool, inputNumberShool, inputClass, inputCity, inputRaion, inputTupeStreet, inputNameStreet, inputHome, inputCorpus, inputRoom, inputFatherFamyli, inputFatherName, inputFatherLastName, inputFatherPhone, inputMatherFamyli, inputMatherName, inputMatherLastName, inputMatherPhone) VALUES ('%(inputFamily)s', '%(inputName)s', '%(inputLastName)s', '%(inputPhone)s', '%(inputDateBirthsday)s', '%(inputShool)s','%(inputNumberShool)s', '%(inputClass)s', '%(inputCity)s', '%(inputRaion)s', '%(inputTupeStreet)s','%(inputNameStreet)s','%(inputHome)s','%(inputCorpus)s', '%(inputRoom)s', '%(inputFatherFamyli)s','%(inputFatherName)s','%(inputFatherLastName)s','%(inputFatherPhone)s', '%(inputMatherFamyli)s','%(inputMatherName)s','%(inputMatherLastName)s','%(inputMatherPhone)s') """
            % {"inputFamily": a, "inputName": b, "inputLastName": c, "inputPhone": d, "inputDateBirthsday": e,
               "inputShool": f, "inputNumberShool": g, "inputClass": h, "inputCity": j, "inputRaion": k,
               "inputTupeStreet": l, "inputNameStreet": m, "inputHome": u, "inputCorpus": r, "inputRoom": mr,
               "inputFatherFamyli": fr, "inputFatherName": gr, "inputFatherLastName": hr, "inputFatherPhone": nr,
               "inputMatherFamyli": br, "inputMatherName": ar, "inputMatherLastName": tr, "inputMatherPhone": ur}
        )
        # Сохранение внесенных изменений
        con.commit()

        # Просмотр измененных данных, вывод последней введенной строки
        cur.execute("SELECT * FROM user_kontakt ORDER BY id DESC LIMIT 1")
        rows = cur.fetchone()
        # for row in rows:
        print('\n', rows)

        # Вывод информации о изменениях
        base = "'user_kontakt'".upper()
        print('\n''Изменения в базу ' + base + ' внесены!' + '\n')
        # Закрыть соединение
        # con.close()
        # Выести страницу успешного запроса
        return render_template('Success!.html')
    else:
        return render_template('index.html')

    q = request.args.get('q')
    if q:
        return render_template('search.html')
    else:
        return render_template('index.html')


@app.route('/about', methods=["POST", "GET"])
def about():
    q = request.args.get('q')
    if q:
        return render_template('search.html')

    else:
        return render_template('about.html')


@app.route('/search', methods=["POST", "GET"])
def search():
    return render_template('search.html')


if __name__ == "__main__":
    app.run(debug=True)
