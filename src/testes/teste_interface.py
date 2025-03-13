import numpy as np

import sys
import os
print(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))
sys.path.append(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))

import time

from classes.interface.interface import InterfaceComands
from classes.data_handler.read_file import Data_Handler as dh
from classes.data_structure import bucket, page
Bucket, ListaBuckets = bucket.Bucket, bucket.ListaBuckets
Page, ListaPages = page.Page, page.ListaPages


path = os.path.join(os.path.join(os.path.abspath(__name__).split("proj_banco_dados")[0], "proj_banco_dados"), "files")
path_file = os.path.join(path, "words_alpha.txt")

interface = InterfaceComands(path_file, 34)