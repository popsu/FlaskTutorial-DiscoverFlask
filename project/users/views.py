from flask import flash, redirect, render_template, request, \
    url_for, Blueprint
from flask_login import login_user, login_required, logout_user
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
                login_user(user)
                flash('You were logged in.')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid Credentials. Please try again.'
      
    return render_template('login.html', error=error, form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.welcome'))
