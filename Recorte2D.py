import numpy as np

## Basicamente são as mesmas estruturas nos recortes, só muda as fórmulas!!


class Recorte2D:

    def __init__(self, viewport, vertices):
        self.viewport = viewport

        #Converte a matriz de vertices para uma lista de listas, mais facil
        self.vertices = [[vertices[0][i], vertices[1][i], vertices[2][i]] 
                         for i in range(len(vertices[0]))] #tem q te, gpt

    def Recortar_esquerda(self):
        
        xmin = self.viewport[0]
        novo_poligono = []
        num_vertices = len(self.vertices)

        for i in range(num_vertices):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % num_vertices]

            if p1[0] < xmin and p2[0] >= xmin:  #Adentrando a area de recorte

                u = (xmin - p1[0]) / (p2[0] - p1[0])
                y = p1[1] + u * (p2[1] - p1[1])
                z = p1[2] + u * (p2[2] - p1[2])
                
                novo_vertice = [xmin, y, z]
                novo_poligono.append(novo_vertice)  #Intersecao
                novo_poligono.append(p2)  #Vertice interno

            elif p1[0] >= xmin and p2[0] >= xmin:  #Ambos dentro
                novo_poligono.append(p2) #vertice interno

            elif p1[0] >= xmin and p2[0] < xmin:  #Saindo da area de recorte

                u = (xmin - p1[0]) / (p2[0] - p1[0])
                y = p1[1] + u * (p2[1] - p1[1])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [xmin, y, z]
                novo_poligono.append(novo_vertice) #Apenas a intersecao

        return novo_poligono
    
    def Recortar_direita(self,saida_rec_esquerda):
        
        xmax = self.viewport[1]
        novo_poligono = []
        num_vertices = len(saida_rec_esquerda)

        for i in range(num_vertices):
            p1 = saida_rec_esquerda[i]
            p2 = saida_rec_esquerda[(i + 1) % num_vertices]

            if p1[0] > xmax and p2[0] <= xmax:  #Adentrando a area de recorte

                u = (xmax - p1[0]) / (p2[0] - p1[0])
                y = p1[1] + u * (p2[1] - p1[1])
                z = p1[2] + u * (p2[2] - p1[2])
                
                novo_vertice = [xmax, y, z]
                novo_poligono.append(novo_vertice)  #Intersecao
                novo_poligono.append(p2)  #Vertice interno

            elif p1[0] <= xmax and p2[0] <= xmax:  #Ambos dentro
                novo_poligono.append(p2) #vertice interno

            elif p1[0] <= xmax and p2[0] > xmax:  #Saindo da area de recorte

                u = (xmax - p1[0]) / (p2[0] - p1[0])
                y = p1[1] + u * (p2[1] - p1[1])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [xmax, y, z]
                novo_poligono.append(novo_vertice)  #Apenas a intersecao

        return novo_poligono
    
    def Recortar_Embaixo(self,saida_rec_direita):

        ymax = self.viewport[3]
        novo_poligono = []
        num_vertices = len(saida_rec_direita)

        for i in range(num_vertices):
            p1 = saida_rec_direita[i]
            p2 = saida_rec_direita[(i + 1) % num_vertices]

            if p1[1] > ymax and p2[1] <= ymax:  #Adentrando a area de recorte

                u = (ymax - p1[1]) / (p2[1] - p1[1])
                x = p1[0] + u * (p2[0] - p1[0])
                z = p1[2] + u * (p2[2] - p1[2])
                
                novo_vertice = [x, ymax, z]
                novo_poligono.append(novo_vertice)  #Intersecao
                novo_poligono.append(p2)  #Vertice interno

            elif p1[1] <= ymax and p2[1] <= ymax:  #Ambos dentro
                novo_poligono.append(p2) #vertice interno

            elif p1[1] <= ymax and p2[1] > ymax:  #Saindo da area de recorte

                u = (ymax - p1[1]) / (p2[1] - p1[1])
                x = p1[0] + u * (p2[0] - p1[0])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [x, ymax, z]
                novo_poligono.append(novo_vertice)  #Apenas a intersecao

        return novo_poligono


    def Recortar_topo(self,saida_rec_embaixo):
        
        ymin = self.viewport[2]
        novo_poligono = []
        num_vertices = len(saida_rec_embaixo)
        
        for i in range(num_vertices):
            p1 = saida_rec_embaixo[i]
            p2 = saida_rec_embaixo[(i + 1) % num_vertices]

            if p1[1] < ymin and p2[1] >= ymin:  #Adentrando a area de recorte

                u = (ymin - p1[1]) / (p2[1] - p1[1])
                x = p1[0] + u * (p2[0] - p1[0])
                z = p1[2] + u * (p2[2] - p1[2])
                
                novo_vertice = [x, ymin, z]
                novo_poligono.append(novo_vertice)  #Intersecao
                novo_poligono.append(p2)  #Vertice interno

            elif p1[1] >= ymin and p2[1] >= ymin:  #Ambos dentro
                novo_poligono.append(p2) #vertice interno

            elif p1[1] >= ymin and p2[1] < ymin:  #Saindo da area de recorte

                u = (ymin - p1[1]) / (p2[1] - p1[1])
                x = p1[0] + u * (p2[0] - p1[0])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [x, ymin, z]
                novo_poligono.append(novo_vertice)  #Apenas a intersecao

        return novo_poligono


if __name__ == "__main__":
    vertices = [[  0,  250, 480],  # X
                [250,  430,   0],  # Y
                [-30,  -65, -90]]  # Z
                                   # Tirei o fator homogeneo, mas qlqr coisa adicionar de boa

    viewport = [100, 400, 80, 380]  # umin, umax, vmin, vmax

    recorte = Recorte2D(viewport, vertices)
    poligono_recortado = recorte.Recortar_esquerda()
    poligono_recortado2 = recorte.Recortar_direita(poligono_recortado)
    poligono_recortado3 = recorte.Recortar_Embaixo(poligono_recortado2)
    poligono_recortado4 = recorte.Recortar_topo(poligono_recortado3)
   
    print("Polígono final recorte esquerda:", poligono_recortado)
    print("\n Polígono final recorte direita:", poligono_recortado2)
    print("\n Polígono final recorte embaixo:", poligono_recortado3)
    print("\n Polígono final recorte topo:", poligono_recortado4)
