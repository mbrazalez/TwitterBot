import boto3
from botocore.exceptions import ClientError
from configuration import configuration as conf


def s3_save_file(key, content, bucketname=None):
    """Save object to S3 Bucket

    :param key: string
    :param content: the content of the object
    :param bucketname: string
    :return: path of S3 where the object has been stored
    """

    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=content, Bucket=bucketname or conf.S3_BUCKET_STORAGE,
        Key=key)

    path = f'{bucketname or conf.S3_BUCKET_STORAGE}/{key}'

    return path


def s3_get_object(key, bucketname=None):
    """Get object tags from S3 Bucket

    :param key: string
    :param bucketname: string
    :return: the object (bytes)
    """

    s3_client = boto3.client('s3')
    bucket = bucketname or conf.S3_BUCKET_STORAGE

    try:
        object_from_s3 = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
        return object_from_s3.decode('utf-8')
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return None
        else:
            raise e