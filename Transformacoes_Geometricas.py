import numpy as np

"""3) Transformar as superfícies com operações de rotação, translação e escala,
nas dimensões x, y e z. A escala não deve deformar as malhas; em outras
palavras, os fatores de escala devem ser os mesmos nas 3 dimensões. """

class Transformacoes_Geometricas:

    def __init__(self,vertices):
         #self.vertices = np.array(vertices)  #convertendo pra array desde o inicio para as mult de matriz
         self.vertices = vertices

   
    
    def Translacao(self,dx,dy,dz):

        matriz_translacao = np.array([ [1, 0, 0, dx ],   # X
                                       [0, 1, 0, dy ],   # Y
                                       [0, 0, 1, dz ],   # Z
                                       [0, 0, 0, 1  ]])  # h
        
        vertices_transladados = matriz_translacao @ self.vertices  #multiplicacao de arrays
        
        #self.vertices = matriz_translacao @ self.vertices --> caso querer salvar a cada operação!!!
        dados_convertidos = [[float(valor) for valor in linha] for linha in vertices_transladados] 
        return dados_convertidos
    
    
    def Escala(self, Sgeral):  #a Escala (Sgeral) deve ser a mesma nas 3 dimensões

        matriz_escala = np.array([ [Sgeral, 0, 0, 0 ],   # X
                                   [0, Sgeral, 0, 0 ],   # Y
                                   [0, 0, Sgeral, 0 ],   # Z
                                   [0,    0,   0, 1 ]])  # h])
        
        vertices_escalados = matriz_escala @ self.vertices

        #self.vertices = matriz_escala @ self.vertices --> caso querer salvar a cada operação!!!
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

        #self.vertices = matriz_rotacao_x @ self.vertices --> caso querer salvar a cada operação!!!

        return vertices_rodados
    
    def Rotacao_em_y(self, graus):

        radianos = np.radians(graus)

        matriz_rotacao_y = np.array([ [np.cos(radianos),  0,  np.sin(radianos),  0 ],   # X
                                      [0,                 1,       0 ,           0 ],   # Y
                                      [-np.sin(radianos), 0, np.cos(radianos),   0 ],   # Z
                                      [      0,           0,       0,            1 ]])  # h
        
        vertices_rodados = matriz_rotacao_y @ self.vertices

        #self.vertices = matriz_rotacao_y @ self.vertices --> caso querer salvar a cada operação!!!

        return vertices_rodados
    
    def Rotacao_em_z(self, graus):

        radianos = np.radians(graus)

        matriz_rotacao_z = np.array([ [np.cos(radianos),  -np.sin(radianos), 0,  0 ],   # X
                                      [np.sin(radianos),  np.cos(radianos),  0 , 0 ],   # Y
                                      [0,                      0,            1,  0 ],   # Z
                                      [0,                      0,            0,  1 ]])  # h
        
        vertices_rodados = matriz_rotacao_z @ self.vertices

        #self.vertices = matriz_rotacao_z @ self.vertices --> caso querer salvar a cada operação!!!
        dados_convertidos = [[float(valor) for valor in linha] for linha in vertices_rodados] 
        return dados_convertidos
        

if __name__ == "__main__":
    
    vertices = [
    [-5, 0, 4, -1],   # X
    [-2, -1, 0, 6],   # Y
    [-3, 3, -4, 0],   # Z
    [1, 1, 1, 1] ]     # H
    vertices = [(187.36430672822868, 281.52216239265516, 20.03723291849055), 
     (176.61584716852576, 286.1471108623356, 23.99474823671324), 
     (191.62004198536994, 300.2942413294096, 27.343859742189753), 
     (202.36850154507283, 296.02688528938364, 23.28520201120323)]

    operacao = Transformacoes_Geometricas(vertices)   #instancia da classe

    resul_translacao = operacao.Translacao(5,2,3)
    resul_escala = operacao.Escala(4)
    resul_rotacao_x = operacao.Rotacao_em_x(-30)
    resul_rotacao_y = operacao.Rotacao_em_y(40)
    resul_rotacao_z = operacao.Rotacao_em_z(50)


    print (resul_translacao)
    print("\n")
    print (resul_escala)
    print("\n")
    print (resul_rotacao_x)
    print("\n")
    print(resul_rotacao_y)
    print("\n")
    print(resul_rotacao_z)
 