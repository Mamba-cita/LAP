from unicodedata import name
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session, abort
from app import app, db,CKEditor
from forms import LoginForm, RegistrationForm, ClientOnboarding, PostForm, SearchForm
from app.models import LapModelView, User, Client, Transporter, Shipments, Posts
from flask_admin import Admin
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
import uuid as uuid
import os 



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/afri_admin')
@login_required
def afri_admin():
    id = current_user.id
    if id == 2:
        return render_template('admin/afri_admin.html')
    else:
        flash('You are not authorized to access Admin page! Contact your Product Manager')
        
    return redirect(url_for('home'))


@app.route('/protected_route')
@login_required
def protected_route():
    return 'Logged in as: ' + current_user.username


@app.route('/validate_user', methods=['GET', 'POST'])
def validate_user():
    if request.method == "POST":
        email = request.get_json()['email']
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"user_exists": "true"})
        else:
            return jsonify({"user_exists": "false"})


@app.route('/')
def index():
    return render_template('public/index/index.html')


@app.route('/user/<name>', methods=['GET', 'POST'])
@login_required

def user(name):
    name = None
    return render_template('admin/templates/users/templates/users.html', name=name)


@app.route('/users', methods=['GET', 'POST'])
@login_required

def users():
    name = None
    our_users = User.query.all()
    return render_template('admin/templates/users/templates/user.html', name=name, our_users=our_users)


@app.route('/user_dashboard', methods=['GET', 'POST'])
# @login_required
def user_dashboard():
    name = None
    form = RegistrationForm()
    return render_template('admin/templates/users/templates/user_dashboard.html', form=form, name=name)


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required

def update_user(id):
    form = RegistrationForm()
    name_to_update = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.password = request.form['password']
        db.session.commit()
        flash('User updated successfully')
        return render_template('admin/templates/users/templates/users.html', form=form, name_to_update=name_to_update)

    else:
        flash('User not updated,try again')
    return render_template('admin/templates/users/templates/update_user.html', form=form)


@app.route('/customers')
@login_required

def customers():
    return 'customers'


@app.route('/orders')
@login_required

def orders():
    return 'orders'


# single order

@app.route('/orders/<int:order_id>')
@login_required

def order(order_id):
    return 'order %d' % order_id


@app.route('/register', methods=['GET', 'POST'])
def register():
    name = None
    form = RegistrationForm()
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        db.session.close()

        flash('You are now registered and can log in')
        return redirect(url_for('login'))
    return render_template('admin/templates/users/templates/register.html', form=form, name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    name = None

    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            flash('You are now logged in')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password - Try again')
    return render_template('admin/templates/users/templates/login.html', form=form, name=name)


@app.route('/home')
@login_required
def home():
    return render_template('public/home/home.html')


@app.route('/clients', methods=['GET', 'POST'])
def clients():
    name = None

    form = ClientOnboarding()
    form.user_id.choices = [(user.id, user.username) for user in User.query.all()]
    if request.method == 'POST':
        created = current_user.id
        client = Client(
            name=request.form['name'],
            email=request.form['email'],
            account_manager=request.form['user_id'],
            created_by=created)

        db.session.add(client)
        db.session.commit()
        db.session.close()
        flash('Client added successfully to the system')
    return render_template('admin/templates/clients/templates/clients.html', form=form, name=name)


@app.route('/transporters', methods=['GET', 'POST'])
@login_required

def transporters():
    name = None

    transporters = Transporter.query.all()
    return render_template('admin/templates/transporters/templates/transporters.html', name=name)


@app.route('/assets', methods=['GET', 'POST'])
@login_required

def assets():
    return render_template('admin/templates/assets/assets.html')

# shipments


@app.route('/shipments', methods=['GET', 'POST'])
@login_required

def shipments():
    shipments = Shipments.query.all()

    return render_template('public/home/shipments.html', shipments=shipments)


@app.route('/shipments_creation', methods=['GET', 'POST'])
@login_required

def shipments_creation():
    return render_template('public/home/shipments_creation.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return render_template('public/index/index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('public/home/order.html')


@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        db.session.close()
        flash('Blog Post added successfully')

    return render_template('public/blog/post.html', form=form)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.filter_by(id=id).first()
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data
        post.slug = form.slug.data
        db.session.add(post)
        db.session.commit()
        flash('Blog Post updated successfully')
        return redirect(url_for('blog_view', id=post.id))
    else:
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author
        form.slug.data = post.slug
    return render_template('public/blog/edit_post.html', form=form)


@app.route('/blog_view/<int:id>')
def blog_view(id):
    blog = Posts.query.get_or_404(id)
    return render_template('public/blog/blog_view.html', blog=blog)


@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    blog = Posts.query.order_by(Posts.date_created)
    return render_template('public/blog/blogs.html', blog=blog)


# pass to nav bar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts.Posts.query
    if form.validate_on_submit():
        posts.searched = form.search.data
        posts = Posts.query.filter(Posts.content.like('%' + posts.searched + '%')).all()
        posts = Posts.order_by(Posts.title).all()
        return render_template('public/index/search.html',
                               form=form,
                               posts=posts)


@app.errorhandler(404)
def not_found(error):
    return render_template('public/404.html'), 404


@app.errorhandler(500)
def not_found(error):
    return render_template('public/500.html'), 500
