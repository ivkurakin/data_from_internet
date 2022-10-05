# Написать приложение или функцию, которые собирают основные новости с сайта yandex-новости.
# Для парсинга использовать XPath. Структура данных в виде словаря должна содержать:
# - *название источника;
# - наименование новости;
# - ссылку на новость;
# - дата публикации.

import requests
from lxml import html

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
url = 'http://dzen.ru/news/'
params = {'issue_tld': 'ru',
          'sso_failed': 'blocked',
          'uuid': '4903b767-6a79-4f8e-a5f9-58891638f522'}
response = requests.get(url=url, headers=headers, params=params)
dom = html.fromstring(response.text)
news = dom.xpath('//div[contains(@class,"mg-card ")]')

news_list = []
for item in news:
    item_source = item.xpath('.//span[@class="mg-card-source__source"]/a/text()')
    if len(item_source) == 1:
        item_source = item_source[0]
    else:
        item_source = None
    item_link = item.xpath('.//h2[@class="mg-card__title"]/a/@href')
    if len(item_link) == 1:
        item_link = item_link[0]
    else:
        item_link = None
    item_tittle = item.xpath('.//h2[@class="mg-card__title"]/a/text()')
    if len(item_tittle) == 1:
        item_tittle = item_tittle[0]
    else:
        item_tittle = None
    item_annotation = item.xpath('.//div[@class="mg-card__annotation"]/text()')
    if len(item_annotation) == 1:
        item_annotation = item_annotation[0]
    else:
        item_annotation = None
    item_time = item.xpath('.//span[@class="mg-card-source__time"]/text()')
    if len(item_time) == 1:
        item_time = item_time[0]
    else:
        item_time = None
    news_dict = {'source': item_source,
                 'link': item_link,
                 'tittle': item_tittle,
                 'annotation': item_annotation,
                 'time': item_time}
    news_list.append(news_dict)
for el in news_list:
    print(el)
