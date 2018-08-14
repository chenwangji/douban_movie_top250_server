# -*- coding: UTF-8 -*-
from flask import Flask, jsonify
from flask_restful import reqparse, Api
import json
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from . import const

app = Flask(__name__)
api = Api(app)

engine = sqlalchemy.create_engine(const.DB_ADRESS, encoding="utf8", echo=False)
BaseModel = sqlalchemy.ext.declarative.declarative_base()

# 利用 Session 对象连接数据库
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()

# 删掉所有表
BaseModel.metadata.drop_all(engine)
# 重新创建表
BaseModel.metadata.create_all(engine)

# 路由
from handler.hd_movie import Page_movies
# 设置路由
api.add_resource(Page_movies, '/movies')

if __name__ == '__main__':
  app.run()