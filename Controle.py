from Superfice_BSplines import BSplines
from Pintor_dist import Pintor_dist
from Recorte2D import Recorte2D
from Visibilidade_calc_Normal import Visibilidade_Normal
from FillPoly import FillPoly
from ProjecaoAxonometrica import ProjecaoAxonometrica
from Transformacoes_Geometricas import Transformacoes_Geometricas
from Recorte3D import Recorte3D

class Controle:
    def __init__(self, tela, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, VRP, P, Y, dp, windows, viewport,geometrica,valores_geo):
                
        # Parâmetros de controle
        self.tela = tela
        self.pontos_controleX= pontos_controleX
        self.pontos_controleY= pontos_controleY
        self.TI= TI
        self.TJ= TJ
        self.RESOLUTIONI= RESOLUTIONI
        self.RESOLUTIONJ= RESOLUTIONJ
        self.VRP = VRP
        self.P = P
        self.Y = Y
        self.dp = dp
        self.windows = windows
        self.viewport = viewport
        self.geometrica = geometrica
        self.valores_geo = valores_geo

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
            #vertices = self.converter_vertices_tradicional(entrada)
            projecao = ProjecaoAxonometrica(vertices, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.inp_projetado = []
            self.converter_pontos_superfice(projecao,False)   
        else:
            vertices=[]      
            #vertices = self.converter_vertices_tradicional(self.outp)                   
            projecao = ProjecaoAxonometrica(vertices, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.outp = []
            self.converter_vertices_superfice(projecao)

    def transformacoes_Geometricas(self,vertices,pontos):
        # geometrica  = 0 (Nenhuma) / =1 (Escala) / = 2 (Rotacao) / = 3 (Translacao)
                
        operacao = Transformacoes_Geometricas(vertices) 

        if self.geometrica == 1:     # ESCALA       
            resul_escala_superfice = operacao.Escala(self.valores_geo)

            operacao = Transformacoes_Geometricas(pontos) 

            resul_escala_pontos = operacao.Escala(self.valores_geo)

            #self.converter_pontos_superfice(resul_escala,True)
            return resul_escala_superfice, resul_escala_pontos

        if self.geometrica  == 2:    # ROTACAO
            x,y,z = self.valores_geo[0]   
            resul_rotacao_x = operacao.Rotacao_em_x(x)
            operacao = Transformacoes_Geometricas(resul_rotacao_x) 
            resul_rotacao_y = operacao.Rotacao_em_y(y)
            operacao = Transformacoes_Geometricas(resul_rotacao_y) 
            resul_rotacao_z_superfice = operacao.Rotacao_em_z(z)


            operacao = Transformacoes_Geometricas(pontos)
            resul_rotacao_x = operacao.Rotacao_em_x(x)
            operacao = Transformacoes_Geometricas(resul_rotacao_x) 
            resul_rotacao_y = operacao.Rotacao_em_y(y)
            operacao = Transformacoes_Geometricas(resul_rotacao_y) 
            resul_rotacao_z_pontos = operacao.Rotacao_em_z(z)

            return resul_rotacao_z_superfice, resul_rotacao_z_pontos

        if self.geometrica == 3: # TRANSLACAO
            x,y,z = self.valores_geo[0]
            resul_translacao_superfice = operacao.Translacao(x,y,z)

            operacao = Transformacoes_Geometricas(pontos) 
            resul_translacao_pontos = operacao.Translacao(x,y,z)

            return resul_translacao_superfice, resul_translacao_pontos
    def vetores_Normais(self):

        for superfice in range(self.quantidadeSuperfice):
                    faces = []
                    for i in range(self.RESOLUTIONI[superfice] - 1):
                        for j in range(self.RESOLUTIONJ[superfice] - 1):
                            faces.append([(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)])

                            visi = Visibilidade_Normal(pontos,[[0,1,2,3]],self.VRP[:-1] ,True) #instancia da classe, so funfa assim
                            produtos_escalares = visi.main()
                            #print(produtos_escalares)
                            if produtos_escalares[0] >= 0: 
                                color = "Green"
                            else:
                                color = "Red"
        
    def main(self):       

        #CRIAR A SUPERFICE 
        # Calcula a superfície B-Spline
        bspline = BSplines(self.pontos_controleX, self.pontos_controleY ,self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                           self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0)
        self.pontos_SRU,  self.Superfice_SRU = bspline.main()
        
        #TRANSFORMANDO EM FORMATO Padrao de Matriz 
        #[x,y,z]       [x, x, x],
        #[x,y,z]  -->  [y, y, y],
        #[x,y,z]       [z, z, z] 

        matriz_superfice=[]
        matriz_pontos=[]
        matriz_superfice = self.converter_vertices_tradicional(self.pontos_SRU)
        matriz_pontos = self.converter_vertices_tradicional(self.Superfice_SRU)
        
        # 1) Objetos modelados em SRU
        #   a.Transformações geométricas (rotações, translações, escalas, cisalhamentos, etc. aplicada ao objeto).
        if self.geometrica != 0:
            matriz_superfice , matriz_pontos = self.transformacoes_Geometricas(matriz_superfice,matriz_pontos)        

        # 2) Pré-cálculos 
        #   a. Centróides de faces e de objetos
        #       i. Recorte (3D) dos objetos que estejam antes do plano Near e depois do plano Far.
        recorte = Recorte3D(0, 600, matriz_superfice)
        matriz_superfice = recorte.Recortar3D()  
        recorte = Recorte3D(0, 600, matriz_pontos)
        matriz_pontos = recorte.Recortar3D()  

        #   b. Vetores normais das faces
        self.vetores_Normais(matriz_superfice,matriz_pontos)
        
        #   c. Sombreamento constante
        #       i. Computar o valor de iluminação total (cor) de cada face

        #   d. Sombreamento Gouraud ou Phong:
        #       i. Vetores normais médios unitários nos vértices
        #       ii. Gouraud: Calcular a iluminação total nos vértices

        # 3) Aplicar as matrizes do pipeline (Converter objeto do SRU para o SRT)
            #PONTOS
        self.axonometrica(self.inp,True)          
            #SUPERFICE
        self.axonometrica(self.outp,False)    

        # 4) Aplicar o teste de visibilidade pelo cálculo da normal para cada face de objeto restante.
        
        #   a. Recorte 2D

        #   b. Algoritmo da scanline (Associar neste algoritmo z-buffer e o algoritmo de rasterização – Fillpoly)
        #       i. Constante: Usar o fillpoly com a cor pré-computada anteriormente;

        #       ii. Gouraud: Usar o fillpoly interpolando as cores dos vértices que foram pré-calculadas;
        
        #       iii. Phong: Usar o fillpoly interpolando os vetores normais dos vértices que foram pré-calculados e, na sequência, calcular a iluminação total (cor) em cada pixel.

        