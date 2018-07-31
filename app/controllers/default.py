import os, pusher
from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, lm, mail
from sqlalchemy import tuple_
from flask_mail import Message as MSGMAIL
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from app.models.tables import User, Post, Follow, Comment, Message
from app.models.forms import LoginForm, PostForm, UserForm

urlSafeSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif','bmp'])

pusher_client = pusher.Pusher(
  app_id=app.config['PUSHER_APP_ID'],
  key=app.config['PUSHER_KEY'],
  secret=app.config['PUSHER_SECRET'],
  cluster=app.config['PUSHER_CLUSTER'],
  ssl=app.config['PUSHER_SSL']
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).filter(User.token=='').first()
        if user and User.validate_login(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("index"))
            flash("Logged in")
        else:
            flash("Login inválido ou sua conta não foi ativada.")
    
    return render_template('login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()

    if form.validate_on_submit():
        existsUsername = User.query.filter_by(username=form.username.data).first()
        if existsUsername:
            flash("Usuário já existente com este username")
            return redirect(url_for("index"))

        existsEmail = User.query.filter_by(email=form.email.data).first()
        if existsEmail:
            flash("Usuário já existente com este e-mail")
            return redirect(url_for("index"))
        
        token = urlSafeSerializer.dumps(form.email.data, salt='email-confirm')
        
        user = User(username=form.username.data, password=form.password.data, name=form.name.data, email=form.email.data)
        user.hash_password(password = form.password.data)
        user.set_token(token = token)
        db.session.add(user)
        db.session.commit()

        msg = MSGMAIL('Confirm Email', sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Seu link para validação é {}'.format(link)
        mail.send(msg)

        flash("Usuário criado com sucesso")
        return redirect(url_for("index"))
    
    return render_template('register.html', form=form)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = urlSafeSerializer.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter(User.email==email).filter(User.token==token).first()
        if user:
            user.token = ''
            db.session.add(user)
            db.session.commit()
            flash("Conta ativada com sucesso")
            return redirect(url_for("index"))
        else:
            flash("Erro, conta não encontrada ou conta já esta ativa.")
            return redirect(url_for("index"))
    except SignatureExpired:
        return '<h1>Este token expirou!</h1>'

@app.route('/logout')
def logout():
    logout_user()
    flash("Logout.")
    return redirect(url_for("login"))
    
@app.route("/index")
@app.route("/")
@login_required
def index():
    posts = Post.query.all()    
    return render_template("index.html", posts=posts)

@app.route("/addpost")
@login_required
def addpost():
    form = PostForm()
    return render_template("post.html", form=form)

@app.route("/post", methods=["POST"])
@login_required
def post():
    form = PostForm()
    filename = ''
    if form.validate_on_submit():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Arquivo não permitido')
            return redirect(url_for("index"))

        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, image=filename)
        db.session.add(post)
        db.session.commit()
        flash("Post enviado com sucesso")
    
    return redirect(url_for("index"))

@app.route("/edit_post/<id>", methods=('GET', 'POST'))
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.user.id != current_user.id:
        flash("Não permitido")
        return redirect(url_for("index"))
        
    form = PostForm(obj=post)
    filename = ''
    if form.validate_on_submit():
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if post.image:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.image))
        else:
            flash('Arquivo não permitido')
            return redirect(url_for("index"))

        post.title = form.title.data
        post.content = form.content.data
        post.image = filename
        db.session.add(post)
        db.session.commit()
        flash("Post atualizado com sucesso")
    
    return render_template('post_edit.html',form=form)

@app.route("/del_post/<id>", methods=['GET'])
@login_required
def del_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.user.id != current_user.id:
        flash("Não permitido")
        return redirect(url_for("index"))

    if post.image:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.image))

    db.session.delete(post)
    db.session.commit()
    flash("Post deletado com sucesso")
    
    return redirect(url_for("index"))

@app.route("/follow_post/<follower_id>", methods=['GET'])
@login_required
def follow_post(follower_id):
    follow = Follow(user_id=current_user.id, follower_id=follower_id)
    db.session.add(follow)
    db.session.commit()
    flash("Seguindo com sucesso")
    
    return redirect(url_for("index"))

@app.route("/unfollow_post/<follower_id>", methods=['GET'])
@login_required
def unfollow_post(follower_id):
    follow = Follow.query.filter_by(follower_id=follower_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
    flash("Parou de seguir com sucesso")
    
    return redirect(url_for("index"))

@app.route("/profile/<id>", methods=['GET'])
@login_required
def profile(id):
    seguindo = False
    form = UserForm()
    usuario = User.query.filter_by(id=id).first()
    posts = Post.query.filter_by(user_id=id).all()
    totalseguindo = Follow.query.filter_by(user_id=usuario.id).count()
    totalseguidores = Follow.query.filter_by(follower_id=usuario.id).count()
    if usuario.id != current_user.id:
        follow = Follow.query.filter_by(follower_id=usuario.id).first()
        if follow:
            seguindo = True
        else:
            seguindo = False

    return render_template("profile.html", usuario=usuario, posts=posts, form=form, seguindo=seguindo, totalseguindo=totalseguindo, totalseguidores=totalseguidores)

@app.route("/imgprofile/<id>", methods=('POST', ))
@login_required
def imgprofile(id):
    form = UserForm()
    usuario = User.query.filter_by(id=id).first()        
    filename = ''
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], filename))
        if usuario.image:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER_PROFILE'], usuario.image))
    else:
        flash('Arquivo não permitido')
        return redirect(url_for("profile", id=usuario.id, form=form))

    usuario.image = filename
    db.session.add(usuario)
    db.session.commit()
    flash("Imagem enviada com sucesso")
    
    return redirect(url_for("profile", id=usuario.id, form=form))

@app.route("/show/<id>", methods=['GET'])
@login_required
def show(id):
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post_id=post.id).all()
    
    return render_template("show.html", post=post, comments=comments)

@app.route("/comment/<id>", methods=['POST'])
@login_required
def comment(id):
    post = Post.query.filter_by(id=id).first()
    body = request.form.get('body')
    if body:
        comment = Comment(user_id=current_user.id, post_id=post.id, body=body)
        db.session.add(comment)
        db.session.commit()
        flash("Comentário adicionado com sucesso")

    return redirect(url_for("show", id=post.id))

@app.route("/chat", methods=['GET'])
@login_required
def chat():
    messages = Message.query.all()  
    return render_template("chat.html", messages=messages)

@app.route("/message", methods=['POST'])
@login_required
def message():
    
    try:
        username = current_user.name
        image = ''

        if current_user.image:
            image = current_user.image

        message = request.form.get('message')

        message_add = Message(username=username, message=message, image=image)
        db.session.add(message_add)
        db.session.commit()

        pusher_client.trigger('chat-channel', 'new-message', { 'username': username, 'image': image, 'message': message })

        return jsonify({ 'result': 'success' })
    except:
        return jsonify({ 'result': 'error' })
