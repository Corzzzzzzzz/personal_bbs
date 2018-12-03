from flask import jsonify

class HttpCode():
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500

def restful_result(code, message='', data=None):
    return jsonify({'code': code, 'message': message, 'data': data})

def success(message='', data=None):
    return jsonify({'code': HttpCode.ok, 'message': message, 'data': data})

def unauth_error(message=''):
    return jsonify({'code': HttpCode.unautherror, 'message': message})

def params_error(message=''):
    return jsonify({'code': HttpCode.paramserror, 'message': message})

def server_error(message=''):
    return jsonify({'code': HttpCode.servererror, 'message': message})