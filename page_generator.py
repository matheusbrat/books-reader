from settings import AWS_STORAGE_BUCKET_NAME
from os.path import basename


class BooksLibraryPageGenerator(object):

    @classmethod
    def build_page(cls, books_map):
        page = "Cover | Info\n"
        page += "---------|---------\n"
        for k in sorted(books_map.keys()):
            v = books_map.get(k)

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

            created_at = v.get('created_at', str('1970-01-01'))

            page += '![%s](%s "%s") | Name: %s <br /> Author: %s <br />Created at: %s<br />[PDF](%s)<br />[MOBI](%s)<br />[EPUB](%s)' % \
                    (title, link_cover, title, title, author, created_at, link_pdf, link_mobi, link_epub)
            page += '\n'

        return page
