import flask
import json
from common.utils import AlchemyEncoder

def err_res(code, msg):
  return flask.jsonify(code, msg) 

def success_res(code, data, msg):
  return flask.jsonify({'code': code, 'data': json.dumps(data, cls=AlchemyEncoder, ensure_ascii=False), 'msg': msg})