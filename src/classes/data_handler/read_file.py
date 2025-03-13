
import sys
import os

sys.path.append(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))

from  classes.data_structure.page import ListaPages



class Data_Handler():
    def __init__(self, path: str, rpp: int):
        self.path = path
        self.rpp = rpp
        self.lines = []
        
    def get_data(self):
        with open(self.path, "r") as file:
            self.lines = (file.read()).split("\n")
            
                
    def get_list_page(self)->ListaPages:
        self.get_data()
        listPages = ListaPages(len(self.lines), self.rpp, str_size=60)
        
        for line in self.lines:
            listPages.add_item(line) 
            
        return listPages
        