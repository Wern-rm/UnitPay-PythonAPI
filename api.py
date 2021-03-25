from flask import Flask
import locale
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
locale.setlocale(locale.LC_ALL, '')
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'UnitPay API'


from models import UnitpayPayments, AccountData
from unitpay import UnitPay
from flask import request
from sqlalchemy import exc
from datetime import datetime
import decimal


@app.route('/api/v1.0/unitpay/payment/', methods=['GET'])
def unitpay_processor():
    unitpay = UnitPay('SECRET_KEY')  # ВВести ключ от UnitPay
    if unitpay.check_handler_request():
        try:
            sum_count = decimal.Decimal(request.args.get('params[profit]'))
            account = db.session.query(AccountData).filter(AccountData.name == request.args.get('params[account]')).first()
            if request.args.get('method') == 'pay':
                if account:
                    pay = UnitpayPayments(unitpay_id=request.args.get('params[unitpayId]'),
                                          account=request.args.get('params[account]'),
                                          sum=request.args.get('params[payerSum]'),
                                          payment_type=request.args.get('params[paymentType]'),
                                          payer_currency=request.args.get('params[payerCurrency]'),
                                          signature=request.args.get('params[signature]'),
                                          profit=request.args.get('params[profit]'))
                    db.session.add(pay)
                    db.session.commit()

                    update_count = sum_count

                    db.session.query(AccountData).filter(AccountData.name == request.args.get('params[account]')).update({
                        'balance': account.balance + update_count
                    })
                    db.session.query(UnitpayPayments).filter(UnitpayPayments.unitpay_id == request.args.get('params[unitpayId]')).update({
                        'date_complete': datetime.now(),
                        'status': 1
                    })
                    db.session.commit()
                    app.logger.info('The request was successfully processed by the system.')
                    return unitpay.get_success_handler_response("The request was successfully processed by the system.")
                else:
                    app.logger.info('Account with this email does not exist.')
                    return unitpay.get_error_handler_response("Account with this email does not exist.")
            else:
                app.logger.info('The request was successfully processed by the system without writing to the database because of.')
                return unitpay.get_success_handler_response("The request was successfully processed by the system without writing to the database because of.")
        except exc.SQLAlchemyError as e:
            print(e)
            app.logger.error(e)
            db.session.rollback()
            return unitpay.get_error_handler_response("The request has been processed by the system.")
    else:
        return unitpay.get_error_handler_response("The request has been processed by the system.")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
