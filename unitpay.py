#!/usr/bin/env python3

import urllib.parse
import hashlib
from urllib.request import urlopen
import json
import re
import copy
from flask import request


class UnitPay(object):
    secretKey = ''
    supportedUnitpayMethods = ['initPayment', 'getPayment']
    requiredUnitpayMethodsParams = {'initPayment': ['desc', 'account', 'sum'], 'getPayment': ['paymentId']}
    supportedPartnerMethods = ['check', 'pay', 'error']
    supportedUnitpayIp = [
        '31.186.100.49',
        '178.132.203.105',
        '52.29.152.23',
        '52.19.56.234',
        '127.0.0.1'  # for debug
    ]

    def __init__(self, secret_key):
        self.formUrl = 'https://unitpay.ru/pay/'
        self.apiUrl = 'https://unitpay.ru/api/'
        self.secretKey = secret_key

    def form(self, public_key, summ, account, desc, currency='RUB', locale='ru', customer_email=None):
        params = {'account': account, 'currency': currency, 'desc': desc, 'sum': summ, 'customerEmail': customer_email}
        params['signature'] = self.get_signature(params)
        params['locale'] = locale
        print(self.generate_signature(account, currency, desc, summ, self.secretKey))
        return self.formUrl + public_key + '?' + urllib.parse.urlencode(params)

    @staticmethod
    def generate_signature(account: str, currency: str, desc: str, sum: str, secret_key: str):
        signature = account + '{up}' + currency + '{up}' + desc + '{up}' + sum + '{up}' + secret_key
        signature = signature.encode('utf-8')
        return hashlib.sha256(signature).hexdigest()

    @staticmethod
    def generate_signature_output(account: str, currency: str, desc: str, sum: str, secret_key: str):
        signature = account + '{up}' + currency + '{up}' + desc + '{up}' + sum + '{up}' + secret_key
        signature = signature.encode('utf-8')
        return hashlib.sha256(signature).hexdigest()

    def get_signature(self, params):
        paramss = copy.copy(params)

        if 'params[signature]' in paramss:
            paramss.pop('params[signature]')
        if 'params[sign]' in paramss:
            paramss.pop('params[sign]')

        if 'customerEmail' in paramss:
            paramss.pop('customerEmail')

        paramss = ksort(paramss)
        paramss.append([0, self.secretKey])

        # list of dict to str
        res_p = []
        for p in paramss:
            res_p.append(str(p[1]))
        strr = '{up}'.join(res_p)
        strr = strr.encode('utf-8')
        h = hashlib.sha256(strr).hexdigest()
        return h

    def check_handler_request(self):
        ip = self.get_ip()

        params = {}
        for v in request.args.lists():
            params[str(v[0])] = request.args.get(v[0])

        if not 'method' in params:
            raise Exception('Method is null')

        if not params:
            raise Exception('Params is null')

        if not params['method'] in self.supportedPartnerMethods:
            raise Exception('Method is not supported')

        if not 'params[signature]' in params:
            raise Exception('signature params is null')

        if params['params[signature]'] != self.get_signature(params):
            raise Exception('Wrong signature')

        if not ip in self.supportedUnitpayIp:
            raise Exception('IP address error')

        return True

    @staticmethod
    def get_ip():
        if not request.headers.getlist("X-Forwarded-For"):
            ip = request.remote_addr
        else:
            ips = request.headers.getlist("X-Forwarded-For")[0].split(",")
            if ips[0] is not None:
                ip = ips[0]
            else:
                ip = request.headers.getlist("X-Forwarded-For")[0]
        return ip

    @staticmethod
    def get_error_handler_response(message):
        return json.dumps({'error': {'message': message}})

    @staticmethod
    def get_success_handler_response(message):
        return json.dumps({'result': {'message': message}})

    def api(self, method, params=None):
        if params is None:
            params = {}
        if not (method in self.supportedUnitpayMethods):
            raise Exception('Method is not supported')
        for rParam in self.requiredUnitpayMethodsParams[method]:
            if not rParam in params:
                raise Exception('Param ' + rParam + ' is null')
        params['secretKey'] = self.secretKey
        request_url = self.apiUrl + '?method=' + method + '&' + self.insert_url_encode('params', params)
        response = urlopen(request_url)
        data = response.read().decode('utf-8')
        jsons = json.loads(data)
        return jsons

    @staticmethod
    def insert_url_encode(inserted, params):
        result = ''
        first = True
        for p in params:
            if first:
                first = False
            else:
                result += '&'
            result += inserted + '[' + p + ']=' + str(params[p])
        return result


def parse_params(s):
    params = {}
    for v in s:
        if re.search('params', v):
            p = v[len('params['):-1]
            params[p] = s[v][0]
    return params


def ksort(d):
    return [[k, d[k]] for k in sorted(d.keys())]