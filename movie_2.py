import requests
import json
import re
from bs4 import BeautifulSoup
from lxml import html
from sqlalchemy import Column, String, Integer, BLOB, Text,  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class moviehtml(Base):
    __tablename__ = 'moviehtml'
    id = Column(String, primary_key=True)
    html = Column(Text, nullable=False)


# class movie(Base):
#     __tablename__ = 'movie'
#     image = Column(BLOB)


engine = create_engine('mysql+mysqlconnector://root:0123456789@localhost:3306/movieinformation')
DBSession = sessionmaker(bind=engine)

url = 'http://www.zmz2019.com/resourcelist/?page='

# n = requests.Session().get(url).text
# soup = BeautifulSoup(n, "lxml")
# soup = soup.find('div', class_='pages').get_text()
# page = int(soup.split('...')[1])


def my_html(page):
    for x in range(page + 1):
        if x > 0:
            print('正在下载第' + str(x) + '页')
            h = requests.Session().get(url + str(x)).text
            soup = BeautifulSoup(h, "lxml")
            # soup = soup.find_all('h3', 'f14')
            # print(soup)
            session = DBSession()
            new_moviehtml = moviehtml(id=x, html=str(soup))
            session.add(new_moviehtml)
            session.commit()
        else:
            continue
        session.close()

        # for i in soup:
        #     aa = i.find('a')
        #     u = 'http://www.zmz2019.com' + aa.get('href')
        #     n = requests.Session().get(u).text
        #     soup2 = BeautifulSoup(n, "lxml")
        #     soup2 = soup2.find('div', class_='imglink')
        #     for ii in soup2:
        #         img = ii.get('href')
        #         print(img)
        #         session = DBSession()
        #         new_movie = movie(image=img)
        #         session.add(new_movie)
        #         session.commit()
        # session.close()

print(my_html(10))

# m = []
# for x in range(3):
#     if x > 0:
#         session = DBSession()
#         newhtml = session.query(moviehtml).filter(moviehtml.id == str(x)).one()
#         newhtml = newhtml.html
#         # print(newhtml)
#         session.close()
#         newsoup = BeautifulSoup(newhtml, 'lxml')
#         newsoup = newsoup.find_all('h3', 'f14')
#     else:
#         continue
#     for newi in newsoup:
#         # print(newi)
#         a = newi.get_text('|')
#         aa = newi.find('a')
#         w = a.split('|')
#         t = w[0]
#         d = w[1]
#         u = 'http://www.zmz2019.com' + aa.get('href')
#         n = requests.Session().get(u).text
#         soup2 = BeautifulSoup(n, "lxml")
#         soup2 = soup2.find('div', class_='imglink')
#         for ii in soup2:
#             img = ii.get('href')
#             # print(img)
#         country = d[d.find('【') + 1:d.find('】')]
#         name = d[d.find('《') + 1:d.find('》')]
#         ename = d[d.find('(') + 1:d.find(')')]
#         y = re.search(r'\d{1,4}$', d)
#         if y is not None:
#             y = y.group(0)
#         print(y)
#         j = [{'type': t, 'country': country, 'ChineseName': name, 'EnglishName': ename, 'year': y, 'image': img}]
#         m.append(j)
# print(json.dumps(m, ensure_ascii=False))