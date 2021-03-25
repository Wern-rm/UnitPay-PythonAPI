from api import db
from datetime import datetime


class UnitpayPayments(db.Model):
    __tablename__ = 'unitpay_payments'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    unitpay_id = db.Column(db.VARCHAR(255), nullable=False)
    account = db.Column(db.VARCHAR(255), nullable=False)
    sum = db.Column(db.REAL(), nullable=False)
    payment_type = db.Column(db.VARCHAR(255), nullable=False)
    payer_currency = db.Column(db.VARCHAR(255), nullable=False)
    signature = db.Column(db.VARCHAR(100), nullable=False)
    date_create = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    date_complete = db.Column(db.DateTime(), nullable=True, default=None)
    status = db.Column(db.Integer(), nullable=False, default=0)
    profit = db.Column(db.VARCHAR(255), nullable=True)

    def __init__(self, unitpay_id, account, sum, payment_type, payer_currency, signature, profit):
        self.unitpay_id = unitpay_id
        self.account = account
        self.sum = sum
        self.payment_type = payment_type
        self.payer_currency = payer_currency
        self.signature = signature
        self.profit = profit


class AccountData(db.Model):
    __tablename__ = 'account_data'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.VARCHAR(30), nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)
    activated = db.Column(db.Integer(), nullable=False, default=0)
    access_level = db.Column(db.Integer(), nullable=False, default=0)
    last_server = db.Column(db.Integer(), nullable=False, default=-1)
    last_ip = db.Column(db.VARCHAR(20), nullable=False, default='xxx.xxx.xxx.xxx')
    last_mac = db.Column(db.VARCHAR(20), nullable=False, default='xx-xx-xx-xx-xx-xx')
    last_hdd = db.Column(db.VARCHAR(100), nullable=False, default='xxxxxxxxxxxxx')
    allowed_ip = db.Column(db.VARCHAR(20), nullable=True)
    allowed_mac = db.Column(db.VARCHAR(20), nullable=True)
    allowed_hdd = db.Column(db.VARCHAR(100), nullable=True)
    session_id = db.Column(db.VARCHAR(100), nullable=True)
    create_date = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.now())
    edit_date = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.now())
    password_edit_date = db.Column(db.TIMESTAMP(), nullable=False, default=datetime.now())
    security_ip = db.Column(db.VARCHAR(20), nullable=False, default='127.0.0.1')
    balance = db.Column(db.Integer(), nullable=False, default=0)
    is_banned = db.Column(db.Integer(), nullable=False, default=0)
    two_factor = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self, name, password):
        self.name = name
        self.password = password