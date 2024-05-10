# python unzippy.py this.zip dictionary.txt

import zipfile
import threading
import argparse
from queue import Queue

def extract_file(zFile, password, found):
    try:
        zFile.extractall(pwd=password.encode())
        print(f'[+] Password found: {password}\n')
        found.put(password)  # Signal that the password was found
    except:
        pass

def main(zip_file_name, dictionary_file_name):
    zFile = zipfile.ZipFile(zip_file_name)
    passFile = open(dictionary_file_name)
    found = Queue()  # Queue to signal thread to stop
    threads = []

    # Start threads for each password
    for line in passFile.readlines():
        if not found.empty():  # Check if password is already found
            break
        password = line.strip('\n')
        thread = threading.Thread(target=extract_file, args=(zFile, password, found))
        threads.append(thread)
        thread.start()

        # Limiting the number of concurrent threads
        if len(threads) >= 10:  # Adjust number as appropriate for your system
            threads[0].join()  # Wait for the first thread to finish
            threads.pop(0)  # Remove the first thread from the list

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    passFile.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crack a ZIP file password using a dictionary attack.")
    parser.add_argument("zip_file_name", help="The name of the ZIP file to crack.")
    parser.add_argument("dictionary_file_name", help="The name of the dictionary file containing potential passwords.")
    args = parser.parse_args()
    main(args.zip_file_name, args.dictionary_file_name)

