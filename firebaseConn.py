import firebase_admin 
import os
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

cred = credentials.Certificate("go-test1-5cdaf-firebase-adminsdk-ow1u2-24dd026a2b.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'go-test1-5cdaf.appspot.com'
})

def generate_download_url(file_path):
    bucket = storage.bucket()
    blob = bucket.blob(file_path)

    download_url = blob.generate_signed_url(
        version='v4',
        expiration=300,
        method='GET'
    )
    return download_url

def upload_image(image_path, destination_path):
    try:
        if not os.path.isfile(image_path):
            raise Exception(f"File not found: {image_path}")

        bucket = storage.bucket()
        blob = bucket.blob(destination_path)
        
        # Upload the local file to the storage path
        blob.upload_from_filename(image_path)
        print(f"Image uploaded to {destination_path}")

        # url = blob.generate_signed_url(
        #     version='v4',
        #     expiration=timedelta(days=1),
        #     method='GET'
        # )

        # print("Image URL:", url)

    except Exception as error:
        print("Failed to upload image: {error}")


def read_by_document(collection, document_id):
    db = firestore.client()
    doc_ref = db.collection(collection).document(document_id)
    document = doc_ref.get()
    if document.exists:
        print('Document data:', document.to_dict())
    else:
        print('No such document!')

def read_by_document_all(collection, document_id, fields):
    db = firestore.client()
    doc_ref = db.collection(collection).document(document_id)

    document = doc_ref.get(field_paths=fields)

    if document.exists:
        data = document.to_dict()
        print("Document data:")
        for field in fields:
            print(f"{field}: {data.get(field)}")
    else:
        print("Document not exists")

# default_app = firebase_admin.initialized_app()
if __name__ == '__main__':
    # read_by_document('data', '1')

    """run """
    # collection = 'data'
    # document_id = '1'
    # fields = ['field1', 'field2', 'field3']
    # read_by_document_all(collection, document_id, fields)

    """run upload image function"""
    # upload_image('image/test.png', 'test1/test.png')

    """get url path"""
    file_path = 'test1/test.png'
    download_url = generate_download_url(file_path)
    print(download_url)
    