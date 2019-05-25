from flask import flash, redirect, render_template, request, \
    session, url_for, Blueprint
from functools import wraps
from project.users.forms import LoginForm
from project.models import User, bcrypt

####################
##### config
####################

users_blueprint = Blueprint(
    name='users',
    import_name=__name__,
    template_folder='templates'
)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))

    return wrap

####################
###### routes
####################


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user and bcrypt.check_password_hash(user.password,
                                                   request.form['password']):
                session['logged_in'] = True
                flash('You were logged in.')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid Credentials. Please try again.'
      
    return render_template('login.html', error=error, form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('home.welcome'))
