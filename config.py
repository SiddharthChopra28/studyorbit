class Config(object):

    SECRET_KEY = '\r\x93r`\x08\xef\x07o\xbbBqE\x8a[ ('

    SQLALCHEMY_BINDS = {
        'shopkeepers_db': 'sqlite:///data/shopkeepers.db',
        'customers_db': 'sqlite:///data/customers.db',
        'orders_db' : 'sqlite:///data/orders.db'
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_NAME = 'localhost:5001'

    UPLOAD_FOLDER = 'static\\uploads'
