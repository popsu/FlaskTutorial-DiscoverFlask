from flask import render_template, Blueprint
from flask_login import login_required
from project import db
from project.models import BlogPost


home_blueprint = Blueprint(
    name='home',
    import_name=__name__,
    template_folder='templates'
)

####################
###### routes
####################


@home_blueprint.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
