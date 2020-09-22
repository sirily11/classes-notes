from docs_generator.docs_generator import convert_notebook_to_html
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import shutil
from os.path import join

MIMETYPES = {
    "application/vnd.google.colaboratory": "application/vnd.jupyter"
}


def clear(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def download_file(drive: GoogleDrive, prev_path: str, folder_id: str, target_folder: str):
    file_list = drive.ListFile(
        {'q': f"'{folder_id}' in parents"}).GetList()
    for file1 in file_list:
        is_folder = file1['mimeType'] == 'application/vnd.google-apps.folder'
        file_id = file1['id']
        name = file1['title']
        mimetype = file1.get('mimeType')
        download_path = join(target_folder, prev_path, name)
        if is_folder:
            new_prev_path = join(prev_path, name)
            os.makedirs(download_path)
            download_file(drive=drive, prev_path=new_prev_path, folder_id=file_id, target_folder=target_folder)
        else:
            try:
                print(f"Downloading file: {name}")
                gfile = drive.CreateFile({'id': file_id})
                download_mimeType = MIMETYPES.get(mimetype)
                if download_mimeType:
                    gfile.GetContentFile(str(download_path), mimetype=download_mimeType)

            except Exception as e:
                print(name, e)


def sync_google_drive(target: str):
    """
    Sync google drive to target folder
    :param target: target folder
    :return:
    """
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    download_file(drive=drive, prev_path='', folder_id='1udyW1umbgNzhAkeWc8h-ZXgM-k0OC1aq', target_folder=target)


if __name__ == '__main__':
    if not os.getenv('ci'):
        clear('notebooks')
        sync_google_drive("notebooks")
    convert_notebook_to_html(site_name="Class Notes")
    print("Copy index.md")
    with open('README.md', 'r') as f:
        content = f.read()
        with open('docs/index.md', 'w') as f1:
            f1.write(content)
