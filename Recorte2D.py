import numpy as np

## Basicamente são as mesmas estruturas nos recortes, só muda as fórmulas!!


class Recorte2D:

    def __init__(self, viewport, vertices):
        self.viewport = viewport
        #self.vertices = vertices
        #Converte a matriz de vertices para uma lista de listas, mais facil
        self.vertices = vertices
        """for i in range(len(vertices[0])):
            print(i)
            self.vertices = [[vertices[0][i], vertices[1][i]]]"""
        #print("\n Antes : ", self.vertices)

    def Recortar_esquerda(self):
       #[u_min, v_min, u_max, v_max]
        xmin = self.viewport[1]
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
                novo_poligono.append(novo_vertice)  # Sala a Intersecao
                novo_poligono.append(p2)  #e o vertice interno

            elif p1[0] >= xmin and p2[0] >= xmin:  #Ambos dentro
                novo_poligono.append(p2) #Salvar apenas o vertice interno

            elif p1[0] >= xmin and p2[0] < xmin:  #Saindo da area de recorte

                u = (xmin - p1[0]) / (p2[0] - p1[0])
                y = p1[1] + u * (p2[1] - p1[1])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [xmin, y, z]
                novo_poligono.append(novo_vertice) #Salvar apenas a intersecao

        return novo_poligono
    
    def Recortar_direita(self,saida_rec_esquerda):
        #[u_min, v_min, u_max, v_max]
        xmax = self.viewport[3]
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
                novo_poligono.append(p2)  

            elif p1[0] <= xmax and p2[0] <= xmax:  #Ambos dentro
                novo_poligono.append(p2) 

            elif p1[0] <= xmax and p2[0] > xmax:  #Saindo da area de recorte

                u = (xmax - p1[0]) / (p2[0] - p1[0])
                y = p1[1] + u * (p2[1] - p1[1])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [xmax, y, z]
                novo_poligono.append(novo_vertice)  
        return novo_poligono
    
    def Recortar_embaixo(self,saida_rec_direita):
        #[u_min, v_min, u_max, v_max]
        ymax = self.viewport[2]
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
                novo_poligono.append(p2) 

            elif p1[1] <= ymax and p2[1] <= ymax:  #Ambos dentro
                novo_poligono.append(p2) 

            elif p1[1] <= ymax and p2[1] > ymax:  #Saindo da area de recorte

                u = (ymax - p1[1]) / (p2[1] - p1[1])
                x = p1[0] + u * (p2[0] - p1[0])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [x, ymax, z]
                novo_poligono.append(novo_vertice)

        return novo_poligono


    def Recortar_topo(self,saida_rec_embaixo):
         #[u_min, v_min, u_max, v_max]
        ymin = self.viewport[0]
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
                novo_poligono.append(p2) 

            elif p1[1] >= ymin and p2[1] >= ymin:  #Ambos dentro
                novo_poligono.append(p2) 

            elif p1[1] >= ymin and p2[1] < ymin:  #Saindo da area de recorte

                u = (ymin - p1[1]) / (p2[1] - p1[1])
                x = p1[0] + u * (p2[0] - p1[0])
                z = p1[2] + u * (p2[2] - p1[2])

                novo_vertice = [x, ymin, z]
                novo_poligono.append(novo_vertice)

        return novo_poligono

    def converter_vertices(self, lista_vertices):
        vertices_covertido = [[], [], []]  
        for linha in lista_vertices:      
            #print("\n\n" ,linha) 
            x, y,z= linha 
            vertices_covertido[0].append(x)
            vertices_covertido[1].append(y)
            #vertices_covertido[2].append(z)
                
        return vertices_covertido

    #chama todos os recortes e executa o recorte total
    def Recortar_total(self): 
        resul1 = self.Recortar_esquerda()
        resul2 = self.Recortar_direita(resul1)
        resul3 = self.Recortar_embaixo(resul2)
        resul4 = self.Recortar_topo(resul3)
        #print("\n RECORTE: " ,resul4)
        recortado  = self.converter_vertices(resul4)

        return resul4

        
if __name__ == "__main__":
    vertices = [[  0,  250, 480 , 100 ,200 ,50],  # X
                [250,  430,   0 , 20 , 100, 25],  # Y
                [-30,  -65, -90, -20 ,50 , 0]]   # Z
                                    # Tirei o fator homogeneo, mas qlqr coisa adicionar de boa (da peido se add kkk)

    viewport = [0, 0, 500, 500]  #[u_min, v_min, u_max, v_max]

    recorte = Recorte2D(viewport, vertices)
    poligono_recortado = recorte.Recortar_total()
   
    print("Polígono final Recortado:", poligono_recortado)
