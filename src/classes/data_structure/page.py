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
    def __init__(self, lim: int = 5, str_size: int = 100    ):
        self.lim = lim
        self.num_pages = 1
        self.str_size = str_size
        self.list_pages: list[Page] = [Page(str_size, lim=lim)]  # Inicia com uma página
    
    def add_item(self, item: str) -> None:
        for page in self.list_pages:
            if page.add_item(item):
                return
        # Se não conseguiu adicionar, cria nova página
        self.num_pages += 1
        new_page = Page(self.str_size, lim=self.lim)
        new_page.add_item(item)
        self.list_pages.append(new_page)
    
    def get_num_regis(self)->int:
        return self.lim * (len(self.list_pages)-1) + self.list_pages[-1].quant
    
    def get_tuples(self):
        for idx, page in enumerate(self.list_pages):
            for item in page:
                yield (item, idx)
    
    def __iter__(self):
        for page in self.list_pages:
            yield page
    
    def __getitem__(self, index: int) -> Page:
        return self.list_pages[index]
    
    def __str__(self):
        return "\n".join(f"PÁGINA {i}:\n{page}" for i, page in enumerate(self.list_pages))



if __name__ == "__main__":
    lista_paginas = ListaPages(lim=2)
    lista_paginas.add_item("Adriano")
    lista_paginas.add_item("Marcelo")
    lista_paginas.add_item("Rodrigo")
    

        