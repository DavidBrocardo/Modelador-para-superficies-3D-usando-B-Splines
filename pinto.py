import math
import tkinter as tk
from tkinter import Canvas

class Pintor_dist:

    def __init__(self, vertices, VRP):
        self.vertices = vertices
        self.VRP = VRP
        
    def Calcular_centroide_face(self, indice_face):
        v = len(indice_face)
        soma_x = soma_y = soma_z = 0

        for i in indice_face:
            x, y = i
            print(x , y)
            soma_x += self.vertices[0][i]
            soma_y += self.vertices[1][i]
            soma_z += self.vertices[2][i]

        centroide_x = soma_x / v
        centroide_y = soma_y / v
        centroide_z = soma_z / v
    
        return centroide_x, centroide_y, centroide_z
    
    def Calcular_distancia_VRP_Face(self, centroide):
        return math.sqrt((self.VRP[0] - centroide[0])**2 + (self.VRP[1] - centroide[1])**2 + (self.VRP[2] - centroide[2])**2)

    def Calcular_dists_e_Ordenar_faces(self, indices_faces):
        face_e_distancia = [(self.Calcular_distancia_VRP_Face(self.Calcular_centroide_face(face)), face) for face in indices_faces]
        
        Faces_ordenadas = sorted(face_e_distancia, key=lambda x: x[0], reverse=True)
        
        matriz_reorganizada = [[[self.vertices[i][j] for j in face] for i in range(len(self.vertices))] for _, face in Faces_ordenadas]
        
        return Faces_ordenadas, matriz_reorganizada

  
        

if __name__ == "__main__":
    vertices = [[21.2, 34.1, 18.8, 5.9, 20],
                [0.7,  3.4,  5.6,  2.9, 20.9],
                [42.3, 27.2, 14.6, 29.7, 31.6],
                [1, 1, 1, 1, 1]]
    
    indices_faces = [[0,1,4], [1,2,4], [2,3,4], [3,0,4], [0,3,2,1]]
    VRP = [25, 15, 80, 1]   

    pintor = Pintor_dist(vertices, VRP)
    Faces_ordenadas, matriz_reorganizada = pintor.Calcular_dists_e_Ordenar_faces(indices_faces)
    root = tk.Tk()
    root.title("Desenho das Faces")
    canvas = Canvas(root, width=500, height=500, bg="white")
    canvas.pack()
    for _, face in Faces_ordenadas:
        pontos = [(vertices[0][i] , vertices[1][i] ) for i in face]
        canvas.create_polygon(pontos, outline="black", fill="gray", width=2)
    root.mainloop()
    print("\nMatriz reorganizada de acordo com as faces ordenadas:")
    for face in matriz_reorganizada:
        print(face)
    

