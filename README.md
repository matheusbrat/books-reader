This library will try to find any epub, mobi, pdf files and then:
    * Generate cover image from epub metadata
    * Upload files to S3
    * Build page with cover and links to s3 files for download


Dependencies:
* libmagic
* requirements.txt


ENV:
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
BOOKS_PATH=
UPLOADER_CLASS=
