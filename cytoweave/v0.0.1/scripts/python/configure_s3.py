import os
import boto3


def configure_s3_bucket():

    if os.getenv("AWS_ACCESS_KEY_ID") is None:
        raise ValueError("AWS_ACCESS_KEY_ID must be set")
    s3_access_key = os.getenv("AWS_ACCESS_KEY_ID")

    if os.getenv("AWS_SECRET_ACCESS_KEY") is None:
        raise ValueError("AWS_SECRET_ACCESS_KEY must be set")
    s3_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if os.getenv("AWS_ENDPOINT_URL") is None:
        raise ValueError("AWS_ENDPOINT_URL must be set")
    s3_endpoint_url = os.getenv("AWS_ENDPOINT_URL")

    if os.getenv("CYTOWEAVE_BUCKET_NAME") is None:
        raise ValueError("CYTOWEAVE_BUCKET_NAME must be set")
    s3_bucket_name = os.getenv("CYTOWEAVE_BUCKET_NAME")

    s3 = boto3.resource('s3',
                        endpoint_url=s3_endpoint_url,
                        aws_access_key_id=s3_access_key,
                        aws_secret_access_key=s3_secret_key,
                        aws_session_token=None,
                        config=boto3.session.Config(signature_version='s3v4'),
                        verify=False)
    s3_bucket = s3.Bucket(s3_bucket_name)

    return s3_bucket, s3_bucket_name
