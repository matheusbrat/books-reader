from os import listdir
from os.path import isfile, splitext, basename
from epubzilla.epubzilla import Epub
from PIL import Image
import StringIO
from settings import *
from uploader import get_uploader
import json
from page_generator import BooksLibraryPageGenerator
from datetime import date

class BooksLibrary(object):
    map_filename = 'books-map.json'

    def __init__(self, path):
        self.uploader = get_uploader()

        self.page = None
        self.books_map = None

        books_list = self.list_books(path)
        self.books_map = self.extract_informations(books_list)

    def __del__(self):
        self.clean_up()

    def list_books(self, path):
        books = []
        for file in listdir(path):
            file_path = join(path, file)
            if isfile(file_path):
                filename, ext = splitext(file)
                if ext in ['.pdf', '.epub', '.mobi']:
                    books.append(file_path)
            else:
                for b in self.list_books(join(path, file)):
                    books.append(b)
        return books

    @classmethod
    def extract_informations(cls, books):
        books_map = {}
        for book in books:
            filename, ext = splitext(basename(book))
            if not books_map.get(filename):
                books_map[filename] = {}
            books_map[filename][ext] = book

            if ext == '.epub':
                epub = Epub.from_file(book)
                image_data = StringIO.StringIO(epub.cover.get_file())
                img = Image.open(image_data)
                img.thumbnail((293, 445), Image.ANTIALIAS)
                img.save(filename + '.jpg', "JPEG")
                books_map[filename]['cover'] = filename + '.jpg'
                books_map[filename]['title'] = epub.title
                books_map[filename]['author'] = epub.author
                books_map[filename]['created_at'] = str(date.today())
                if books_map[filename]['title']:
                    books_map[filename]['title'] = books_map[filename]['title'].encode('ascii', errors='ignore')
                if books_map[filename]['author']:
                    books_map[filename]['author'] = books_map[filename]['author'].encode('ascii', errors='ignore')


        return books_map

    def remote_sync(self):
        self.upload_books()
        self.update_remote_books_map()

    def clean_up(self):
        for k, v in self.books_map.iteritems():
            cover = v.get('cover')
            if cover and isfile(cover):
                os.remove(cover)
        os.remove(self.map_filename)

    def upload_books(self):
        for k, v in self.books_map.iteritems():
            metadata = {'author': v.get('author') or '---', 'title': v.get('title') or '---'}
            for e in ['.epub', '.mobi', '.pdf', 'cover']:
                elem = v.get(e)
                if elem:
                    self.uploader.upload(elem, metadata)

    def update_remote_books_map(self):
        self.load_remote_books_map()
        self.upload_remote_books_map()

    def load_remote_books_map(self):
        self.uploader.download(self.map_filename)

        with open(self.map_filename, 'r') as data_file:
            data = data_file.read()
            if data == '':
                data = '{}'
            data = json.loads(data)

        self.books_map.update(data)

    def upload_remote_books_map(self):
        books_map_text = json.dumps(self.books_map)
        with open(self.map_filename, 'w+') as data_file:
            data_file.write(books_map_text)
        self.uploader.upload(self.map_filename, override=True)

    def generate_page(self):
        page = BooksLibraryPageGenerator.build_page(self.books_map)
        return page
