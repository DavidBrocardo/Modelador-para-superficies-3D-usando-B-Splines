class Recorte3D:
    def __init__(self, znear, zfar, vertices):
        self.znear = znear
        self.zfar = zfar
        self.vertices = self.converter_vertices(vertices)
        

    def converter_vertices(self, lista_vertices):
        vertices_covertido = [[], [], []]  
        
        for linha in lista_vertices:  
                x, y, z = linha 
                vertices_covertido[0].append(x)
                vertices_covertido[1].append(y)
                vertices_covertido[2].append(z)
        
        return vertices_covertido

    def Calcular_centroide_face(self):

        soma_z = 0
        v =0
        for i in range(len(self.vertices[0])):  
            v+= 1
            soma_z += self.vertices[2][i]  

        centroide_z = soma_z / v
    
        return  centroide_z

    def Recortar3D(self):       
        
        centroide = self.Calcular_centroide_face()         
        if self.znear <= centroide<= self.zfar:
            recortou = False
        else: 
            recortou = True   

        return recortou



