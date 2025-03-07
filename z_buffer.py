import numpy as np  

class Zbuffer:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura  = altura
        #matriz com tamanho largura x altura da tela
        self.profundidadeZ = np.full((largura, altura), float('inf')) #inicializando profundidade com infinito

    # De cada pixel da tela:
    def testar_e_atualizar_profundidade(self, x,y,z): 
        if 0 <= x < self.largura and 0 <= y < self.altura:
            if z < self.profundidadeZ[y, x]:  #Z menor, mais perto
                self.profundidadeZ[y, x] = z
                return True  #Desenha o pixel
        return False  #Nao atualiza o pixel
    


    ##Explicações para chamar no sombreamento e no Fill Poly:

    # -Sombreamento: 
    '''color = calcular_iluminacao() - davisao calculou valor do sombreamento
       if testar_e_atualizar_profundidade(x, y, z):  - se for true ele sombreia
          canvas[y, x] = color  '''
    # -Fill Poly: (essa explicacao GPT kkk)
    '''for y in range(y_x):
        for x in range(x1, xmin, y_ma2):  # Supondo que x1 e x2 foram calculados para essa linha
            z = interpolar_z(x, y, vertices, z_values)  # Interpola a profundidade
            if zbuffer.testar_e_atualizar_profundidade(x, y, z):  # Verifica o Z-Buffer
                canvas[y, x] = color  # Desenha o pixel'''
