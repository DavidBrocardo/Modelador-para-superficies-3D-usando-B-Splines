import numpy as np

"""3) Transformar as superfícies com operações de rotação, translação e escala,
nas dimensões x, y e z. A escala não deve deformar as malhas; em outras
palavras, os fatores de escala devem ser os mesmos nas 3 dimensões. """

class Transformacoes_Geometricas:

    def __init__(self,vertices):
         
         self.vertices = vertices

   
    
    def Translacao(self,dx,dy,dz):

        matriz_translacao = np.array([ [1, 0, 0, dx ],   # X
                                       [0, 1, 0, dy ],   # Y
                                       [0, 0, 1, dz ],   # Z
                                       [0, 0, 0, 1  ]])  # h
        
        vertices_transladados = matriz_translacao @ self.vertices  #multiplicacao de arrays
        
        
        dados_convertidos = [[float(valor) for valor in linha] for linha in vertices_transladados] 
        return dados_convertidos
    
    
    def Escala(self, Sgeral):  #a Escala (Sgeral) deve ser a mesma nas 3 dimensões

        matriz_escala = np.array([ [Sgeral, 0, 0, 0 ],   # X
                                   [0, Sgeral, 0, 0 ],   # Y
                                   [0, 0, Sgeral, 0 ],   # Z
                                   [0,    0,   0, 1 ]])  # h])
        
        vertices_escalados = matriz_escala @ self.vertices

        
        # Convertendo para float puro do Python
        dados_convertidos = [[float(valor) for valor in linha] for linha in vertices_escalados] 
        return dados_convertidos
    
    def Rotacao_em_x(self, graus):

        radianos = np.radians(graus)  #Graus para radianos

        matriz_rotacao_x = np.array([ [1,       0,                    0,        0 ],   # X
                                      [0,  np.cos(radianos), -np.sin(radianos), 0 ],   # Y
                                      [0, np.sin(radianos), np.cos(radianos),   0 ],   # Z
                                      [0,          0,                    0,     1 ]])  # h
        
        vertices_rodados = matriz_rotacao_x @ self.vertices

        

        return vertices_rodados
    
    def Rotacao_em_y(self, graus):

        radianos = np.radians(graus)

        matriz_rotacao_y = np.array([ [np.cos(radianos),  0,  np.sin(radianos),  0 ],   # X
                                      [0,                 1,       0 ,           0 ],   # Y
                                      [-np.sin(radianos), 0, np.cos(radianos),   0 ],   # Z
                                      [      0,           0,       0,            1 ]])  # h
        
        vertices_rodados = matriz_rotacao_y @ self.vertices

        

        return vertices_rodados
    
    def Rotacao_em_z(self, graus):

        radianos = np.radians(graus)

        matriz_rotacao_z = np.array([ [np.cos(radianos),  -np.sin(radianos), 0,  0 ],   # X
                                      [np.sin(radianos),  np.cos(radianos),  0 , 0 ],   # Y
                                      [0,                      0,            1,  0 ],   # Z
                                      [0,                      0,            0,  1 ]])  # h
        
        vertices_rodados = matriz_rotacao_z @ self.vertices

        
        dados_convertidos = [[float(valor) for valor in linha] for linha in vertices_rodados] 
        return dados_convertidos
        

 