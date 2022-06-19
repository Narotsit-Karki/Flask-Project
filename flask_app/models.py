from flask_app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader # for managing user session
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
   
    uid = db.Column(db.Integer, primary_key = True,autoincrement = True)
    username = db.Column(db.String(20), unique = True , nullable = False)
    email = db.Column(db.String(100),unique = True, nullable = False)
    image_file = db.Column(db.String(20),nullable=False , default = 'default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref = 'author', lazy = True)  #backref similar to adding column
    comment = db.relationship('Comments', backref = 'comment_user', lazy = True)
    def __repr__(self): # how our object is printed
        return f"Users('{self.username}' , '{self.email}','{self.image_file}')"

    def get_id(self):
        return self.uid 


class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable =False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    content = db.Column(db.Text, nullable= False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.uid'),nullable =False)
    posts_comments = db.relationship('Comments', backref = 'comment_post',lazy = True, passive_deletes = True)
    def __repr__(self):  # how our object is printed
        return f"Post('{self.title}' , {self.content},'{self.date_posted}')"


class Comments(db.Model):
    cid = db.Column(db.Integer, primary_key = True,autoincrement= True)
    comment_uid = db.Column(db.Integer,db.ForeignKey('users.uid'),nullable = False)
    date_commented = db.Column(db.DateTime,default=datetime.utcnow())
    comment = db.Column(db.Text,nullable= False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.pid', on_delete = "CASCADE"), nullable = False)


    def __repr__(self):
        return f"Comments('{self.comment_uid},'{self.date_commented}','{self.comment}')"



