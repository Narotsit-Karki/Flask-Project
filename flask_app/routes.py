from flask import render_template, url_for, flash, redirect, request
import hashlib, binascii , secrets , os
from flask_app.forms import Registration_Form,Login_Form, Update_Account_Form , Post_Form , Edit_Post_Form
from flask_app.models import Users, Post, Comments
import  os
from PIL import Image
from flask_app import app, db , bcrypt
from flask_login import login_user,current_user,logout_user, login_required

# def generate_hash(password):
#     psd = password.encode("utf-8")
#     salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
#     hsh_pwd = hashlib.pbkdf2_hmac('sha256', psd, salt, 200000)
#     hsh_pwd = binascii.hexlify(hsh_pwd)
#     return (salt + hsh_pwd).decode('ascii')
#
#
# def verify_password(password, index):
#     stored_hash = Data_Info['password_hash'][index]
#     salt = stored_hash[:64]
#     password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('ascii'), 200000)
#     password_hash = binascii.hexlify(password_hash).decode("ascii")
#     return (salt + password_hash) == stored_hash

@app.route('/')
def home():
    return redirect(url_for('posts'))

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    post_datas = Post.query.all()
    comments = Comments.query.all()
    post_datas = post_datas[-1::-1]
    comments = comments[-1::-1]


    back_path = url_for('static',filename='background.jpg')
    return render_template('posts.html', title='Posts', post_datas=post_datas, comments = comments, back_path = back_path)


@app.route('/about-us')
def about_us():
    return render_template('about-us.html', title='About-Us')


@app.route('/Login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('❗ Already logged in','info')
        return redirect(url_for('posts'))

    form = Login_Form()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):

            login_user(user,remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f"✔ Logged in successfully ... Welcome, {user.username}", 'success')
            return redirect(next_page) if next_page else redirect(url_for('posts'))
        else:
            flash("❌ login Failed ... Check email or password.",'danger')

    return render_template('login.html', form=form, title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('❗ Already a registered user...','info')
        return redirect(url_for('posts'))
    form = Registration_Form()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username = form.username.data,email =form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"✔ Account for {form.username.data} has been successfully created ... you can now log in",'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out . . .",'info')
    return redirect(url_for('posts'))

def update_profile_pic(profile_pic):
    random_hex = secrets.token_hex(12)
    f_name ,f_ext = os.path.splitext(profile_pic.filename)
    new_picture_file = random_hex + f_ext
    picture_path = os.path.join(app.root_path ,'static/profile_pics', new_picture_file)
    output_size = (255,255)
    i = Image.open(profile_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return new_picture_file




@app.route("/account",methods = ['GET','POST'])
@login_required # to prevent from not logged users to not to get account.html webpage
def account():
    form = Update_Account_Form()
    post = Post.query.filter_by(user_id=current_user.uid).all()
    comment = Comments.query.all()
    post = post[-1::-1]
    comment = comment[-1::-1]
    if form.validate_on_submit():
        if form.profile_pic.data:
            pic_file = update_profile_pic(form.profile_pic.data)
            if current_user.image_file != 'default.jpg':
                try:
                    os.remove(app.root_path+'/static/profile_pics/'+current_user.image_file)
                except Exception:
                    pass
            current_user.image_file = pic_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('✔ Account Updated Successfully','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('user_account.html',title="Account",form = form , post_datas = post, comments = comment , image_file = url_for('static',filename='profile_pics/' + current_user.image_file))

@app.route('/posts/new',methods=['GET','POST'])
@login_required
def new_post():
    form = Post_Form()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Post Submitted...', 'success')
        return redirect(url_for('posts'))
    return render_template('create_post.html',title = 'New Post',form=form)

@app.route('/create-comment/<int:post_id>',methods = ['POST'])
def create_comment(post_id):
    text = request.form.get('text')
    post = Post.query.filter_by(pid = post_id).first()
    if not current_user.is_authenticated:
        flash('❗ Login First to Comment!!','danger')
        return redirect(url_for('login'))

    if post:
        print(post,text,current_user)
        comment = Comments(comment = text,comment_user = current_user,comment_post = post)
        db.session.add(comment)
        db.session.commit()
        flash('✔ Comment Posted...','success')
        
    else:
        flash('❌ Post Doesnot Exist ...','danger')

    return redirect(url_for('posts'))


@app.route('/delete-post/<int:post_id>',methods = ['POST'])
@login_required
def delete_post(post_id):
    print(post_id)
    post = Post.query.filter_by(pid=post_id).first()
    comment = Comments.query.filter_by(post_id=post_id).all()
    print(post.content)
    db.session.delete(post)
    for c in comment:
        db.session.delete(c)
    
    db.session.commit()
    flash('✔ Post Deleted ... ','success')
    return redirect(url_for('account'))


@app.route('/authour/<string:authour_name>',methods=['GET'])
def users_information(authour_name):
    authour = Users.query.filter_by(username=authour_name).first()
    authour = authour
    return render_template('authour_info_page.html',title = authour_name , authour = authour)


@app.route('/edit-post/<string:user>/<int:post_id>' , methods = ['GET','POST'])
@login_required
def edit_post(user,post_id):
    form = Edit_Post_Form()
    posts = current_user.post
    for post in posts:
        if post.pid == post_id:
            post = post 
            break
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('✔ Post Updated Sucessfully ...')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
   

    return render_template('edit_post.html',title = 'Edit Post' ,post = post, form = form)
