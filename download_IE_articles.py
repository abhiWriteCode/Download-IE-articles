import requests
from bs4 import BeautifulSoup
import json
import re
import os
import argparse


parser = argparse.ArgumentParser(description='Read IE articles')

parser.add_argument('--url', type=str, required=True,
                    help='Enter a URL')
args = vars(parser.parse_args())


def get_title(soup):
    return soup.title.get_text()


def get_description(soup):
    return soup.find(name='meta', attrs={'name': 'description'})['content']


def get_article_details(soup):
    doc = soup.find(name="script", type="application/ld+json", string=re.compile('articleBody'))
    if doc is not None:
        doc_text = doc.get_text()
        doc_text_json = json.loads(doc_text)
        article_body = doc_text_json.get('articleBody')
        date_published = doc_text_json.get('datePublished')
        return {
            'article_body': article_body,
            'date_published': date_published
        }


if __name__ == "__main__":
    url = args['url']
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        title = get_title(soup)
        description = get_description(soup)
        article_details = get_article_details(soup)

        if article_details is not None:
            file_name = 'IE_article.txt'
            if os.path.exists(file_name):
                os.remove(file_name)
                
            with open(file_name, "a", encoding="utf-8") as f:
                print(f'Title: {title}', file=f)
                print(f'Description: {description}', file=f)
                print(f'Date: {article_details["date_published"]}\n', file=f)
                print(f'Article: \n{article_details["article_body"]}', file=f)
                print('\nOutput file:', file_name)
