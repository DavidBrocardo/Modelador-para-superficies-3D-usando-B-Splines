import math
import numpy as np

class Pintor_dist:

    def __init__(self, vertices, VRP):
        self.vertices = vertices
        self.VRP = VRP

    
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
    
    def Calcular_distancia_VRP_Face(self, VRP, centroide):

        #Formula da distancia euclidiana
        dist = math.sqrt((VRP[0] - centroide[0])**2 + (VRP[1] - centroide[1])**2 + (VRP[2] - centroide[2])**2)

        return dist

    def Calcular_dists_e_Ordenar_faces(self, vertices, VRP, indices_faces):

        face_e_distancia = [] #face e distancia dela em relação ao VRP

        for indice_face in indices_faces:
            centroide = self.Calcular_centroide_face(vertices, indice_face)
            distancia = self.Calcular_distancia_VRP_Face(VRP, centroide)
            face_e_distancia.append((distancia, indice_face))

        #Ordenar as faces pela dist, maior para menor
        Faces_ordenadas = sorted(face_e_distancia, key=lambda x: x[0], reverse=True)

        return Faces_ordenadas

    


if __name__ == "__main__":
   
    vertices = [[21.2, 34.1, 18.8, 5.9, 20],
                [0.7,  3.4,  5.6,  2.9, 20.9],
                [42.3, 27.2, 14.6, 29.7,31.6],
                [  1,   1 ,   1,     1,  1]]
    
    indices_faces = [ [0,1,4],[1,2,4],[2,3,4],[3,0,4],[0,3,2,1] ] #Os vertices de cada face, ex: Face ABE(Face 014)
        
    VRP = [25, 15, 80, 1]   

    pintor = Pintor_dist(vertices, VRP) #instancia da classe, só funfa assim

    Faces_ordenadas = pintor.Calcular_dists_e_Ordenar_faces(vertices, VRP, indices_faces)

    x = 1
    print("\nFaces ordenadas da mais distante para a mais próxima:\n") #Essa é a ordem pra ser pintada já, de tras pra frente
    for distancia, face in Faces_ordenadas:
        print(f"{x}º Face: {face} ; Distância: {distancia:.5f}")
        x = x + 1

    print("\n")