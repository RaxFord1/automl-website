import logging
import os
import traceback
import zipfile

# import rarfile


def extract_and_delete_rar(rar_file_path, extract_path):
    raise Exception("Not implemented")
    # try:
    #     os.makedirs(extract_path, exist_ok=True)
    #
    #     with rarfile.RarFile(rar_file_path) as rar:
    #         rar.extractall(path=extract_path)
    #     logging.log(f"RAR Files extracted to {extract_path}")
    #
    #     os.remove(rar_file_path)
    #     logging.log(f"RAR file {rar_file_path} has been deleted.")
    # # except Exception as e:
    #     traceback.print_exception(e)
    #     logging.log(logging.ERROR, f"RAR An error occurred: {e}")


def extract_and_delete_zip(zip_file_path, extract_path):
    try:
        os.makedirs(extract_path, exist_ok=True)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        logging.log(logging.INFO, f"ZIP Files extracted to {extract_path}")

        os.remove(zip_file_path)
        logging.log(logging.INFO, f"ZIP file {zip_file_path} has been deleted.")
    except Exception as e:
        traceback.print_stack()
        logging.log(logging.ERROR, f"ZIP An error occurred: {e}")
