from os import listdir
from os.path import isfile, splitext, basename
from epubzilla.epubzilla import Epub
from PIL import Image
import StringIO
from settings import *
from uploader import get_uploader


class BooksReader(object):

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

    def extract_informations(self, books):
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

        return books_map

    def build_page(self):
        page = "Cover | Info\n"
        page += "---------|---------\n"
        for k in sorted(self.books_map.keys()):
            v = self.books_map.get(k)

            title = v.get('title')
            author = v.get('author')
            link_pdf = ""
            link_epub = ""
            link_mobi = ""
            link_cover = ""

            if v.get('.pdf'):
                link_pdf = 'https://s3-us-west-2.amazonaws.com/%s/%s' % (AWS_STORAGE_BUCKET_NAME,
                                                                         basename(v.get('.pdf')))

            if v.get('.epub'):
                link_epub = 'https://s3-us-west-2.amazonaws.com/%s/%s' % (AWS_STORAGE_BUCKET_NAME,
                                                                          basename(v.get('.epub')))

            if v.get('.mobi'):
                link_mobi = 'https://s3-us-west-2.amazonaws.com/%s/%s' % (AWS_STORAGE_BUCKET_NAME,
                                                                          basename(v.get('.mobi')))

            if v.get('cover'):
                link_cover = 'https://s3-us-west-2.amazonaws.com/%s/%s' % (AWS_STORAGE_BUCKET_NAME,
                                                                           basename(v.get('cover')))

            page += '![%s](%s "%s") | Name: %s <br /> Author: %s <br />PDF: %s<br />MOBI: %s<br />EPUB: %s' % \
                    (title, link_cover, title, title, author, link_pdf, link_epub, link_mobi)

        self.page = page

    def upload_books(self):
        uploader = get_uploader()
        for k, v in self.books_map.iteritems():
            for e in ['.epub', '.mobi', '.pdf', 'cover']:
                elem = v.get(e)
                if elem:
                    uploader.upload(elem)

    def __init__(self, path):
        self.page = None
        self.books_map = None
        books_list = self.list_books(path)

        self.books_map = self.extract_informations(books_list)

        self.upload_books()
        self.build_page()
        self.post_page_generated()
        self.clean_up()

    def clean_up(self):
        for k, v in self.books_map.iteritems():
            cover = v.get('cover')
            if cover and isfile(cover):
                os.remove(cover)


    def post_page_generated(self):
        pass


def main():
    BooksReader(BOOKS_PATH)

if __name__ == "__main__":
    main()