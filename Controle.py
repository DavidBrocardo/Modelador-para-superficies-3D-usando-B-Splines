from Superfice_BSplines import BSplines
from Pintor_dist import Pintor_dist
from Recorte2D import Recorte2D
from Visibilidade_calc_Normal import Visibilidade_Normal
from FillPoly import FillPoly
from ProjecaoAxonometrica import ProjecaoAxonometrica
from Transformacoes_Geometricas import Transformacoes_Geometricas
from Recorte3D import Recorte3D

class Controle:
    def __init__(self):
        # Parâmetros de controle
        a = 2
        self.geometrica = 0

    def converter_vertices_tradicional(self, lista_vertices):
        vertices_covertido = [[], [], [],[]]  
        for linha in lista_vertices:  
            for item in linha: 
                x, y, z = item 
                vertices_covertido[0].append(x)
                vertices_covertido[1].append(y)
                vertices_covertido[2].append(z)
                vertices_covertido[3].append(1)
        return vertices_covertido        
    
    def converter_vertices_superfice(self, lista_vertices):
            indice = 0
            for i in range(self.RESOLUTIONI):
                linha = []
                for j in range(self.RESOLUTIONJ):
                    indice = i * self.RESOLUTIONJ + j
                    elemento = [lista_vertices[0][indice] ,
                                lista_vertices[1][indice] ,
                                lista_vertices[2][indice] ]  
                             
                    linha.append(elemento)
                self.outp.append(linha)
    
    
    def converter_pontos_superfice(self, lista_vertices,geo):
            indice = 0
            for i in range(self.NI + 1):
                linha = []
                for j in range(self.NJ + 1):
                    indice = i * (self.NJ + 1) + j
                    # projecao[0], projecao[1], projecao[2] contêm as coordenadas projetadas (desconsiderando W)
                    elemento = [lista_vertices[0][indice],
                                lista_vertices[1][indice],
                                lista_vertices[2][indice]]
                    linha.append(elemento)
                if geo:
                    self.inp.append(linha)
                self.inp_projetado.append(linha) 

    def axonometrica(self,entrada,pontos):       
        if pontos:
            vertices=[]
            vertices = self.converter_vertices_tradicional(entrada)
            projecao = ProjecaoAxonometrica(vertices, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.inp_projetado = []
            self.converter_pontos_superfice(projecao,False)   
        else:
            vertices=[]      
            vertices = self.converter_vertices_tradicional(self.outp)                   
            projecao = ProjecaoAxonometrica(vertices, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.outp = []
            self.converter_vertices_superfice(projecao)

    def transformacoes_Geometricas(self):
        # geometrica  = 0 (Nenhuma) / =1 (Escala) / = 2 (Rotacao) / = 3 (Translacao)
        if self.geometrica != 0:
            vertices=[]
            vertices = self.converter_vertices_tradicional(self.outp)
            pontos = self.converter_vertices_tradicional(self.inp)
            operacao = Transformacoes_Geometricas(vertices) 

            if self.geometrica == 1:     # ESCALA       
                resul_escala = operacao.Escala(self.valores_geo)
                self.outp = [] 
                self.converter_vertices_superfice(resul_escala)

                operacao = Transformacoes_Geometricas(pontos) 
                self.inp = []
                self.inp_projetado = []
                resul_escala = operacao.Escala(self.valores_geo)
                self.converter_pontos_superfice(resul_escala,True)
                

            if self.geometrica  == 2:    # ROTACAO
                x,y,z = self.valores_geo[0]   
                resul_rotacao_x = operacao.Rotacao_em_x(x)
                operacao = Transformacoes_Geometricas(resul_rotacao_x) 
                resul_rotacao_y = operacao.Rotacao_em_y(y)
                operacao = Transformacoes_Geometricas(resul_rotacao_y) 
                resul_rotacao_z = operacao.Rotacao_em_z(z)
                self.outp = [] 
                self.converter_vertices_superfice(resul_rotacao_z)

                operacao = Transformacoes_Geometricas(pontos)
                resul_rotacao_x = operacao.Rotacao_em_x(x)
                operacao = Transformacoes_Geometricas(resul_rotacao_x) 
                resul_rotacao_y = operacao.Rotacao_em_y(y)
                operacao = Transformacoes_Geometricas(resul_rotacao_y) 
                resul_rotacao_z = operacao.Rotacao_em_z(z)

                self.inp = []
                self.inp_projetado = []
                self.converter_pontos_superfice(resul_rotacao_z,True)
                

            if self.geometrica == 3: # TRANSLACAO
                x,y,z = self.valores_geo[0]
                resul_translacao = operacao.Translacao(x,y,z)
                self.outp = [] 
                self.converter_vertices_superfice(resul_translacao)

                operacao = Transformacoes_Geometricas(pontos) 
                self.inp = []
                self.inp_projetado = []
                resul_translacao = operacao.Translacao(x,y,z)
                self.converter_pontos_superfice(resul_translacao,True)
    
    def main(self):       
        
        # 1) Objetos modelados em SRU
        #   a.Transformações geométricas (rotações, translações, escalas, cisalhamentos, etc. aplicada ao objeto).
        self.transformacoes_Geometricas()        

        # 2) Pré-cálculos 
        #   a. Centróides de faces e de objetos
        #       i. Recorte (3D) dos objetos que estejam antes do plano Near e depois do plano Far.

        #   b. Vetores normais das faces

        #   c. Sombreamento constante
        #       i. Computar o valor de iluminação total (cor) de cada face

        #   d. Sombreamento Gouraud ou Phong:
        #       i. Vetores normais médios unitários nos vértices
        #       ii. Gouraud: Calcular a iluminação total nos vértices

        # 3) Aplicar as matrizes do pipeline (Converter objeto do SRU para o SRT)
        self.axonometrica()

        # 4) Aplicar o teste de visibilidade pelo cálculo da normal para cada face de objeto restante.
        
        #   a. Recorte 2D

        #   b. Algoritmo da scanline (Associar neste algoritmo z-buffer e o algoritmo de rasterização – Fillpoly)
        #       i. Constante: Usar o fillpoly com a cor pré-computada anteriormente;

        #       ii. Gouraud: Usar o fillpoly interpolando as cores dos vértices que foram pré-calculadas;
        
        #       iii. Phong: Usar o fillpoly interpolando os vetores normais dos vértices que foram pré-calculados e, na sequência, calcular a iluminação total (cor) em cada pixel.

        