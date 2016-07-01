from os.path import join, dirname
from dotenv import load_dotenv
import os


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

UPLOADER_CLASS = os.environ.get("UPLOADER_CLASS")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
BOOKS_PATH = os.environ.get("BOOKS_PATH")