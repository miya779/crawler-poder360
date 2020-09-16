#poder360 crawler
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import mysql.connector

#used to convert the string month to mysql numerical format
month = {'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'}

cnx = mysql.connector.connect(user='root',password='root', database='poder_news')
cursor = cnx.cursor()



try:
    for i in range(1, 4087):
        if(i == 1):
            page = requests.get('https://www.poder360.com.br/todas-Noticias/')
        else:
            page = requests.get('https://www.poder360.com.br/todas-Noticias/page/'+str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        #get all links from the page
        news_links = [a['href'] for a in soup.findAll('a',{'class': 'row link-post'})]
        for link in news_links:
            try:
                #print(link)
                #extract title, resume, text and date from the news page and store them in mysql
                news_page = requests.get(link)
                soup = BeautifulSoup(news_page.text,'html.parser')
                article = soup.article
                title = article.h1.text
                summary = soup.find('div',{'class':'resume'}).text.strip().replace('\n','. ')
                text = soup.find('div',{'class':'content wp cropped js-mediator-article'}).text.replace("Continuar lendo","").strip().replace('\n','. ').replace("Receba a newsletter do Poder360todos os dias no seu e-mail","").replace("\xa0", " ")
                date_hour = soup.find('p',{'class': 'author'}).text
                date_hour = re.search('(\d{1,2})\.([a-zA-Z]{3})\.(\d{4})[^0-9]*(\d{1,2})h(\d{1,2})',date_hour)
                date = date_hour.group(3) + "-" + month[date_hour.group(2)] + "-" + date_hour.group(1) # AAAA-MM-DD
                hour = date_hour.group(4) + ":" + date_hour.group(5) + ":00" # HH:MM:SS
                #insert news into mysql
                query = "INSERT INTO news (link, date, time, title, summary,text) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (link, date, hour, title, summary, text)
                cursor.execute(query, values)
                cnx.commit()
            except Exception as e:
                print(str(e))
except Exception as e:
    print(str(e))

cnx.close()
#(atualizado.*|$)?


#link = 'https://www.poder360.com.br/congresso/policia-prende-suspeitos-e-aponta-flordelis-como-mandante-de-assassinato/'
#news_page = requests.get(link)
#soup = BeautifulSoup(news_page.text,'html.parser')
#article = soup.article
#title = article.h1.text
#summary = soup.find('div',{'class':'resume'}).text.strip().replace('\n','. ')
#text = soup.find('div',{'class':'content wp cropped js-mediator-article'}).text.replace("Continuar lendo","").strip().replace('\n','. ').replace("Receba a newsletter do Poder360todos os dias no seu e-mail","").replace("\xa0", " ")
#date_hour = soup.find('p',{'class': 'author'}).text
#date_hour = re.search('(\d{1,2})\.([a-zA-Z]{3})\.(\d{4})[^0-9]*(\d{1,2})h(\d{1,2})',date_hour)
#date = date_hour.group(3) + "-" + month[date_hour.group(2)] + "-" + date_hour.group(1)
#hour = date_hour.group(4) + ":" + date_hour.group(5) + ":00"
#query = "INSERT INTO news (link, date, time, title, summary,text) VALUES (%s, %s, %s, %s, %s, %s)"
#values = (link, date, hour, title, summary, text)
#cursor.execute(query, values)
#cnx.commit()
