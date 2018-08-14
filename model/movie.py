# -*- coding: UTF-8 -*-
import sqlalchemy
from app import BaseModel, session

class Movie(BaseModel):
  __tablename__ = 'movie'
  __table_args__ = {
    "mysql_engine": "InnoDB",
    "mysql_charset": "utf8"
  }
  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  title = sqlalchemy.Column(sqlalchemy.String(80), unique=False)
  info = sqlalchemy.Column(sqlalchemy.String(80), unique=False)
  rating_num = sqlalchemy.Column(sqlalchemy.Float, unique=False)
  rating_people_count = sqlalchemy.Column(sqlalchemy.Integer, unique=False)
  slogan = sqlalchemy.Column(sqlalchemy.String(80), unique=False)
  movie_img = sqlalchemy.Column(sqlalchemy.String(80), unique=False)

  def __repr__(self):
    data = (self.id, self.title, self.info, self.rating_num, self.rating_people_count, self.slogan, self.movie_img)
    movie = "TOP%s:\n电影名称：%s\n电影信息：%s\n电影评分：%s\n电影评价人数：%s\n电影 slogan：%s\n电影海报：%s\n"%(data)
    return movie

def create_movie(fetched_movie):
  movie = Movie(
    id=fetched_movie['movie_index'],
    title=fetched_movie['movie_title'],
    info=fetched_movie['movie_info'],
    rating_num=fetched_movie['movie_rating_num'],
    rating_people_count=fetched_movie['rating_people_count'],
    slogan=fetched_movie['movie_slogan'],
    movie_img=fetched_movie['movie_img']
  )

  session.add(movie)
  try:
    session.commit()
  except BaseException:
    return 0
  else:
    return movie.id 