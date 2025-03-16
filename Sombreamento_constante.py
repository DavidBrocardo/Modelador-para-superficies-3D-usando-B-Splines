import numpy as np

"""c.	Sombreamento constante
i.	Computar o valor de iluminação total (cor) de cada face

Só vai calcular das faces visiveis, calculo de visibilidade pela normal
já vai ter sido feito!

Já vai ter todas as infos calculadas tbm! evitar recalculos
(centroide da face, vetor normal da face, etc...) salvei tudo em lista de listas
"""

class Sombreamento_constante:
    def __init__(self, ila, il, ka, kd, ks, n, luz_pos, centroides, normais, vetores_s):
        self.ila = np.array(ila)  # Luz ambiente (R, G, B)
        self.il = np.array(il)    # Intensidade da lâmpada (R, G, B)
        self.ka = np.array(ka)    # Coeficiente de reflexão ambiente (R, G, B)
        self.kd = np.array(kd)    # Coeficiente de reflexão difusa (R, G, B)
        self.ks = np.array(ks)    # Coeficiente de reflexão especular (R, G, B)
        self.n = n                # Expoente especular
        self.luz_pos = np.array(luz_pos)  # Posição da luz
        self.centroides = np.array(centroides)  # Lista de centroides
        self.normais = np.array(normais)        # Lista de vetores normais
        self.vetores_s = np.array(vetores_s)    # Lista de vetores S (direção do observador)

    def Calcular_iluminacao_ambiente(self): # Iluminação ambiente [Ia = Ila . Ka]	
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
        iluminacoes.append(Itotal)

        return iluminacoes

# NAO APAGAR AINDA ESSE MAIN
if __name__ == "__main__":
    '''
    Ila = (IlaR, IlaG, IlaB)  Luz ambiente
    Il = (IlR,IlG,IlB) Luzes pontuais
    Ka = (KaR,KaG,KaB)
    Kd = (KdR,KdG,KdB) Materiais
    Ks = (KsR,KsG,KsB,n)
    '''

    ila = (120,20,30)  # Luz ambiente
    il = (150,100,20)  # Intensidade da lampada
    luz_pos = [70, 20, 35]  # Posiçao da lampada

    #Propriedades do material
    ka = (0.4,0.4,0.4)  # Coeficiente de reflexao ambiente
    kd = (0.7,0.4,0.4)  # Coeficiente de reflexao difusa
    ks = (0.5,0.4,0.4)  # Coeficiente de reflexao especular
    n = 2.15  # Expoente especular

    centroides_faces_visiveis = [
        25.100, 8.333, 33.700   # Face 1
    ]

    vetores_normais_visiveis = [0.669, 0.378, 0.639]

    vetores_s = [   # Vetor s que é o Vetor O da visibilidade lá
        -0.002, 0.143, 0.990
    ]

    #instancia da classe
    sombrear = Sombreamento_constante(ila, il, ka, kd, ks, n, luz_pos,centroides_faces_visiveis, vetores_normais_visiveis, vetores_s)

    iluminacoes = sombrear.Calcular_iluminacao_total()  #Todas as iluminaçoes para serem aplicadas em cada face estão aqui, é uma lista
    
    for i, ilum in enumerate(iluminacoes):
        print(f"Iluminação total da face {i}: {ilum}")
