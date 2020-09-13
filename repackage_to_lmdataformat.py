import os
import glob
import lm_dataformat
import tarfile
import tqdm
import sys
import shutil

def repackage(scrape_directory):
    data_file_paths = glob.glob(os.path.join(scrape_directory,"*_data.tar"))

    lm_archive = lm_dataformat.Archive(scrape_directory)

    old_directory = os.path.join(scrape_directory, "old")
    os.makedirs(old_directory)    
    for data_file_path in tqdm.tqdm(data_file_paths):
        with tarfile.open(data_file_path, "r:bz2") as tar:
            for member in tar.getmembers():
                file_reader = tar.extractfile(member)
                content = file_reader.read().decode("utf-8")
                lm_archive.add_data(content)
        new_path = os.path.join(old_directory, os.path.basename(data_file_path))
        shutil.move(data_file_path, new_path)

    lm_archive.commit() 

def test_read(file_path):
    lm_reader = lm_dataformat.Reader("")
    for text in lm_reader.read_jsonl(file_path):
        print(text)

if __name__ == '__main__':
    # scrape_directory = "E:/Eleuther_AI/webtext2/dumps/scrapes/rs_2011-02"    
    scrape_directory = sys.argv[1]
    repackage(scrape_directory)

    # file_path = "E:/Eleuther_AI/webtext2/dumps/scrapes/rs_2011-02/lm_dataformat/data_0_time1599823923_default.jsonl.zst"    
    # test_read()