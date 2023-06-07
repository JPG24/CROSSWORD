import numpy as np
import timeit
import pickle as pkl
from progress.bar import Bar, ChargingBar

from classesA import Mapa


def importarParaules(path, lengths, timer=False) -> dict:
    t0 = timeit.default_timer()
    
    with open(path, "r") as file:
        paraules = file.read().split('\n')
        paraules = paraules
        print(len(paraules))
        diccionari = {}
        bar1 = Bar("Important", max=len(paraules))
        for paraula in paraules:
            if len(paraula) not in diccionari.keys() and len(paraula) in lengths:
                diccionari[len(paraula)] = np.array([])
            try:
                diccionari[len(paraula)] = np.append(diccionari[len(paraula)], paraula)
            except:
                pass
            bar1.next()
        bar1.finish()
        
    if timer: print(f"Temps per importar {path}: {timeit.default_timer() - t0}")
    return diccionari

def txtToPkl(path, lengths):
    with open(path, "wb") as file:
        pkl.dump(importarParaules(path, lengths), file)
        
def importPickle(path):
    with open(path, "rb") as file:
        dictionary = pkl.load(path)
    return dictionary
    

def importarMapa(path) -> list:
    mapa = np.array([[]])
    with open(path, 'r') as file:
        for line in file.read().split('\n'):
            if mapa.size == 0:
                mapa = np.array([line.split('\t')])
            else: mapa = np.vstack((mapa, np.array([line.split('\t')])))
    return mapa

def main():
    
    timer = True
    
    A = False
    CB = True

    if A:
        print("A:")
        mapa_A = importarMapa('crossword_A.txt')
        mapa = Mapa(mapa_A)
        mapa.generaCaselles(timer=timer)
        paraules_A = importarParaules('diccionari_A.txt', mapa.getLengths(), timer=timer)
        mapa.forwardChecking(paraules_A, timer=timer)
        print("Mapa final de A:")
        mapa.printMapa()
        
    if CB:
        print("CB:")
        mapa_CB = importarMapa('crossword_CB_v3.txt')
        mapa = Mapa(mapa_CB)
        mapa.generaCaselles(timer=timer)
        paraules_CB = importarParaules("diccionari_CB_v3.txt", mapa.getLengths(), timer=timer)
        mapa.forwardChecking(paraules_CB, timer=timer)
        print("Mapa final de CB:")
        mapa.printMapa()
     

if __name__ == "__main__":
    main()
