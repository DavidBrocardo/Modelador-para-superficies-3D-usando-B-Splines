import numpy as np

class Visibilidade_Normal:

    def __init__(self, vertices, indices_faces,VRP, pintor):
        if pintor:
            self.vertices = self.converter_vertices(vertices)
            
        else:
            self.vertices = vertices
        self.indices_faces = indices_faces
        self.VRP = VRP
    
    
    def converter_vertices(self, lista_vertices):
        vertices_covertido = [[], [], []]  
        for linha in lista_vertices:  
                x, y, z = linha 
                vertices_covertido[0].append(x)
                vertices_covertido[1].append(y)
                vertices_covertido[2].append(z)
        print(vertices_covertido)
        return vertices_covertido
    
    def Calcular_vet_normal_unitario_face(self, vertices, indice_face): #calcula de uma face

        vertices = np.array(vertices) #s├│ funfa convertendo pra array pra manipular

        p0 = vertices[:3, indice_face[0]]
        p1 = vertices[:3, indice_face[1]] #pegando os vertices da face e seus x,y,z
        p2 = vertices[:3, indice_face[2]]

        v1 = p1 - p0 
        v2 = p2 - p0  #vets 1 e 2 para calcular o vet normal

        Vnormal = np.cross(v1, v2)  #produto vetorial v1 x v2
  
        norma = np.linalg.norm(Vnormal)
        Vnormal_unitario = Vnormal / norma  #calc do vet unitario

        return Vnormal_unitario
    
    def Calcular_vet_normal_das_faces(self, vertices, indices_faces): #calcula de todas as faces armazenadas

        normais_faces = []
       
        #print("\n")
        for i, face in enumerate(indices_faces): 
            
            normal_unitaria = self.Calcular_vet_normal_unitario_face(vertices, face)
            normais_faces.append(normal_unitaria)  #calculando e salvando todos os vets normais das faces

            #print(f"Normal da face {i}: {normal_unitaria}")
        #print("\n")

        return normais_faces

    def Calcular_centroide_face(self, vertices, indice_face):

        v = len(indice_face) # Nº de vertices da face, ex: face ABE = 3; face ABCD = 4;
        
        soma_x = 0
        soma_y = 0
        soma_z = 0

        for i in indice_face:
            print(vertices[0])
            print(i)
            print(vertices[0][i])
            soma_x += vertices[0][i]
            soma_y += vertices[1][i] #vai somando os valores xyz de cada face
            soma_z += vertices[2][i]

        centroide_x = soma_x / v
        centroide_y = soma_y / v #calcula o centroide, dividindo pelo Nº de vertices
        centroide_z = soma_z / v
    
        return centroide_x, centroide_y, centroide_z
    
    def Calcular_vet_observacao_face (self, VRP, vertices, indices_faces):

        VRP = np.array(VRP) 
        vets_de_observacao_faces = []
        
        for indice_face in indices_faces:
            centroide = self.Calcular_centroide_face(vertices, indice_face) 
            vet_observacao = VRP - centroide  

            norma = np.linalg.norm(vet_observacao)  #calc do vet de observacao unitario
            VetorO_unitario = vet_observacao / norma 

            vets_de_observacao_faces.append(VetorO_unitario) 
           
        return vets_de_observacao_faces

    def main(self):

        vets_normais = self.Calcular_vet_normal_das_faces(self.vertices, self.indices_faces)
        vets_observacao = self.Calcular_vet_observacao_face(self.VRP, self.vertices, self.indices_faces)
        produtos_escalares = [np.dot(vn, vo) for vn, vo in zip(vets_normais, vets_observacao)] #gpt cantou
        return produtos_escalares
if __name__ == "__main__":
   
    vertices = [[21.2, 34.1, 18.8],
                [0.7,  3.4,  5.6],
                [42.3, 27.2, 14.6]]
    vertices =  [(176.61584716852576, 302.4606292819998, 19.380588436890747), 
                (161.61165235168156, 302.09376893358626, 26.83487647345148),
                (176.6158471685257, 303.9757883716631, 33.65308525117195),
                (191.62004198536994, 302.0991495773967, 26.83335459756128)]
    indices_faces = [ [0,1,2,3]] #Os vertices de cada face, ex: Face ABE(Face 014)

    VRP = [25, 15, 80]   

    visi = Visibilidade_Normal(vertices, indices_faces,VRP ,True) #instancia da classe, so funfa assim
    produtos_escalares = visi.main()

    #print(np.array(vets_observacao))  #printa como uma matriz numpy (mais facil assim)

    print("\n")

    for i, produto in enumerate(produtos_escalares):
        if produto >= 0:
            print(f"Produto escalar da face {i}: {produto:.3f} --> A face é Visível!")
        else:
            print(f"Produto escalar da face {i}: {produto:.3f} --> A face não é visível!")

    print("\n")