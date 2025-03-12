
import sys
import os

sys.path.append("/home/henrique/Documents/pyProjects/proj_banco_dados/src/classes")

from  data_structure.page import ListaPages



class Data_Handler():
    def __init__(self, path: str, rpp: int):
        self.path = path
        self.rpp = rpp
        
    def get_data_to_page(self, page: ListaPages):
        with open(self.path, "r") as file:
            lines = (file.read()).split("\n")
            for line in lines[:10000]:
                page.add_item(line)
                
    def get_list_page(self)->ListaPages:
        listPages = ListaPages(self.rpp, str_size=60)
        self.get_data_to_page(listPages)
        return listPages
        