import numpy as np

"""c.	Sombreamento constante
i.	Computar o valor de iluminação total (cor) de cada face

Só vai calcular das faces visiveis, calculo de visibilidade pela normal
já vai ter sido feito!

Já vai ter todas as infos calculadas tbm! evitar recalculos
(centroide da face, vetor normal da face, etc...) salvei tudo em lista de listas
"""

class Sombreamento_constante:
    def __init__(self, ila, il, ka, kd, ks, n, luz_pos, centroides, normais, vetores_s, visibilidade):
        self.ila = np.array(ila)  #Luz ambiente (R, G, B)
        self.il = np.array(il)    #Intensidade da lâmpada (R, G, B)
        self.ka = np.array(ka)    #Coeficiente de reflexão ambiente (R, G, B)
        self.kd = np.array(kd)    #Coeficiente de reflexão difusa (R, G, B)
        self.ks = np.array(ks)    #Coeficiente de reflexão especular (R, G, B)
        self.n = n                #Expoente especular
        self.luz_pos = np.array(luz_pos)  #Posição da luz
        self.centroides = np.array(centroides)  #Lista de centroides
        self.normais = np.array(normais)        #Lista de vetores normais
        self.vetores_s = np.array(vetores_s)    #Lista de vetores S (direção do observador)
        self.visibilidade = visibilidade

    def Calcular_iluminacao_ambiente(self): #Iluminação ambiente [Ia = Ila . Ka]	
        return self.ila * self.ka

    def Calcular_iluminacao_difusa(self, i): #Iluminação difusa [Id = Il . Kd . (n.l)]	

        vetor_L = self.luz_pos - self.centroides  # Vetor L = (luz - centroide da face)
        vetor_L /= np.linalg.norm(vetor_L)  # Vetor L normalizado
        n_dot_l = max(np.dot(self.normais, vetor_L), 0)  #Produto escalar (n . l)

        return self.il * self.kd * n_dot_l

    def Calcular_iluminacao_especular(self, i):  #Iluminação especular [Is = Il . Ks . (r.s)^n]
      
        vetor_L = self.luz_pos - self.centroides   # Vetor L
        vetor_L /= np.linalg.norm(vetor_L)  # Vetor L normalizado

        # Vetor R = 2(n . l) * n - l
        n_dot_l = np.dot(self.normais, vetor_L)
        vetor_R = 2 * n_dot_l * self.normais - vetor_L
        vetor_R /= np.linalg.norm(vetor_R)  # Vetor R normalizado

        #Produto escalar (r . s)
        r_dot_s = max(np.dot(vetor_R, self.vetores_s), 0)

        return self.il * self.ks * (r_dot_s ** self.n)

    def Calcular_iluminacao_total(self): #Iluminação total [It = Ia + Id + Is]		

        iluminacoes = []
        Ia = self.Calcular_iluminacao_ambiente()

        
        Id = self.Calcular_iluminacao_difusa(self.centroides)
        Is = self.Calcular_iluminacao_especular(self.centroides)
        
        Itotal = Ia + Id + Is        
        if (self.visibilidade[0] < 0):
            Itotal = Ia 
        iluminacoes.append(Itotal)
        return iluminacoes


