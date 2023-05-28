from flask import Flask, render_template, request, redirect, session, flash, url_for


app = Flask(__name__)
app.secret_key = 'alura'


class Game():
    def __init__(self, title, genre, platform):
        self.title = title
        self.genre = genre
        self.platform = platform


game_list = [
    Game(title='God of War', genre='action', platform='ps2'),
    Game(title='Super Mario World', genre='platform', platform='snes'),
    Game(title='Sonic The Hedgehog', genre='platform', platform='genesis')
]


class User():
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password


user_list = [
    User(name='Augusto', username='acardoso', password='change@123')
]

user_dict = {}
for user in user_list:
    user_dict.update({user.username: user})


@app.route('/')
def render_homepage():
    if 'auth_user' not in session or session['auth_user'] is None:
        return redirect(url_for('render_login_page'))
    return render_template('index.html', titulo='Games', games=game_list)


@app.route('/new')
def render_new_game_page():
    if 'auth_user' not in session or session['auth_user'] is None:
        return redirect(url_for('render_login_page', next=url_for('render_new_page')))
    return render_template('new.html', titulo='Games')


@app.route('/create', methods=['POST'])
def create_game():
    title = request.form['title']
    genre = request.form['genre']
    platform = request.form['platform']

    game = Game(title, genre, platform)
    game_list.append(game)
    return redirect(url_for('render_homepage'))


@app.route('/login')
def render_login_page():
    next = request.args.get('next')
    return render_template('login.html', next=next)


@app.route('/auth', methods=['POST'])
def authenticate_user():
    username_list = [user.username for user in user_list]
    if request.form['username'] in username_list:
        target_user = user_dict[request.form['username']]
        if request.form['password'] in target_user.password:
            session['auth_user'] = target_user.username
            flash('Login successful')

            if request.form['next'] == 'None':
                next_page = "/"
            else:
                next_page = request.form['next']
            return redirect(next_page)
        else:
            flash('Fail to login')
            return redirect(url_for('render_login_page'))
    else:
        flash('Fail to login')
        return redirect(url_for('render_login_page'))


@app.route('/logout')
def logout_user():
    session['auth_user'] = None
    flash('User logged out successfully')
    return redirect(url_for('render_homepage'))


app.run(host='0.0.0.0', port=8000, debug=True)
