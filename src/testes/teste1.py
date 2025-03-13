import numpy as np

import sys
import os
print(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))
sys.path.append(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))

import time

from classes.data_handler.read_file import Data_Handler as dh
from classes.data_structure import bucket, page
Bucket, ListaBuckets = bucket.Bucket, bucket.ListaBuckets
Page, ListaPages = page.Page, page.ListaPages

# file path
path = os.path.join(os.path.join(os.path.abspath(__name__).split("proj_banco_dados")[0], "proj_banco_dados"), "files")
print(path)
path_file = os.path.join(path, "words_alpha.txt")


dataHand = dh(path_file, 100) 


start = time.time()
pages = dataHand.get_list_page()
fim_pages = time.time() - start

# quantiadade de registros


print(f"Tepo para passar arquivos para página: {fim_pages}")
print("/"*20 + "Passar páginas para Bucket" + "/"*20)

regis = pages.regis
num_pages = pages.pointer + 1
num_buckets = num_pages * 4
tuples_per_bucket = max(1, int(np.ceil(regis / num_buckets))) 


baldes = ListaBuckets(regis, tuples_per_bucket)
start = time.time()
baldes.add_from_list(pages.list_tuples())
fim_baldes = time.time() - start

print(f"Tempo para passar paginas para balde: {fim_baldes}")

print(f"TEMPO TOTAL: {fim_baldes + fim_pages}")