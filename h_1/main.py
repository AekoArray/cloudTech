import sys
import boto3
from io import BytesIO
from pathlib import Path
import os

session = boto3.session.Session()
s3 = session.client(
    service_name="s3",
    endpoint_url="https://storage.yandexcloud.net",
    region_name="ru-central1",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)


def get_album_pictures(album):
    result = []
    for obj in s3.list_objects(Bucket=album)["Contents"]:
        result.append(obj["Key"])
    return result


def get_albums():
    result = []
    for bucket in s3.list_buckets()["Buckets"]:
        result.append(bucket["Name"])
    return result


def _list(parameters):
    if "-a" in parameters:
        pictures = get_album_pictures(parameters[parameters.index("-a") + 1])
        print("Список фотографий в альбоме")
        for picture in pictures:
            print(f"{str(pictures.index(picture) + 1)}. {picture}")
    else:
        albums = get_albums()
        print("Список альбомов:")
        for album in albums:
            print(f"{str(albums.index(album) + 1)}. {album}")


def upload_bucket(bucket, files):
    for file in files:
        data = BytesIO(open(str(file), "rb").read())
        data.name = file.name
        s3.upload_fileobj(data, bucket, file.name)


def _upload(parameters):
    if "-p" not in parameters or "-a" not in parameters:
        raise ValueError("Не указан один из параметров")
    directory = Path(parameters[parameters.index("-p") + 1])
    album_name = parameters[parameters.index("-a") + 1]
    if not Path.is_dir(directory):
        raise ValueError("Указанный путь не является директорией")
    pictures = []
    for file in directory.iterdir():
        if not Path.is_dir(file) and (".jpeg" in file.name or ".jpg" in file.name):
            pictures.append(file)
    if album_name not in get_albums():
        s3.create_bucket(Bucket=album_name)
    upload_bucket(album_name, pictures)


def download_bucket(bucket):
    files = []
    pictures = get_album_pictures(bucket)
    for file in pictures:
        files.append({"name": file, "data": s3.get_object(Bucket=bucket, Key=file)["Body"].read()})
    return files


def _download(parameters):
    if "-p" not in parameters or "-a" not in parameters:
        raise ValueError("Не указан один из параметров")
    directory = Path(parameters[parameters.index("-p") + 1])
    album_name = parameters[parameters.index("-a") + 1]
    if not Path.is_dir(directory):
        raise ValueError("Указанный путь не является директорией")
    Path.mkdir(directory / album_name, exist_ok=True)
    pictures = download_bucket(album_name)
    for picture in pictures:
        file_path = directory / album_name / picture["name"]
        file = open(file_path, "wb")
        file.write(picture["data"])


def main(argv=None):
    if "list" in argv:
        _list(argv)
    elif "upload" in argv:
        _upload(argv)
    elif "download" in argv:
        _download(argv)
    else:
        raise ValueError("No command was given.")


if __name__ == "__main__":
    main(sys.argv)
