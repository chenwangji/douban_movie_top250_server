# -*- coding: UTF-8 -*-

import requests
import re
from lxml import html

BASE_URL = 'https://movie.douban.com/top250'

class Spider():
  movie_list = []

  def get_movies(self, base_url):
    COUNT_OF_SINGLE_PAGE = 25
    TOTAL = 250
    start = 0
    while start <= TOTAL:
      params = { 'start': start, 'filter': '' }
      url = base_url + '?start={0[start]}&filter={0[filter]}'.format(params)
      res = requests.get(url).content
      current_html = html.fromstring(res)
      self.get_sigle_page_movies(current_html, start)
      # 换至下页
      start += COUNT_OF_SINGLE_PAGE
    return self.movie_list

  def get_sigle_page_movies(self, current_html, start):
    movie_index = start
    for i in current_html.xpath('//div[@class="item"]'):
      try:
        # index
        movie_index += 1
        # 电影名称
        movie_title = i.xpath('div[@class="info"]/div[@class="hd"]/a/span[@class="title"]/text()')[0]
        # 电影信息
        movie_info = i.xpath('div[@class="info"]/div[@class="bd"]/p[1]/text()')[0].strip()
        # 电影评分
        movie_rating_num = i.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
        # 电影评价人数
        pattern = re.compile(r'^\d+')
        rating_people_count = re.search(pattern, i.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[last()]/text()')[0]).group()
        # 电影 slogan
        movie_slogan = i.xpath('div[@class="info"]/div[@class="bd"]//span[@class="inq"]/text()')[0]
        # 电影海报
        movie_img = i.xpath('div[@class="pic"]//img/@src')[0]

        data = {
          'movie_index': movie_index, 
          'movie_title': movie_title, 
          'movie_info': movie_info, 
          'movie_rating_num': movie_rating_num, 
          'rating_people_count': rating_people_count, 
          'movie_slogan': movie_slogan, 
          'movie_img': movie_img
        }
        self.save_data(data)
      except: 
        pass

  def save_data(self, data):
    self.movie_list.append(data)
