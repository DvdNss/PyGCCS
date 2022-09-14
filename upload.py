"""

    PROJECT: PyGCCS
    FILENAME: upload.py
    AUTHOR: David NAISSE
    DATE: September 13, 2022

    DESCRIPTION: Upload files to GCP bucket.
    
"""
import argparse
import logging
import os

from google.cloud import storage
from tqdm import tqdm

logging.basicConfig(
    format='%(asctime)s '
           '%(pathname)s '
           'function:%(funcName)s() '
           '[%(levelname)s] --> %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.info


def upload_to_bucket(project_id: str, bucket_name: str, destination: str, rename: str, files, folder, key: str):
    """
    Upload files or folder to GCP bucket.

    :param rename: new names for files
    :param project_id: google cloud bucket ID
    :param bucket_name: google cloud bucket name
    :param destination: destination folder for files/folder
    :param files: files to upload
    :param folder: folder to upload
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

    # If folder mode, redefine files
    if folder is not None:
        files = os.listdir(folder)
        files = [f"{os.path.join(folder, file)}" for file in files]

    # Upload files to bucket
    for file in tqdm(files, desc=f"Uploading files to {bucket_name}/{destination}"):

        # check if current path is a file
        if os.path.isfile(file):
            # Rename file if needed
            filename = file.split('/')[-1] if rename is None else rename

            # Create a blob object from the filepath
            blob = bucket.blob(destination + filename)

            # Upload the file to a destination
            blob.upload_from_filename(file)

    log(f"Files have been uploaded to {bucket_name + '/' + destination}. ")


if __name__ == "__main__":
    # Init. parser
    parser = argparse.ArgumentParser("Upload files or folders to GCS bucket. ")
    parser.add_argument("-p", "--project_id", help="Google Cloud project ID. ", type=str)
    parser.add_argument("-b", "--bucket_name", help="Google Cloud bucket name. ", type=str)
    parser.add_argument("-d", "--destination", help="Google Cloud bucket destination. ", type=str)
    parser.add_argument("-r", "--rename", help="New name for file in bucket. ", type=str, default=None)
    parser.add_argument("-f", "--files", help="Files to upload to GC bucket separated by &. ", default=None)
    parser.add_argument("--folder", help="Folder to upload to GC bucket. ", default=None)
    parser.add_argument("-k", "--key", help="Path to IAM JSON service account key for bucket access. ",
                        default="key.json")
    args = parser.parse_args()

    # Run main script
    upload_to_bucket(
        project_id=args.project_id,
        bucket_name=args.bucket_name,
        destination=args.destination,
        rename=args.rename if len(args.files.split('&')) > 1 else None,
        files=args.files.split('&') if args.files is not None else None,
        folder=args.folder,
        key=args.key
    )
