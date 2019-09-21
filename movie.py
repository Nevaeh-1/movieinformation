import requests
import json
import re
from bs4 import BeautifulSoup
from lxml import html
from sqlalchemy import Column, String, Integer, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class moviehtml(Base):
    __tablename__ = 'moviehtml'
    id = Column(String, primary_key=True)
    html = Column(Text, nullable=False)


class movie(Base):
    __tablename__ = 'movie'
    id = Column(String(20), primary_key=True)
    type = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    chinese_name = Column(String(150), nullable=False)
    english_name = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    url = Column(String(200), nullable=False)


engine = create_engine('mysql+mysqlconnector://root:0123456789@localhost:3306/movieinformation')
DBSession = sessionmaker(bind=engine)

url = 'http://www.zmz2019.com/resourcelist/?page='
n = requests.Session().get(url).text
soup = BeautifulSoup(n, "lxml")
soup = soup.find('div', class_='pages').get_text()
page = int(soup.split('...')[1])
m = []
l = 0
for x in range(page):
    print('正在下载第' + str(x) + '页')
    if x > 0:
        h = requests.Session().get(url + str(x)).text
        soup = BeautifulSoup(h, "lxml")
        soup = soup.find_all('h3', 'f14')
    else:
        continue
    for i in soup:
        print(i)
        a = i.get_text('|')
        aa = i.find('a')
        w = a.split('|')
        t = w[0]
        d = w[1]
        print(d)
        u = 'http://www.zmz2019.com' + aa.get('href')
        country = d[d.find('【') + 1:d.find('】')]
        name = d[d.find('《') + 1:d.find('》')]
        ename = d[d.find('(') + 1:d.find(')')]
        y = re.search(r'\d{1,4}$', d)
        if y is not None:
            y = y.group(0)
        print(y)
        j = [{'type': t, 'country': country, 'ChineseName': name, 'EnglishName': ename, 'year': y}]
        m.append(j)
        l = l + 1
        session = DBSession()
        new_movie = movie(id=l, type=t, country=country, chinese_name=name, english_name=ename, year=y, url=u)
        session.add(new_movie)
        session.commit()
    session.close()
print(json.dumps(m, ensure_ascii=False))
