import requests
import json
import re
from bs4 import BeautifulSoup
from lxml import html
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class moviehtml(Base):
#     __tablename__ = 'moviehtml'
#     id = Column(String, primary_key=True)
#     html = Column(String, nullable=False)
#
#
# engine = create_engine('mysql+mysqlconnector://root:0123456789@localhost:3306/movieinformation')
# DBSession = sessionmaker(bind=engine)

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
            # session = DBSession()
            # new_moviehtml = moviehtml(id=x, html=soup)
            # session.add(new_moviehtml)
            # session.commit()
        else:
            continue
        # session.close()

        for i in soup:
            aa = i.find('a')
            u = 'http://www.zmz2019.com' + aa.get('href')
            n = requests.Session().get(u).text
            # print(n)
            soup2 = BeautifulSoup(n, "lxml")
            soup2 = soup2.find_all('div', 'imglink')
            for ii in soup2:
                img = ii.find_all('img')
                # image = img[img.find('\"')+1:img.find('\"')]
                print(img)
                # print(image)
                # print('ok')
            # print(soup2)

print(my_html(1))
