import yaml
import subprocess
from pprint import pprint
import os
cwd = os.getcwd()
dir_path = os.path.dirname(os.path.realpath(__file__))

def compile_book(path, file):
    print(path, file)
    subprocess.run(["bash", dir_path + "/compile.sh", path, file])
    

with open(r'publish.yml') as file:
    documents = yaml.full_load(file)
    for book in documents['books']:
        compile_book(book['basepath'], book['export_file'])