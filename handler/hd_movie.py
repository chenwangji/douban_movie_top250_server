from flask import jsonify
from flask_restful import reqparse, Resource
import json
from app import session
import app.const as const
from common.utils import AlchemyEncoder
from model.movie import Movie, create_movie
from common.spider import Spider
from common.template import err_res, success_res

# RESTful API 的参数解析
parser = reqparse.RequestParser()
parser.add_argument('page_now', type=int, required=True, help="need page_now data")
parser.add_argument('page_size', type=int, required=True, help="need page_size data")


class Page_movies(Resource):
  def get(self):
    args = parser.parse_args()
    if 'page_now' not in args:
      return err_res(code=0, msg='no page_now')
    if 'page_size' not in args:
      return err_res(code=0, msg='no page_size')
  
    page_now = args['page_now']
    page_size = args['page_size']
    if page_now * page_size > 250:
      return err_res(code=0, msg='无更多电影')
  
    cached_movies = session.query(Movie).filter(Movie.id.between((page_now - 1) * page_size + 1, page_now * page_size)).all()
    if len(cached_movies):
      return success_res(code=1000, data=cached_movies, msg='success')
    try:
      spider = Spider()
      movies = spider.get_movies(const.BASE_URL)
      for movie in movies:
        create_movie(movie)
      cached_movies = session.query(Movie).filter(Movie.id.between((page_now - 1) * page_size + 1, page_now * page_size)).all()
      return success_res(code=1000, data=cached_movies, msg='success')
    except:
      return err_res(code=0 , msg='err')