import numpy as np

import sys
import os

sys.path.append(os.path.join(os.path.abspath(__name__).split("src")[0], "src"))


# criar um bucket

# armazena uma lista de tuplas
# e um ponteiro para outro bucket quando ocorrer um overflow
class Bucket():
    def __init__(self, lim: np.uint64):
        self.lim = lim
        self.qunt = 0
        # lista de tuplas
        self.tuple_list: np.ndarray[tuple[str, int]] = np.empty(self.lim, dtype=object)
        # ponteiro para bucket após overflow
        self.next: 'Bucket' = None
    
    def add_tuple(self, item: tuple)->bool:
        if self.full():
            return self.overflow(item)
            
        self.tuple_list[self.qunt] = item
        self.qunt+=1
        return False
    
    def full(self):
        return self.qunt >= self.lim
    
    def overflow(self, item: tuple) -> bool:
        if self.next is None:
            self.next = Bucket(self.lim)
            self.next.add_tuple(item)  # Adiciona o item no novo bucket
            return True  # Indica que houve overflow
    
        return self.next.add_tuple(item)  # Continua o encadeamento
    
    def search(self, key: str)->int:
        for i in range(self.qunt):
            k, index = self.tuple_list[i]
            if k == key:
                return index
        return self.next.search(key) if self.next else None
    
    def __str__(self):
        itens = [f"{k} {i}" for k, i in self.tuple_list[:self.qunt]]
        result = f"Bucket: [{', '.join(itens)}]"
        if self.next:
            result+= " Overflow -> " + str(self.next)
        return result
# lista de Buckets

# a lista vai ser responsável por receber uma tuple e aplicar a função hash
# logo depois direciona para o bucket correto


def base_hash(key: str, num_buckets: int, prime: int = 31):
    hash_value = 0
    for i, char in enumerate(key):
        hash_value += (ord(char) * (prime ** i))  # Soma ponderada
    return hash_value % num_buckets  # Limita ao número de buckets


class ListaBuckets():
    def __init__(self, quant, lim=5, hash_function = base_hash):
        """Quantidade de items, Número máximo de tuplas por bukcet, função hash usada"""
        # recebe quantidade de items e limite de cada bucket
        self.qunt: int = int(np.ceil(quant / lim)) # arredonda para cima
        # limite de tuplas por bucket
        self.lim = lim
        # lista de buckets
        self.list_bucket: np.ndarray[Bucket] =  np.array([Bucket(lim) for _ in range(self.qunt)], dtype=object)
        self.hash_function = hash_function
        
        self.overflow_num = 0
        self.colision_num = 0
        
    def add_item(self, item: tuple):
        key, _ = item
        index = self.hash_function(key, self.qunt)
        
        if self.list_bucket[index].full():
            self.colision_num += 1
            
        if self.list_bucket[index].add_tuple(item):
            self.overflow_num += 1
            
    def add_from_list(self, array: np.ndarray):
        hashList = array[:, 0]
        func = np.vectorize(lambda x: self.hash_function(str(x), self.qunt))
        hashList = func(hashList)
        
        for i, tuple in enumerate(array):
            index = hashList[i]
            
            if self.list_bucket[index].full():
                self.colision_num += 1
            
            if self.list_bucket[index].add_tuple((str(tuple[0]), tuple[1])):
                self.overflow_num += 1
        
    def search(self, key: str)->int:
        index = self.hash_function(key, self.qunt)
        return self.list_bucket[index].search(key)
    
    def __str__(self):
        return "\n".join(f"Bucket {i}: {self.list_bucket[i]}" for i in range(self.qunt))
        
# funções hash

if __name__ == "__main__":
    lista = ListaBuckets(quant=5, lim=2)
    
    # Adiciona elementos
    lista.add_item(("Alice", 20))
    lista.add_item(("Bob", 30))
    lista.add_item(("Charlie", 40))
    lista.add_item(("Daniel", 50))
    lista.add_item(("Henrique", 10))

    # Testa a busca
    print(lista.search("Alice"))   # 20
    print(lista.search("Bob"))     # 30
    print(lista.search("Charlie")) # 40
    print(lista.search("Daniel"))  # None (não existe)
    
    print(lista)
    print(lista.__dict__)