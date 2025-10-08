from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)


def generate_password(length, complexity):

    if complexity == 'low':
        characters = string.ascii_lowercase
    elif complexity == 'medium':
        characters = string.ascii_letters + string.digits
    elif complexity == 'high':
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_letters + string.digits

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def get_password_strength(password):

    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "low", "danger"
    elif score <= 4:
        return "medium", "warning"
    else:
        return "high", "success"


@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    strength = None
    strength_class = None
    selected_length = 12
    selected_complexity = 'medium'

    if request.method == 'POST':
        selected_length = int(request.form.get('length', 12))
        selected_complexity = request.form.get('complexity', 'medium')

        if selected_length < 4:
            selected_length = 4
        elif selected_length > 50:
            selected_length = 50

        password = generate_password(selected_length, selected_complexity)

        strength, strength_class = get_password_strength(password)

    return render_template('index.html',
                           password=password,
                           strength=strength,
                           strength_class=strength_class,
                           selected_length=selected_length,
                           selected_complexity=selected_complexity)


if __name__ == 'main':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)