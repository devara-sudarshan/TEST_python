import json
from .uploader import FileUploader

def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    uploader = FileUploader(config)
    uploader.process_files()

if __name__ == '__main__':
    main()
