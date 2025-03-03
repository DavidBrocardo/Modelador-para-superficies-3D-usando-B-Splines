import math
import tkinter as tk
from tkinter import Canvas
from Recorte2D import Recorte2D
from Visibilidade_calc_Normal import Visibilidade_Normal
from FillPoly import FillPoly


class Pintor_dist:
    def __init__(self, vertices, VRP, canvas,viewport):
        self.vertices = vertices  # Lista de listas de vértices
        self.VRP = VRP
        self.canvas = canvas
        self.viewport = viewport
    
    def calcular_centroide_face(self, indice_face):
        v = len(indice_face)
        soma_x = soma_y = soma_z = 0

        for i in indice_face:
            x, y = i
            #print(x , y)
            soma_x += self.vertices[x][y][0]
            soma_y += self.vertices[x][y][1]
            soma_z += self.vertices[x][y][2]

        centroide_x = soma_x / v
        centroide_y = soma_y / v
        centroide_z = soma_z / v
    
        return centroide_x, centroide_y, centroide_z
    
    def calcular_distancia_VRP_face(self, centroide):
        return math.sqrt((self.VRP[0] - centroide[0])**2 + 
                         (self.VRP[1] - centroide[1])**2 + 
                         (self.VRP[2] - centroide[2])**2)

    def calcular_dists_e_ordenar_faces(self, indices_faces):
        face_e_distancia = [(self.calcular_distancia_VRP_face(self.calcular_centroide_face(face)), face) for face in indices_faces]
        
        faces_ordenadas = sorted(face_e_distancia, key=lambda x: x[0], reverse=True)
        
        return  faces_ordenadas

    def controle(self, indices_faces):
        faces_ordenadas = self.calcular_dists_e_ordenar_faces(indices_faces)

        for _, face in faces_ordenadas:
            pontos = []
            for i in face:
                xi, yi = i
                x = self.vertices[xi][yi][0]  # Coordenada X do vértice
                y = self.vertices[xi][yi][1]  # Coordenada Y do vértice
                z = self.vertices[xi][yi][2]  # Coordenada z do vértice
                pontos.append((x, y, z))
            #print(pontos)
            visi = Visibilidade_Normal(pontos,[[0,1,2,3]],self.VRP[:-1] ,True) #instancia da classe, so funfa assim
            produtos_escalares = visi.main()
            #print(produtos_escalares)
            if produtos_escalares[0] >= 0: 
                color = "Green"
            else:
                color = "Red"

            recorte = Recorte2D(self.viewport, pontos)
            poligono_recortado = recorte.Recortar_total()
            FillPoly(poligono_recortado,self.canvas,"white")
            if len(poligono_recortado) != 0:
                x1, y1, z1 = poligono_recortado[0]
                cond = True
                for i in reversed(poligono_recortado):
                    if cond :
                        x2, y2, z2 = i
                        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
                        cond  = False
                    else:
                        x1, y1, z1 = i
                        self.canvas.create_line(x2, y2, x1, y1, fill=color, width=1)
                        x2 = x1
                        y2 = y1

        
        return

        

if __name__ == "__main__":
    vertices = [
        [21.2, 0.7, 42.3],
        [34.1, 3.4, 27.2],
        [18.8, 5.6, 14.6],
        [5.9, 2.9, 29.7],
        [20, 20.9, 31.6]
    ]
    
    indices_faces = [[0,1,4], [1,2,4], [2,3,4], [3,0,4], [0,3,2,1]]
    VRP = [25, 15, 80]    

    pintor = Pintor_dist(vertices, VRP)
    pintor.controle(indices_faces)
