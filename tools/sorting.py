from itertools import chain

import os
from pathlib import Path
import re
from shutil import move, unpack_archive


files_extension_to_folders = {
    'images': ['.jpeg', '.png', '.jpg', '.svg', '.bmp', '.tiff'],
    'video': ['.avi', '.mp4', '.mov', '.mkv', '.flv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.djvu', '.djv', '.csv', '.fb2'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar']
    }

cyrillic_symbols = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяёъыэ'
cyrillic_to_latin = ('a', 'b', 'v', 'h', 'g', 'd', 'e', 'ye',
                     'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l',
                     'm', 'n', 'o', 'p', 'r', 's', 't', 'u',
                     'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'yu',
                     'ya', 'yo', '', 'y', 'e')
transliteration = {}

for cyrillic, latin in zip(cyrillic_symbols, cyrillic_to_latin):
    transliteration[ord(cyrillic)] = latin
    transliteration[ord(cyrillic.upper())] = latin.upper()

empty_folders = []
folders_to_rename = []


def find_files(path: str) -> None:

    for i in Path(path).iterdir():

        if i.is_file():

            if (ext := i.suffix) in chain(*files_extension_to_folders.values()):

                new_name = normalize(i.stem)

                if ext in files_extension_to_folders['images']:
                    move_file(i, new_name, ext, 'images')

                elif ext in files_extension_to_folders['video']:
                    move_file(i, new_name, ext, 'video')

                elif ext in files_extension_to_folders['documents']:
                    move_file(i, new_name, ext, 'documents')

                elif ext in files_extension_to_folders['audio']:
                    move_file(i, new_name, ext, 'audio')

                elif ext in files_extension_to_folders['install']:
                    move_file(i, new_name, ext, 'install')

                elif ext in files_extension_to_folders['archives']:
                    unpack_archive_file(i, new_name, ext, 'archives')

        elif i.is_dir() and not (i.name in files_extension_to_folders):

            if not os.listdir(i):
                empty_folders.append(i)
            else:
                folders_to_rename.append(i)

            find_files(i)


def move_file(old_file_path, new_name, ext, folder):
    new_path_file = Path(old_file_path.parent, folder)
    new_path_file.mkdir(exist_ok=True, parents=True)
    new_path = (Path(old_file_path.parent, f'{new_name}{ext}'))
    os.rename(old_file_path, new_path)
    move(new_path, new_path_file)


def unpack_archive_file(old_file_path, new_name, ext, folder):
    new_path_file = Path(old_file_path.parent, folder)
    new_path_file.mkdir(exist_ok=True, parents=True)
    new_path = (Path(old_file_path.parent, f'{new_name}{ext}'))
    os.rename(old_file_path, new_path)
    unpack_archive(new_path, Path(new_path_file, new_name), ext.replace('.', ''))
    os.remove(new_path)


def normalize(old_name: str) -> str:

    new_name = old_name.translate(transliteration)
    new_name = re.sub(r'\W', '_', new_name)

    return new_name


def rename_folders(list_folders):
    for folder in list_folders[::-1]:

        new_folder_name = normalize(folder.name)

        new_path_folder = (Path(folder.parent, f'{new_folder_name}'))

        try:
            os.rename(folder, new_path_folder)
        except FileExistsError:
            new_path_folder = (Path(folder.parent, f'{new_folder_name}_1'))
            os.rename(folder, new_path_folder)


def perform():
    sorting_folder = input('Sorting folder: ')

    if not sorting_folder:
        sorting_folder = Path().cwd()

    else:
        sorting_folder = Path(sorting_folder)

    find_files(sorting_folder)
    for folder in empty_folders:
        folder.rmdir()
    rename_folders(folders_to_rename)


if __name__ == '__main__':
    perform()
    print('sorting is complete')
