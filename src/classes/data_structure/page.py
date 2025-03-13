import numpy as np

class Page():
    def __init__(self, str_size: int, *, lim=5):
        self.lim: np.int64 = np.int64(lim)  # Capacidade máxima da página
        self.quant: np.int64 = np.int64(0)  # Quantidade atual de itens
        self.itens: np.ndarray = np.full(self.lim, "", dtype=f"U{str_size}")  # Inicializa com strings vazias
        
    def add_item(self, item: str) -> bool:
        if self.quant >= self.lim:
            return False
        self.itens[self.quant] = item
        self.quant += 1    
        return True
    
    def __iter__(self):
        for i in range(self.quant):
            yield self.itens[i]
    
    def __getitem__(self, index: int) -> str:
        return self.itens[index]

    def __str__(self):
        return "\n".join(f"  - {self.itens[i]}" for i in range(self.quant))


class ListaPages():
    def __init__(self, regis: int, lim: int,str_size: int = 100):
        self.lim = lim
        self.regis = regis
        self.pointer = 0
        self.num_pages = int(np.ceil(self.regis/self.lim))
        self.str_size = str_size
        self.list_pages: np.ndarray[Page] = np.array([Page(str_size, lim=lim) for _ in range(self.num_pages)], dtype=object)  # Inicia com uma página
    
    def add_item(self, item: str) -> None:
        if self.list_pages[self.pointer].add_item(item):
            return
        self.pointer += 1
        self.list_pages[self.pointer].add_item(item)
    
    
    def get_num_regis(self)->int:
        return self.regis
    
    def get_tuples(self):
        for idx, page in enumerate(self.list_pages):
            for item in page:
                yield (item, idx)
    
    def list_tuples(self):
        return np.array(list(self.get_tuples()), dtype=object)
        
        
    
    def __iter__(self):
        for page in self.list_pages:
            yield page
    
    def __getitem__(self, index: int) -> Page:
        return self.list_pages[index]
    
    def __str__(self):
        return "\n".join(f"PÁGINA {i}:\n{page}" for i, page in enumerate(self.list_pages))



if __name__ == "__main__":
    lista_paginas = ListaPages(lim=2, regis=3)
    lista_paginas.add_item("Adriano")
    lista_paginas.add_item("Marcelo")
    lista_paginas.add_item("Rodrigo")
    
    for i, tuple in enumerate(lista_paginas.list_tuples()):
        print(i, tuple)
    

        