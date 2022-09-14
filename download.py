"""

    PROJECT: PyGCCS
    FILENAME: download.py
    AUTHOR: David NAISSE
    DATE: September 13, 2022

    DESCRIPTION: Download file from GCP bucket.
    
"""

import argparse
import logging
import os
from typing import List

from google.cloud import storage
from tqdm import tqdm

logging.basicConfig(
    format='%(asctime)s '
           '%(pathname)s '
           'function:%(funcName)s() '
           '[%(levelname)s] --> %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.info


def download_from_bucket(project_id: str, bucket_name: str, destination: str, files=List[str], key: str = "key.json"):
    """
    Download files from GCP bucket.

    :param project_id: google cloud project ID
    :param bucket_name: google cloud bucket name
    :param destination: local destination folder
    :param files: files to download from GC bucket
    :param key: JSON service account key
    """

    # Set env variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key
    log("Environment variable has been set. ")

    # Initialise a client
    client = storage.Client(project_id)
    log("Client has been initialized. ")

    # Create a bucket object for our bucket
    bucket = client.get_bucket(bucket_name)

    # Download form bucket for each file
    for file in tqdm(files, desc=f"Downloading files to {destination}/"):
        # Get only filename
        filename = file.split('/')[-1]

        # Create a blob object from the filepath
        blob = bucket.blob(file)

        # Download the file to a destination
        blob.download_to_filename(destination + filename)
        log(f"File has been downloaded to {destination + filename}. ")


if __name__ == "__main__":
    # Init. parser
    parser = argparse.ArgumentParser("Download file from GCS bucket. ")
    parser.add_argument("-p", "--project_id", help="Google Cloud project ID. ", type=str)
    parser.add_argument("-b", "--bucket_name", help="Google Cloud bucket name. ", type=str)
    parser.add_argument("-d", "--destination", help="Local destination folder. ", type=str, default="")
    parser.add_argument("-f", "--files", help="Files to download from GC bucket separated by &. ", type=str)
    parser.add_argument("-k", "--key", help="JSON key for bucket access. ", default="key.json")
    args = parser.parse_args()

    # Run main script
    download_from_bucket(
        project_id=args.project_id,
        bucket_name=args.bucket_name,
        destination=args.destination,
        files=args.files.split('&'),
        key=args.key
    )
