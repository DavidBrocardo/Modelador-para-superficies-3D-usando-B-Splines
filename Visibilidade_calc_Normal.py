import math
import numpy as np

class Visibilidade_Normal:

    def __init__(self, vertices, indices_faces):
        self.vertices = vertices
        self.indices_faces = indices_faces

    
    def Calcular_centroide_face(self, vertices, indice_face):

        v = len(indice_face) # Nº de vertices da face, ex: face ABE = 3; face ABCD = 4;
        
        soma_x = 0
        soma_y = 0
        soma_z = 0

        for i in indice_face:
            soma_x += vertices[0][i]
            soma_y += vertices[1][i] #vai somando os valores xyz de cada face
            soma_z += vertices[2][i]

        centroide_x = soma_x / v
        centroide_y = soma_y / v #calcula o centroide, dividindo pelo Nº de vertices
        centroide_z = soma_z / v
    
        return centroide_x, centroide_y, centroide_z
    


    def Calcular_vet_normal_unitario_face(self, vertices, indice_faces):

        p0 = vertices[:, indice_faces[0]]
        p1 = vertices[:, indice_faces[1]]  #pegando as coordenadas x,y,z de cada vertice
        p2 = vertices[:, indice_faces[2]]

        v1 = p2 - p1   #calculo dos vetores 1 e 2 para calcular o vetor normal
        v2 = p0 - p1

        Vnormal = np.cross(v1, v2)  #produto vetorial v1 x v2
  
        Vnormal_unitario = Vnormal / np.linalg.norm(Vnormal)  #calc do vetor unitario

        return Vnormal_unitario
    
    
if __name__ == "__main__":
   
    vertices = [[21.2, 34.1, 18.8, 5.9, 20],
                [0.7,  3.4,  5.6,  2.9, 20.9],
                [42.3, 27.2, 14.6, 29.7,31.6],
                [  1,   1 ,   1,     1,  1]]
    
    indices_faces = [ [0,1,4],[1,2,4],[2,3,4],[3,0,4],[0,3,2,1] ] #Os vertices de cada face, ex: Face ABE(Face 014)
        
    VRP = [25, 15, 80, 1]   


    visi = Visibilidade_Normal(vertices, indices_faces) #instancia da classe, só funfa assim

    normal_014 = visi.Calcular_vet_normal_unitario_face(vertices, indices_faces)

    