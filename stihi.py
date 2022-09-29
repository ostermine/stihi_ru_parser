import requests
from bs4 import BeautifulSoup
import datetime
import random
import re


HTML_REGEX = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
BASE_URL = 'https://stihi.ru/poems/list.html?'
POEM_URL = 'https://stihi.ru/'
TODAY = datetime.datetime.today()

# удаляет из текста html теги
def cleanhtml(raw_html):
  cleantext = re.sub(HTML_REGEX, '', raw_html)
  return cleantext

# функция принимает 3 необязательных параметра - год YYYY, месяц MM, день DD и возвращает количество стихов, которые были написаны в этот день
def poemCount(year=TODAY.strftime("%Y"), month=TODAY.strftime("%m"), day=TODAY.strftime("%d")):
    url = BASE_URL + f'day={day}&month={month}&year={year}&topic=all'
    try:
        response = requests.get(url)
    except:
        print('Не удалось спарсить, попробуйте позднее')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        poemLinks = soup.find_all('div', class_='textlink nounline')
        return poemLinks[0].text.split('\n')[1].split('-')[0]

# функция принимает 3 необязательных параметра - год YYYY, месяц MM, день DD и возвращает рандомный стих, написанный в этот день
def randomPoem(year=TODAY.strftime("%Y"), month=TODAY.strftime("%m"), day=TODAY.strftime("%d")):
    url = POEM_URL + f'{year}/{month}/{day}/' + str(random.randint(1, int(poemCount(year,month,day))))
    try:
        response = requests.get(url)
    except:
        print('Не удалось спарсить, попробуйте позднее')
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        poem = soup.find_all('div', class_='text')
        print(cleanhtml(str(*poem) + f'\n{url}'))

if __name__ == "__main__":
    randomPoem()