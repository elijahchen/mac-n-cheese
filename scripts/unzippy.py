# python unzippy.py this.zip dictionary.txt

import zipfile
import threading
import argparse
from queue import Queue

def extract_file(zFile, password):
    try:
        zFile.extractall(pwd=password.encode())
        print(f'[+] Password found: {password}\n')
        return password
    except (zipfile.BadZipFile, RuntimeError) as e:
        print(f'[-] Error extracting file: {e}')
        return None

def signal_password_found(password_queue, password):
    if password:
        password_queue.put(password)

def main(zip_file_name, dictionary_file_name):
    with zipfile.ZipFile(zip_file_name) as zFile, open(dictionary_file_name) as passFile:
        password_queue = Queue()  # Queue to signal thread to stop
    threads = []

    # Start threads for each password
    for line in passFile.readlines():
        if not found.empty():  # Check if password is already found
            break
        password = line.strip('\n')
        thread = threading.Thread(target=extract_file, args=(zFile, password))
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

        password = extract_file(zFile, password)
        signal_password_found(password_queue, password)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crack a ZIP file password using a dictionary attack.")
    parser.add_argument("zip_file_name", help="The name of the ZIP file to crack.")
    parser.add_argument("dictionary_file_name", help="The name of the dictionary file containing potential passwords.")
    args = parser.parse_args()
    main(args.zip_file_name, args.dictionary_file_name)

