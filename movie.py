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
    year = Column(Integer)
    url = Column(String(200), nullable=False)
    image = Column(String)


engine = create_engine('mysql+mysqlconnector://root:0123456789@localhost:3306/movieinformation')
DBSession = sessionmaker(bind=engine)

url = 'http://www.zmz2019.com/resourcelist/?page='
n = requests.Session().get(url).text
soup = BeautifulSoup(n, "lxml")
soup = soup.find('div', class_='pages').get_text()
page = int(soup.split('...')[1])


def my_html(page):
    for x in range(page + 1):
        if x > 0:
            print('正在下载第' + str(x) + '页')
            h = requests.Session().get(url + str(x)).text
            soup = BeautifulSoup(h, "lxml")
            session = DBSession()
            new_moviehtml = moviehtml(id=x, html=str(soup))
            session.add(new_moviehtml)
            session.commit()
        else:
            continue
        session.close()


print(my_html(20))

m = []
l = 0
for id1 in range(21):
    if id1 > 0:
        session = DBSession()
        newhtml = session.query(moviehtml).filter(moviehtml.id == str(id1)).one()
        newhtml = newhtml.html
        # print(newhtml)
        session.close()
        newsoup = BeautifulSoup(newhtml, 'lxml')
        newsoup = newsoup.find_all('h3', 'f14')
        for i in newsoup:
            # print(i)
            a = i.get_text('|')
            aa = i.find('a')
            w = a.split('|')
            t = w[0]
            d = w[1]
            # print(t)
            u = 'http://www.zmz2019.com' + aa.get('href')
            n = requests.Session().get(u).text
            soup2 = BeautifulSoup(n, "lxml")
            soup2 = soup2.find('div', class_='imglink')
            for ii in soup2:
                print(ii)
                img = ii.get('href')
                # print(img)
            country = d[d.find('【') + 1:d.find('】')]
            name = d[d.find('《') + 1:d.find('》')]
            ename = d[d.find('(') + 1:d.find(')')]
            y = re.search(r'\d{1,4}$', d)
            if y is not None:
                y = y.group(0)
            # print(y)
            j = [{'type': t, 'country': country, 'ChineseName': name, 'EnglishName': ename, 'year': y, 'image': img}]
            m.append(j)
            l = l + 1
            print('已经爬取第' + str(l) + '个')
            session = DBSession()
            new_movie = movie(id=l, type=t, country=country, chinese_name=name, english_name=ename, year=y, url=u, image=img)
            session.add(new_movie)
            session.commit()
        session.close()
    else:
        continue
print(json.dumps(m, ensure_ascii=False))
