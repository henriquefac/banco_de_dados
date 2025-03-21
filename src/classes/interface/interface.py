import numpy as np
import time

import sys
import os

sys.path.append(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))

from classes.data_structure.bucket import Bucket, ListaBuckets
from classes.data_structure.page import Page, ListaPages
from classes.data_handler.read_file import Data_Handler as dh

class Interface():
    def __init__(self, path, rpp):
        self.dataHandler = dh(path=path, rpp=rpp)
        self.listPages = None  # Atrasar a carga para otimizar desempenho
        self.buckets = None  # Armazena os buckets após a primeira chamada
    
    # Paginar os dados (lazy loading)
    def get_pages(self) -> ListaPages:
        if self.listPages is None:
            self.listPages = self.dataHandler.get_list_page()
        return self.listPages
    
    # Criar e armazenar lista de buckets
    def get_buckets(self) -> ListaBuckets:
        if self.buckets is not None:
            return self.buckets  # Retorna os buckets armazenados
        
        regis = self.get_pages().regis
        tuples_per_bucket = self.get_tuple_per_bucket()
        self.buckets = ListaBuckets(regis, tuples_per_bucket)
        
        # adicionar tuplas para bucket
        self.buckets.add_from_list(self.listPages.list_tuples())
        
        return self.buckets
    
    # Calcular número de tuplas por bucket
    def get_tuple_per_bucket(self, safe_factor=4) -> int:
        num_pages = self.get_pages().num_pages  # Evita divisão por zero
        num_buckets = num_pages * safe_factor
        tuples_per_bucket = max(1, int(np.ceil(self.get_pages().regis / num_buckets)))  # Garante pelo menos 1 tupla por bucket
        
        return tuples_per_bucket

    
    def init_interface(self):
        start = time.time()
        self.get_pages()
        fim_page = time.time() - start
        
        print(f"Tempo para passar o arquivo para página: {fim_page}")
        
        start = time.time()
        self.get_buckets()
        fim_bucket = time.time() - start
        
        print(f"Tempo para passar tuplas da pagina para bucket: {fim_bucket}")

# implementar comandos como table scan
# busca por bucket

# Apresentar taxa de colizão
# Apresentar taxa de overflow


class InterfaceComands(Interface):
    def __init__(self, path, rpp):
        super().__init__(path, rpp)
        self.init_interface()
        self.last_table_search_cost = None
        self.last_hash_consult_cost = None
        
    def table_scan(self, key):
        count = 0
        for i, page in enumerate(self.listPages):
            count += 1
            for item in page:
                if item == key:
                    self.last_table_search_cost = count 
                    return (item, i)
                
        self.last_table_search_cost = count
        return None
    
    def get_page_by_key(self, key):
        idx = self.buckets.search(key)
        if idx is None:
            return None
        
        self.last_hash_consult_cost = 0
        pages = [self.listPages[idx]]
        for page in pages:
            self.last_hash_consult_cost += 1    
            for item in page:
                if item == key:
                    return (item, idx)
        return None
        
    def colison_rate(self):
        return (self.buckets.colision_num / self.listPages.get_num_regis())

    def overflow_rate(self):
        return (self.buckets.overflow_num / self.buckets.qunt)

    def compared_search_method(self, key):
        start = time.time()
        result_hash = self.get_page_by_key(key)
        time_hash = time.time() - start
        
        start = time.time()
        restul_table_scan = self.table_scan(key)
        time_table_scan = time.time() - start   
        
        print(f"Busca por hash: {result_hash}, Tempo: {time_hash:.6f} s, Acessos: {self.last_hash_consult_cost}")
        print(f"Table scan: {restul_table_scan}, Tempo: {time_table_scan:.6f} s, Acessos: {self.last_table_search_cost}")
        print(f"Taxa de colisão: {self.colison_rate():.2%}")
        print(f"Taxa de overflow: {self.overflow_rate():.2%}")

if __name__ == "__main__":
    interface = InterfaceComands(r"/home/henrique/Documents/pyProjects/proj_banco_dados/words_alpha.txt", 3)
    
    interface.compared_search_method("acetazolamide")
    
    
#    handler = dh(r"/home/henrique/Documents/pyProjects/proj_banco_dados/words_alpha.txt", 2)
#    lista_pages = handler.get_list_page()
#    print(lista_pages)
#    
#    buckets = ListaBuckets(lista_pages.get_num_regis(), 3)
#    
#    for idx, page in enumerate(lista_pages):
#        for item in page:
#            buckets.add_item((item, idx))
#            
#    print(buckets)