from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .database import db_session
from .models import User, AuthToken

auth = Blueprint('auth', __name__, url_prefix='/auth')

def redirect_dest(fallback):
    dest = request.args.get('next')
    if dest is None:
        return redirect(fallback)
    elif dest != 'None': # this is so dumb but it works :D
        dest_url = dest
    else:
        return redirect(fallback)
    return redirect(dest_url)

def scrub_db_tokens():
    # scrub the db of expired tokens
    return

@auth.before_app_request
def load_logged_in_user():
    token = session.get('token')

    if token is None:
        g.user = None
    else:
        auth_token_obj = db_session.query(AuthToken).filter(AuthToken.token == token).first()
        if auth_token_obj is not None:
            g.user = db_session.query(User).filter(User.id == auth_token_obj.user_id).first()
        else:
            g.user = None

@auth.route('/login', methods=('GET', 'POST'), strict_slashes=False)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        error = None
        user = db_session.query(User).filter(User.username == username).first()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password or password.'

        if error is None:
            # create the auth token and store that in the session + db
            token_obj = AuthToken().create(user)
            db_session.add(token_obj)
            db_session.commit()
            session.clear()
            session['token'] = token_obj.token
            # if the remember flag is set, we want this to be a permanent session
            if remember == '1':
                session.permanent = True
            
            # might just have this function scrub expired tokens hmm
            scrub_db_tokens()

            # then attempt a redirect based on the 'next' url parameter
            return redirect_dest(fallback=url_for('main.index'))

        # if there is an error flash it
        flash(error)
    
    # return the login page
    return render_template('auth/login.html')

@auth.route('/logout', strict_slashes=False)
def logout():
    # get the token from the session
    token = session['token']

    # remove the token from the browser
    session['token'] = None

    # expire the token

    # scrub old tokens
    scrub_db_tokens()

    # then attempt a redirect based on the 'next' url parameter
    return redirect_dest(fallback=url_for('main.index'))
