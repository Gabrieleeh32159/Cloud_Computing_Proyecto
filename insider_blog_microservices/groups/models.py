from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import base64

db_name = "insiderblogdatabase"
password = "UgkLHJq07at9t4cNsTDl"
port = 5432
host = "insiderblogdatabase.cxqodojbla85.us-east-1.rds.amazonaws.com"
db_path=f'postgresql://postgres:{password}@{host}:{port}/'
secret_key = 'DBPPr0y3ct70F1n4l'

db = SQLAlchemy()

def setup_db(app, database_path=db_path):
    app.config['SECRET_KEY']=secret_key
    app.config['SQLALCHEMY_DATABASE_URI']=db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app=app
    db.init_app(app)
    db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, nullable= True)
    public_id = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), unique = True, autoincrement = True, nullable = False)
    description = db.Column(db.Text, default='')
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.Text, nullable = False, default=base64.b64encode(open('server/imagenes/default.jpg', 'rb').read()).decode('utf-8'))
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    groups = db.relationship('Group', secondary='group_user' , lazy = True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"User('{self.username}', \nEmail:'{self.email}', \nDescription:'{self.description}' \nPass:'{self.password}' \nPublic_id:'{self.public_id}' \nImg:'{self.image_file}')"

    def format(self):
        return{
            'id': self.id,
            'username': self.username,
            'description': self.description,
            'email': self.email,
            'image_file': self.image_file,
            'password': self.password,
            'posts_ids': [post.id for post in self.posts],
            'groups_ids': [group.group_name for group in self.groups]
        }

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False, default=0) 

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def format(self):
        user = User.query.filter(User.id == self.user_id).one_or_none()
        return{
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_name': user.username,
            'user_id': self.user_id,
            'group_id':self.group_id
        }


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key = True)
    group_name = db.Column(db.String(30), unique = True, nullable = False)
    members = db.relationship('User', secondary = 'group_user', lazy = True)
    posts = db.relationship('Post', backref = 'posts', lazy = True, cascade = "all, delete-orphan")

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f"Id('{self.id}', Group_name'{self.group_name}')"

    def format(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
        }


class GroupUser(db.Model):
    __tablename__ = 'group_user'
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key = True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True) 

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'group_id': self.group_id,
            'user_id': self.group_id,
        }
