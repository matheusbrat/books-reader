from bookslibrary import BooksLibrary
from settings import *
import subprocess
from os.path import join, abspath


def main():
    bl = BooksLibrary(BOOKS_PATH)
    bl.remote_sync()
    page = bl.generate_page()
    with open('page.md', 'w+') as f:
        f.write(page)

    command = ["sh", POST_PAGE_GENERATED, abspath('page.md')]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = process.communicate()[0]


if __name__ == "__main__":
    main()
