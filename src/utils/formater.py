import csv
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from sqlalchemy.testing.suite.test_reflection import metadata
from sympy.physics.units.definitions.unit_definitions import oersted
from torch.distributed.rpc.api import method_name

from mimr import documents


class FromHTMLtoCVS:
    def __init__(self, html_path: str, cvs_output_file: str):
        self.html_path = html_path
        self.cvs_output_file = cvs_output_file

    def clear_data(self):
        with open(self.html_path, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        text_tags = soup.find_all('div', class_='text')
        text_values = [tag.get_text(separator=' ', strip=True) for tag in text_tags]

        with open(self.cvs_output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for text in text_values:
                if len(text) > 20:
                    for line in text.split('\n'):  # Разбиваем текст на строки
                        writer.writerow([line])  # Каждая строка записывается как отдельная


class CVStoDocuments:
    def __init__(self, cvs_output_file: str, documents_path: str):
        self.cvs_output_file = cvs_output_file
        self.documents_path = documents_path

    def format(self):
        documents_list = []
        _id = 0
        with open(self.cvs_output_file, 'r') as f:
            for line in f.readlines():
                documents_list.append(
                    Document(page_content=line, metadata={'id': _id})
                )
                _id += 1
        with open(self.documents_path, 'w') as f1:
            f1.write('from langchain.docstore.document import Document\n')
            f1.write('documents = ')
            f1.write(str(documents_list))


root_path = '/home/iwan/PycharmProjects/Telegram-Chat-Bot/src/'
html_path = root_path + 'mimr.html'
cvs_output_file = root_path + 'mimr.csv'
documents_path = root_path + 'mimr.py'

# Создаем экземпляр класса и запускаем метод
FromHTMLtoCVS(html_path=html_path, cvs_output_file=cvs_output_file).clear_data()
CVStoDocuments(cvs_output_file=cvs_output_file, documents_path=documents_path).format()
