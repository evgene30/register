from datetime import datetime
from mail import send_mail
import pymysql
from flask import Flask, render_template, request
from ImageWrite import scale_image

# Создаем экземпляр Flask App
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # Соединяемся с базой данных
        cnx = pymysql.connect('localhost', 'root', '12345678', 'kontakt')
        cursor = cnx.cursor()

        Section = request.form['inputSection'].strip()
        Division = request.form['inputDivision'].strip()
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

        # загрузка изображений на сервер через приложение ImageWrite
        user_name = f"{b}_{a}_{c}"
        fix = scale_image(qr, user_name)


        # отправка письма с данными на электронную почту
        body = str(
            f'РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ В БАЗЕ ДАННЫХ ВАШЕГО ОТДЕЛА:''\n'
            '\n'
            '\n'
            f'Название объединения: "{Section}", {Division.lower()}''\n'
            '\n'
            f'{b} {a} {c}''\n'
            '\n'
            f'телефон: +375{d}, дата рождения: {e}''\n'
            '\n'
            f'Личная информация:''\n'
            f'{f} №{g}, класс/группа: {h}''\n'
            f'Адрес: {j}, {k} {l} {m} {u}, {r}, квартира {mr}''\n'
            '\n'
            f'Иформация о родителях:''\n'
            f'Ф.И.О. Отца, телефон: {fr} {gr} {hr}, +375{nr}''\n'
            f'Ф.И.О. Матери, телефон: {br} {ar} {tr}, +375{ur}''\n'
            '\n'
            f"Дата регистрации (время сервера): {datetime.now().strftime('%d-%B-%Y %X')}"
            )

        send_mail(body, fix, user_name.lower(), Division)

        # Ввод значений полей в базу данных
        cursor.execute(
           """INSERT INTO user_kontakt (inputFamily, inputName, inputLastName, inputPhone, inputDateBirthsday, inputShool, inputNumberShool, inputClass, inputCity, inputRaion, inputTupeStreet, inputNameStreet, inputHome, inputCorpus, inputRoom, inputFatherFamyli, inputFatherName, inputFatherLastName, inputFatherPhone, inputMatherFamyli, inputMatherName, inputMatherLastName, inputMatherPhone) VALUES ('%(inputFamily)s', '%(inputName)s', '%(inputLastName)s', '%(inputPhone)s', '%(inputDateBirthsday)s', '%(inputShool)s','%(inputNumberShool)s', '%(inputClass)s', '%(inputCity)s', '%(inputRaion)s', '%(inputTupeStreet)s','%(inputNameStreet)s','%(inputHome)s','%(inputCorpus)s', '%(inputRoom)s', '%(inputFatherFamyli)s','%(inputFatherName)s','%(inputFatherLastName)s','%(inputFatherPhone)s', '%(inputMatherFamyli)s','%(inputMatherName)s','%(inputMatherLastName)s','%(inputMatherPhone)s') """
            % {"inputFamily": a, "inputName": b, "inputLastName": c, "inputPhone": d, "inputDateBirthsday": e,
               "inputShool": f, "inputNumberShool": g, "inputClass": h, "inputCity": j, "inputRaion": k,
               "inputTupeStreet": l, "inputNameStreet": m, "inputHome": u, "inputCorpus": r, "inputRoom": mr,
               "inputFatherFamyli": fr, "inputFatherName": gr, "inputFatherLastName": hr, "inputFatherPhone": nr,
               "inputMatherFamyli": br, "inputMatherName": ar, "inputMatherLastName": tr, "inputMatherPhone": ur}
        )
        # Сохранение внесенных изменений
        cnx.commit()
        #cursor.close()

        # Просмотр измененных данных, вывод последней введенной строки
        #cursor.execute("SELECT * FROM user_kontakt ORDER BY id")
        #results = cursor.fetchone()
        #print(row)

        # Вывод информации о изменениях
        #base = "user_kontakt".upper()
        #print('\n''Изменения в базу ' + base + ' внесены!' + '\n')

        # Закрыть соединение
        cnx.close()

        # Выести страницу успешного запроса
        return render_template('Success!.html')
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