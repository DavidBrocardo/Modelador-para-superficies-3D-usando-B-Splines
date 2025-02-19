import math
import numpy as np

class Recorte2D:

    def __init__(self, viewport, vertices):
        
        self.viewport = viewport
        self.vertices = vertices

    def Recortar_poligono (self, viewport, vertices):

        #Recortar_esquerda()
        #Recortar_direita()
        #Recortar_baxo()
        #Recortar_cima()
        return 0

    def Recortar_esquerda(self, viewport, vertices):

        xmin = viewport[0]
        novo_poligono = []

        for i in range(len(self.vertices)):

            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]

            if p1 < xmin and p2 >= xmin:  #Adentrando a area de recorte 
                x = xmin
                u = (x - p1[0]) / (p2[0] - p1[0])
                y = (p1[1] + u) * (p2[1] - p1[1])
                z = (p1[2] + u) * (p2[2] - p1[2])

                novo_vertice = [x,y,z] 

                novo_poligono.append(novo_vertice)
                novo_poligono.append(p2)

            if p1 >= xmin and p2 >= xmin:  #Ambos dentro da area de recorte

                novo_poligono.append(p2)

            if p1 >= xmin and p2 < xmin:  #Saindo da area de recorte
                x = xmin
                u = (x - p1[0]) / (p2[0] - p1[0])
                y = (p1[1] + u) * (p2[1] - p1[1])
                z = (p1[2] + u) * (p2[2] - p1[2])

                novo_vertice = [x,y,z] 

                novo_poligono.append(novo_vertice)

            return novo_poligono


    
if __name__ == "__main__":

              #   A    B     C
    vertices = [[ 0,  250, 18.8 ],
                [250, 430,  0   ],
                [-30, -65, -90  ],
                [  1,   1,   1  ]]  
    
    arestas = [[1],[2],[0]]  # A-> B, B ->C, C -> A
    
    viewport = [100, 400, 80, 380] #umin, umax, vmin, vmax
  

    recorte = Recorte2D(viewport, vertices) #instancia da classe, só funfa assim

 