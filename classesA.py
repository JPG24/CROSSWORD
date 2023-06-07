import numpy as np
import timeit
import copy

'''
Classe que conte les diferents paraules del tauler
    @_mida (int): número de caselles que té
    @_paraula (string): paraula que cumpleix les restriccions
    @_caselles (list de tuples): coordenades que té la paraula
    @_creuades (list de list): caselles creuades [posició creuada, paraula creuada, posició paraula creuada]
'''
class Casella:
    def __init__(self, mida = 0, caselles = np.array([])) -> None:
        self._mida = mida
        self._paraula = ""
        self._caselles = caselles
        self._creuades = []

    def printCaselles(self) -> None:
        print(self._mida)
        print(self._paraula)
        print(self._caselles)
        print(self._creuades)

'''
Classe que conte el crossword
    @_mapa (matrix de chars): crossword 
    @_domini (list de Caselles): possibles posicions per introduir paraules
    @_solucio (bool): si el crossword està resolt
'''
class Mapa:
    def __init__(self, mapa) -> None:
        self._mapa = mapa
        self._domini = np.array([])
        self._solucio = False

    def toMapa(self) -> None:
        if self._solucio:
            for espai in self._domini:
                for i, casella in enumerate(espai._caselles):
                    self._mapa[casella[0], casella[1]] = espai._paraula[i]

    def printMapa(self) -> None:
        self.toMapa()
        for linia in self._mapa:
            print(linia)

    def getLengths(self) -> list:
        l = []
        for p in self._domini:
            l.append(p._mida)
        return list(set(l))
            
            

    ''' 
    Comprova donada una casella si es una intersecció
        @i (int): coord fila
        @j (int): coord columna

        @return si és una casella creuada
    '''
    def validaCreuades(self, i , j) -> bool:        
        if i == 0:
            if j == 0:
                if self._mapa[i][j + 1] == '0' and self._mapa[i + 1][j] == '0':
                    return True
            elif j == len(self._mapa[0]) - 1:
                if self._mapa[i][j - 1] == '0' and self._mapa[i + 1][j] == '0':
                    return True
            elif (self._mapa[i][j + 1] == '0' or self._mapa[i][j - 1] == '0') and self._mapa[i + 1][j] == '0':
                    return True
            else: return False     
        elif i == len(self._mapa) - 1:
            if j == 0:
                if self._mapa[i][j + 1] == '0' and self._mapa[i - 1][j] == '0':
                    return True
            elif j == len(self._mapa[0]) - 1:
                if self._mapa[i][j - 1] == '0' and self._mapa[i - 1][j] == '0':
                    return True
            elif (self._mapa[i][j + 1] == '0' or self._mapa[i][j - 1]) == '0' and self._mapa[i - 1][j] == '0':
                    return True
            else: return False     
        elif j == 0:
            if i == 0:
                if self._mapa[i][j + 1] == '0' and self._mapa[i + 1][j] == '0':
                    return True
            elif i == len(self._mapa) - 1:
                if self._mapa[i][j + 1] == '0' and self._mapa[i - 1][j] == '0':
                    return True
            elif self._mapa[i][j + 1] == '0' and (self._mapa[i + 1][j] == '0' or self._mapa[i - 1][j] == '0'):
                    return True
            else: return False     
        elif j == len(self._mapa[0]) - 1:
            if i == 0:
                if self._mapa[i][j - 1] == '0' and self._mapa[i + 1][j] == '0':
                    return True
            elif i == len(self._mapa) - 1:
                if self._mapa[i][j - 1] == '0' and self._mapa[i - 1][j] == '0':
                    return True
            elif self._mapa[i][j - 1] == '0' and (self._mapa[i + 1][j] == '0' or self._mapa[i - 1][j] == '0'):
                    return True
            else: return False
        
        elif (self._mapa[i][j + 1] == '0' or self._mapa[i][j - 1] == '0') and (self._mapa[i + 1][j] == '0' or self._mapa[i - 1][j] == '0'):
            return True
        
        else:
            return False

    '''
    Selecciona totes les caselles que són '0' i en crea els respectius dominis amb la limitació d'espai
    Busca quines són les caselles creuades de cada paraula i ho guarda amb la estructura (posició dins de la paraula, l'altre paraula, posició altre paraula)
    '''
    def generaCaselles(self, timer=False) -> None:
        
        t0 = timeit.default_timer()
        
        for i, j in np.ndindex(self._mapa.shape):
            if self._mapa[i][j] == '0':

                #INICI VERTICAL
                if i == 0 or self._mapa[i - 1][j] == '#':
                    n = i
                    mida = 0
                    caselles = []
                    while n < len(self._mapa):
                        if self._mapa[n][j] == '#':
                            break
                        caselles.append((n,j))
                        mida += 1
                        n += 1
                    if mida > 1:
                        self._domini = np.append(self._domini, Casella(mida, caselles))

                #INICI HORITZONTAL
                if j == 0 or self._mapa[i][j - 1] == '#':
                    m = j
                    mida = 0
                    caselles = []
                    while (m < len(self._mapa[i]) and self._mapa[i][m] != '#'):
                        caselles.append((i,m))
                        mida += 1
                        m += 1
                    if mida > 1:
                        self._domini = np.append(self._domini, Casella(mida, caselles))
                        
                #CREUADA
                if self.validaCreuades(i, j) == True:
                    # localitzem les paraules que es creuen
                    paraules_creuades = []
                    for k, espai in enumerate(self._domini): # probar np.ndenumearte si da tiempo
                        if (i, j) in espai._caselles:
                            paraules_creuades.append((k, espai._caselles.index((i, j))))
                    # afagim les variables a cada paraula 
                    self._domini[paraules_creuades[0][0]]._creuades.append((paraules_creuades[0][1], paraules_creuades[1][0], paraules_creuades[1][1]))
                    self._domini[paraules_creuades[1][0]]._creuades.append((paraules_creuades[1][1], paraules_creuades[0][0], paraules_creuades[0][1]))
        
        if timer: print(f"Temps per crear mapa: {timeit.default_timer() - t0}") 
                        
    '''
    Utilitza BACKTRACKING per resoldre el crossword a través d'un llistat de paraules
        @paraules (list de string): diccionari de paraules per completra el crossword (variables)
        @utilitzades (list de string): paraules que ja s'estan utilitzant en el crossword

        @return si ha trobat una solució amb les paraules donades
    '''      
    def backTracking(self, paraules, utilitzades = []) -> bool:
        
        if len(utilitzades) == len(self._domini):
            # Està resolt
            self._solucio = True
            return True

        if not paraules:
            # No hi ha solució
            return False
        
        for espai in self._domini: 
            if espai._paraula == "": 
                for i, paraula in enumerate(paraules[espai._mida]):
                    
                    # comprovem que no s'incompleixin les restriccions 
                    valida = True
                    for creuada in espai._creuades: 
                        if self._domini[creuada[1]]._paraula != "":
                            if self._domini[creuada[1]]._paraula[creuada[2]] != paraula[creuada[0]]:
                                valida = False
                                break
                            
                    # si es compleixen les restriccions afagim la paraula i utilitzem la recursivitat
                    if valida:
                        espai._paraula = paraula
                        utilitzades.append(paraula)
                        paraules[espai._mida] = np.delete(paraules[espai._mida], i)
                        if self.backTracking(paraules, utilitzades):
                            return True
                         
                        else:
                            # si no ha trobat solució retornem tot a l'estat original
                            espai._paraula = ""
                            paraules[espai._mida] = np.insert(paraules[espai._mida], i, utilitzades[-1])
                            utilitzades.pop(-1)
                            
                return False

    '''
    Crea la matriu que utilitzarem per comprobar les restriccions
        @paraules (dict de arrays): diccionari de paraules per completar el crossword (variables)
    '''
    def matriuForwardChecking(self, paraules) -> None: 
        self._matriuFC = np.empty(len(self._domini),dtype=object)
        for x in range(len(self._domini)):
                self._matriuFC[x] = copy.deepcopy(paraules[self._domini[x]._mida])


    
    '''
    Comprova que es compleixin les restriccions pel FORWARDCHECKING en totes les paraules que es creuen
        @paraules (dict de arrays): diccionari de paraules per completar el crossword (variables)
        
        @return si encara hi ha solucions possibles
    '''
    def actualitzarDomini(self, paraules, rowsDone) -> bool:
        self.matriuForwardChecking(paraules)
        
        # busquem quines són les paraules que es creuen amb les que tenim posades
        creuades = []
        for espai in self._domini:
            if espai._paraula != "":
                for creuada in espai._creuades:
                    creuades.append((creuada[1], creuada[2], espai._paraula[creuada[0]]))
                    
        list(set(creuades))
        
        # eliminem les paraules que no compleixin les restriccions
        for creuada in creuades:
            deleted = []
            for i, paraula in enumerate(self._matriuFC[creuada[0]]):
                if paraula[creuada[1]] != creuada[2]:
                    deleted.append(i)
            self._matriuFC[creuada[0]] = np.delete(self._matriuFC[creuada[0]], deleted) 
                    
        # comprovem si hi ha alguna fila buida
        for i, fila in enumerate(self._matriuFC):
            if np.size(fila) == 0 and i > rowsDone:
                return False
        
        return True
                    
    
    def forwardChecking(self, paraules, utilitzades=[], first=True, timer=False) -> bool:
        
        if first:
            t0 = timeit.default_timer()
            self.matriuForwardChecking(paraules)
        
        if len(utilitzades) == len(self._domini):
            # Està resolt
            self._solucio = True
            return True

        if not paraules:
            # No hi ha solució
            if first and timer: print(f"Temps per fer forwardChecking: {timeit.default_timer() - t0}")
            return False
        
        for x, espai in enumerate(self._domini): 
            if espai._paraula == "": 
                for i, paraula in enumerate(self._matriuFC[x]):

                    espai._paraula = paraula
                    utilitzades.append(paraula)
                    where = np.where(paraules[espai._mida] == paraula)
                    paraules[espai._mida] = np.delete(paraules[espai._mida], where[0])
                    
                    # actualitzem el domini i comprovem si podem seguir
                    if self.actualitzarDomini(paraules, x):
                        if self.forwardChecking(paraules, utilitzades, False):
                            if first and timer: print(f"Temps per fer forwardChecking: {timeit.default_timer() - t0}")
                            return True
                        
                    # si no ha trobat solució retornem tot a l'estat original
                    espai._paraula = ""
                    paraules[espai._mida] = np.insert(paraules[espai._mida], where[0], utilitzades[-1])
                    utilitzades.pop(-1)
                
                if first and timer: print(f"Temps per fer forwardChecking: {timeit.default_timer() - t0}")             
                return False
    