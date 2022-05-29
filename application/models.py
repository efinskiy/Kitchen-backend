from email.policy import default
import sqlalchemy
from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin
import enum
from werkzeug.security import generate_password_hash, check_password_hash

class CouponTypes(enum.Enum):
    fixed = 1
    percent = 2
    fixed_with_rest = 3

class Logging(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)
    path = db.Column(db.Text)
    headers = db.Column(db.Text)
    request = db.Column(db.Text)
    referrer = db.Column(db.Text)
    ip = db.Column(db.Text)
    error = db.Column(db.Text)
    hash = db.Column(db.Text)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50))
    value = db.Column(db.String(50))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_kitchen = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    recovery = db.relationship('RecoveryLink', backref = 'userRef')


    # @property
    # def password(self):
    #     return "password hashed and not readable"
    
    # @password.setter
    # def password(self, passwd: str):
    #     self.password = passwd
    
    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    icon = db.Column(db.String(50))
    visible = db.Column(db.Boolean)
    is_system = db.Column(db.Boolean, default=False)
    is_default = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=1)
    products = db.relationship('Menu', backref='cat')
    coupon = db.relationship('Coupon', backref='cat')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def avaliableOnly(self):
        if self.title == "Популярное":
            return True
        if len(self.products) == 0:
            return False
        else:
            for product in self.products:
                if product.balance <= 0:
                    return False
            return True
            

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Integer)
    img = db.Column(db.String(50))
    price = db.Column(db.Float, nullable = False)
    balance = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    sells = db.Column(db.Integer, default=0)
    basket = db.relationship('Basket', backref = 'menu')
    discount = db.relationship('Sale', backref= 'product')


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(sqlalchemy.Enum(CouponTypes))
    avaliable_category = db.Column(db.Integer, db.ForeignKey(Category.id))
    key = db.Column(db.String(50))
    discount = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    
    order = db.relationship('Order', backref='customer')
    basket = db.relationship('Basket', backref = 'customer')
    recovery = db.relationship('RecoveryLink', backref = 'customerRef')

    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Basket(db.Model):
    __tablename__ = 'basket'

    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer)
    
    cust_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    item = db.Column(db.Integer, db.ForeignKey(Menu.id))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CancelReason(db.Model):
    __tablename__ = 'cancelreasons'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    isAdminReason = db.Column(db.Boolean, default=True)
    order = db.relationship('Order', backref = 'cancelReasonRef')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    payment_type = db.Column(db.Integer)
    is_payed = db.Column(db.Boolean, default=False)
    confirmation_code = db.Column(db.Integer, nullable=False)
    items = db.Column(db.Text)
    ord_price = db.Column(db.Float, nullable = False)
    date = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    cancelReason = db.Column(db.Integer, db.ForeignKey(CancelReason.id))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self) -> str:
        return str(self.items)

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, db.ForeignKey(Menu.id))
    discount = db.Column(db.Integer)
    expiring = db.Column(db.DateTime)
    disabled = db.Column(db.Boolean, default=False)

class RecoveryLink(db.Model):
    __tablename__ = 'recoverylinks'

    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer, db.ForeignKey(Customer.id))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    is_used = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(64))