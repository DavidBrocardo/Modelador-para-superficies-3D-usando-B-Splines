class Recorte3D:
    def __init__(self, znear, zfar, vertices):
        self.znear = znear
        self.zfar = zfar
        self.vertices = vertices

    def Recortar3D(self):
        
        nova_matriz = [[], [], [],[]]
        for i in range(len(self.vertices[0])):  
            x = self.vertices[0][i]  
            y = self.vertices[1][i]
            z = self.vertices[2][i]  
            #o poligono ta dentro do volume visivel ou nao
            if self.znear <= z <= self.zfar:
                nova_matriz[0].append(x)
                nova_matriz[1].append(y)
                nova_matriz[2].append(z)  #mantido
                nova_matriz[3].append(1)
        

        return nova_matriz


if __name__ == "__main__":
    vertices = [[  0,  250, 480],  # X
                [250,  430,   0],  # Y
                [30,  -65,  510]]  # Z
    
    znear = -100   #perto d+ da camera, tampa ela inteira, por isso deve ser recortado 
    zfar = 600   #longe d+ da camera, só gasta processamento e nem da pra direito

    recorte = Recorte3D(znear, zfar, vertices)
    vertices_visiveis = recorte.Recortar3D()

    print("Vértices após o recorte:", vertices_visiveis)


##
##   Ver com o professor se o nosso z do que é visivel é negativo???
##