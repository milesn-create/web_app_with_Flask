from flask import Flask, render_template, request, make_response
import re

app = Flask(__name__)

@app.route('/request-info')
def request_info():
    return render_template(
        'request_info.html',
        args=request.args,
        headers=request.headers,
        cookies=request.cookies
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    login = None
    password = None

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        response = make_response(
            render_template('login.html', login=login, password=password)
        )

        response.set_cookie('user_login', login)

        return response

    return render_template('login.html', login=login, password=password)

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    formatted = None
    phone_input = ""

    if request.method == 'POST':
        phone_input = request.form.get('phone')

        if not re.match(r'^[\d\+\-\(\)\.\s]+$', phone_input):
            error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
        else:
            digits = re.sub(r'\D', '', phone_input)

            if phone_input.startswith('+7') or phone_input.startswith('8'):
                valid_length = 11
            else:
                valid_length = 10

            if len(digits) != valid_length:
                error = "Недопустимый ввод. Неверное количество цифр."
            else:
                if len(digits) == 11:
                    digits = digits[-10:]

                formatted = f"8-{digits[0:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}"

    return render_template('phone.html', error=error, formatted=formatted, phone_input=phone_input)

if __name__ == '__main__':
    app.run(debug=True)
