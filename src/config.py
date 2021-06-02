from dotenv import load_dotenv
import os

load_dotenv("../.env")

IMAGES_DIR = os.path.join('../static', 'images')

UPLOAD_FOLDER = IMAGES_DIR
SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
