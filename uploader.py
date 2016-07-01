import os
from os.path import splitext, basename
import magic
from settings import *
import boto3

s3 = boto3.resource('s3')


def get_uploader():
    return my_import(UPLOADER_CLASS)()


class Uploader(object):

    def upload(self, f):
        raise NotImplemented()


class S3Uploader(Uploader):

    def __init__(self):
        self.bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)

    def upload(self, f, metadata):
        filename = basename(f)

        objs = list(self.bucket.objects.filter(Prefix=filename))
        if len(objs) > 0 and objs[0].key == filename:
                print("File already exists: ", filename)
        else:
            print("File doesn't exists. Uploading ", filename)
            data = open(f, 'rb')
            self.bucket.put_object(Key=filename, Body=data, ACL='public-read',
                                   ContentType=magic.from_file(f, mime=True), Metadata=metadata)
