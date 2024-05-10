# python unzippy.py this.zip dictionary.txt

import zipfile
import threading
import argparse
from queue import Queue

def extract_file(zip_file_object, password, password_queue):
    try:
        zip_file_object.extractall(pwd=password.encode())
        print(f'[+] Password found: {password}\n')
        password_queue.put(password)
    except (zipfile.BadZipFile, RuntimeError):
        pass

def signal_password_found(password_queue, password):
    if password:
        password_queue.put(password)

def main(zip_file_name, dictionary_file_name):
    try:
        with zipfile.ZipFile(zip_file_name) as zip_file_object, open(dictionary_file_name) as dictionary_file_object:
            password_queue = Queue()  # Queue to signal thread to stop
            threads = []
    except FileNotFoundError as e:
        print(f'Error: {e}')
        return

    # Start threads for each password
    for line in dictionary_file_object.readlines():
        if not password_queue.empty():  # Check if password is already found
            break
        password = line.strip('\n')
        thread = threading.Thread(target=extract_file, args=(zip_file_object, password, password_queue))
        thread.daemon = True  # Set thread as daemon to avoid blocking main thread
        threads.append(thread)
        thread.start()

        # Limiting the number of concurrent threads
        if len(threads) >= 10:  # Adjust number as appropriate for your system
            threads[0].join()  # Wait for the first thread to finish
            threads.pop(0)  # Remove the first thread from the list

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crack a ZIP file password using a dictionary attack.")
    parser.add_argument("zip_file_name", help="The name of the ZIP file to crack.")
    parser.add_argument("dictionary_file_name", help="The name of the dictionary file containing potential passwords.")
    args = parser.parse_args()
    main(args.zip_file_name, args.dictionary_file_name)

