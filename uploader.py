import os
from os.path import splitext, basename, join
import magic
from settings import *
import boto3

s3 = boto3.resource('s3')

uploader_instance = None


def get_uploader():
    global uploader_instance
    if uploader_instance is None:
        uploader_instance = my_import(UPLOADER_CLASS)()
    return uploader_instance


class Uploader(object):

    def upload(self, f):
        raise NotImplemented()

    def download(self, f):
        raise NotImplemented()


class S3Uploader(Uploader):

    def __init__(self):
        self.bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)

    def upload(self, f, metadata={}, override=False):
        filename = basename(f)

        objs = list(self.bucket.objects.filter(Prefix=filename))
        if not override and len(objs) > 0 and objs[0].key == filename:
            print("File already exists: ", filename)
        else:
            if not override:
                print("File doesn't exists. Uploading ", filename)
            else:
                print("Uploading", filename)
            data = open(f, 'rb')
            self.bucket.put_object(Key=filename, Body=data, ACL='public-read',
                                   ContentType=magic.from_file(f, mime=True), Metadata=metadata)

    def download(self, f):
        filename = basename(f)

        objs = list(self.bucket.objects.filter(Prefix=filename))
        if len(objs) > 0 and objs[0].key == filename:
            self.bucket.download_file(filename, join(dirname(__file__), filename))
