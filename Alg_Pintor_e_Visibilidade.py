import math
import numpy as np

class PintoreVisibilidade:

    def __init__(self, vertices, VRP):
        self.vertices = vertices
        self.VRP = VRP

    
    def calcular_centroide_face(self, vertices, indice_face):

        v = len(indice_face) # Nº de vertices da face, ex: face ABE = 3; face ABCD = 4;
        
        soma_x = 0
        soma_y = 0
        soma_z = 0

        for i in indice_face:
           
            soma_x += vertices[0][i]
            soma_y += vertices[1][i] #vai somando os valores xyz de cada face
            soma_z += vertices[2][i]

        centroide_x = soma_x / v
        centroide_y = soma_y / v #finalmente calcula o centroide, dividindo pelo Nº de vertices
        centroide_z = soma_z / v
    
        return centroide_x, centroide_y, centroide_z


if __name__ == "__main__":
   
    vertices = [[21.2, 34.1, 18.8, 5.9, 20],
                [0.7,  3.4,  5.6,  2.9, 20.9],
                [42.3, 27.2, 14.6, 29.7,31.6],
                [  1,   1 ,   1,     1,  1]]
    
    indice_face = [0,1,4]  #Os vertices de cada face, ex: Face ABE(Face 014)
        
    VRP = [25, 15, 80, 1]   

    pintor = PintoreVisibilidade(vertices, VRP) #instancia da classe, só funfa assim

    centroide = pintor.calcular_centroide_face(vertices, indice_face)
    print(f"Centroide da face: {centroide}") 
