from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from config import bcrypt, db
from sqlalchemy.orm import validates
from flask_login import UserMixin

# Models go here!

class User (db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    _password_hash= db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    favorites = db.relationship('Favorite', back_populates='user')
    notes = db.relationship('Note', back_populates='user')


    serialize_rules = ('-favorites.user, -notes.user',)


    @validates("username")
    def validate_username(self, key, value):
        usernames: User.query.all()
        if not value and value in usernames:
            raise ValueError("Username already taken")
            
        return value
    
    @hybrid_property
    def password_hash(self):
      raise Exception("password_hash may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))



# def authenticate_user (username, password):
#     try:
#         user = User.query.filter_by(username=username).one()
#         if not user.auth(password=password):
#             return False
#         login_user(user, remember=True)
#     except NoResultFound:
#         return False
# # @hybrid_property
# def password_hash(self):
#     raise Exception("password_hash may not be viewed")

# @password_hash.setter
# def password_hash(self, password):
#     password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
#     self._password_hash = password_hash.decode('utf-8')

# def authenticate(self, password):
#     return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

class Article (db.Model, SerializerMixin):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())
    title = db.Column(db.String())
    image_url = db.Column(db.String())
    key_facts = db.Column(db.String())
    description = db.Column(db.String())
    article_url = db.Column(db.String())

    notes = db.relationship('Note', back_populates='article')
    favorite = db.relationship('Favorite', back_populates='article')

    # serialize_rules = ('-notes.article', '-favorite.article',)
    serialize_rules = ('-notes', '-favorite', '-user',)

    @validates('category')
    def validate_article_category(self, key, value):
        allowed_categories = ['Culture', 'Geography', 'Health', 'History', 'Human Activities', 'Mathematics', 'Natural Sciences', 'People', 'Philosophy', 'Religion', 'Social Sciences', 'Technology']
        if value not in allowed_categories:
            raise ValueError("Invalid category: Choose from 'Culture', 'Geography', 'Health', 'History', 'Human Activities', 'Mathematics', 'Natural Sciences', 'People', 'Philosophy', 'Religion', 'Social Sciences', 'Technology'")
        return value


    @hybrid_property
    def is_current_user_note(self):

        notes = Article.query.filter(Article.id == self.id).notes.all()
        if notes:
            current_user = User.query.filter_by(id=current_user.id).first()
            current_user_notes = self.notes.filter_by(user_id=current_user.id)
            return current_user_notes
        else:
            current_user_notes = None

class Note (db.Model, SerializerMixin):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    title = db.Column(db.String())
    text = db.Column(db.String())

    article = db.relationship('Article', back_populates='notes')
    user = db.relationship('User', back_populates='notes')


    # serialize_rules = ('-article.notes, -user.notes,',)
    serialize_rules = ( '-favorite', '-user', '-article',)


class Favorite (db.Model, SerializerMixin):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    
    
    user = db.relationship('User', back_populates='favorites')
    article = db.relationship('Article', back_populates='favorite')
   
    # serialize_rules = ('-user.favorites, -article.favorites,',)
    serialize_rules = ('-notes', '-user', '-article')

    @validates('category')
    def validate_favorite_category(self, key, value):
        allowed_categories = ['Culture', 'Geography', 'Health', 'History', 'Human Activities', 'Mathematics', 'Natural Sciences', 'People', 'Philosophy', 'Religion', 'Social Sciences', 'Technology']
        if value not in allowed_categories:
            raise ValueError("Invalid category: Choose from 'Health', 'History', 'Human Activities', 'Mathematics', 'Natural Sciences', 'People', 'Philosophy', 'Religion', 'Social Sciences', 'Technology'")
        return value
        
    

    
    


