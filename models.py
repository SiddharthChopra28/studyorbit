from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Shopkeeper(UserMixin, db.Model):

    __bind_key__ = 'shopkeepers_db'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String())
    coordinates = db.Column(db.String())
    location = db.Column(db.String())
    date_joined = db.Column(db.String(), nullable=False)
    items_sold = db.Column(db.String()) #str of dict
    #params for items_sold - name, details {stock, price, img_link, desc}

    def get_id(self):
        return self.email

    def __repr__(self):
        return f"{self.id} - {self.username} - {self.email} - {self.items_sold}"


class Customer(UserMixin, db.Model):

    __bind_key__ = 'customers_db'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String())
    coordinates = db.Column(db.String())
    location = db.Column(db.String())
    date_joined = db.Column(db.String(), nullable=False)

    def get_id(self):
        return self.email

    def __repr__(self):
        return f"{self.id} - {self.username} - {self.email}"


class Order(db.Model):

    __bind_key__ = 'orders_db'

    id = db.Column(db.Integer(), primary_key=True)
    customer_email = db.Column(db.String(), nullable=False)
    seller_email = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    amount = db.Column(db.String(), nullable=False)
    img_link = db.Column(db.String(), nullable=False)
    desc = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.stock} - {self.price}"


