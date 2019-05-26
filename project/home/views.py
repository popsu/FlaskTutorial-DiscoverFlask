from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from project import db
from project.models import BlogPost
from project.home.forms import MessageForm


home_blueprint = Blueprint(
    name='home',
    import_name=__name__,
    template_folder='templates'
)

####################
###### routes
####################


@home_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            title=form.title.data,
            description=form.description.data,
            author_id=current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted. Thanks', 'success')
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        return render_template('index.html', posts=posts, form=form, error=error)


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
