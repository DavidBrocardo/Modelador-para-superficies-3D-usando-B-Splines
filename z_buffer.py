class RasterizadorScanline:
    def __init__(self, largura, altura):
        """Inicializa o rasterizador com um Z-Buffer e os parâmetros da tela."""
        self.largura = largura
        self.altura = altura
        self.zbuffer = [[float('inf')] * altura for _ in range(largura)]  # Z-Buffer com infinito
        self.pixels = {}  # Dicionário para armazenar pixels visíveis

    def interpolar_valor(self, x1, y1, v1, x2, y2, v2, x):
        """Interpola um valor entre dois pontos."""
        if x1 == x2:
            return v1  # Evita divisão por zero
        return v1 + (v2 - v1) * (x - x1) / (x2 - x1)



    def projetar_para_viewport(self, vertices, viewport):
        """Aplica a transformação de projeção e mapeamento para a viewport."""
        u_min, v_min, u_max, v_max = viewport
        proj_vertices = []
        for i in range(len(vertices[0])):
            # Extração das coordenadas homogêneas
            x, y, z, w = vertices[0][i], vertices[1][i], vertices[2][i], vertices[3][i]
            
            # Divisão para passar para coordenadas homogêneas (perspectiva)
            x /= w
            y /= w
            z /= w
            
            # Mapeamento para a viewport 2D
            u = int((x + 1) * (u_max - u_min) / 2 + u_min)
            v = int((y + 1) * (v_max - v_min) / 2 + v_min)
            
            proj_vertices.append((u, v, z))  # Armazenamos a posição 2D e a profundidade
        return proj_vertices

    def rasterizar_poligono(self, vertices, valores_z, indices_faces, viewport):
        """Executa o algoritmo Scanline para rasterizar um polígono com Z-Buffer."""
        # Limpa buffers
        self.zbuffer = [[float('inf')] * self.altura for _ in range(self.largura)]
        self.pixels.clear()

        # Projeção dos vértices para a viewport
        vertices_projetados = self.projetar_para_viewport(vertices, viewport)

        # Rasterizar as faces
        for face in indices_faces:
            # Obtém os três vértices da face
            v1 = vertices_projetados[face[0]]
            v2 = vertices_projetados[face[1]]
            v3 = vertices_projetados[face[2]]
            
            # Chamamos a função que irá rasterizar o triângulo com Z-Buffer
            self.rasterizar_triangulo(v1, v2, v3)

    def rasterizar_triangulo(self, v1, v2, v3):
        """Rasteriza um triângulo usando o Z-Buffer."""
        # Ordena os vértices pelo eixo Y
        vertices = sorted([v1, v2, v3], key=lambda v: v[1])

        # Determina os limites do triângulo
        min_y = max(min(v[1] for v in vertices), 0)
        max_y = min(max(v[1] for v in vertices), self.altura - 1)

        # Varre cada linha horizontal (Scanline)
        for y in range(min_y, max_y + 1):
            intersecoes = []

            # Verifica interseção de scanline com as arestas do triângulo
            for i in range(3):
                (x1, y1, z1), (x2, y2, z2) = vertices[i], vertices[(i + 1) % 3]

                if y1 <= y < y2 or y2 <= y < y1:
                    # Calcula interseção no eixo X e Z para a linha scanline
                    x_int = self.interpolar_valor(y1, x1, y1, y2, x2, y)  # Interpolação de X
                    z_int = self.interpolar_valor(y1, z1, y2, z2, y)  # Interpolação de Z

                    intersecoes.append((x_int, z_int))

            # Ordena interseções pelo X
            intersecoes.sort()

            # Preenche os pixels entre os pares de interseções
            for i in range(0, len(intersecoes), 2):
                if i + 1 >= len(intersecoes):
                    continue  # Evita erro caso haja número ímpar de interseções

                x_inicio, z_inicio = intersecoes[i]
                x_fim, z_fim = intersecoes[i + 1]

                if x_inicio > x_fim:
                    x_inicio, x_fim = x_fim, x_inicio
                    z_inicio, z_fim = z_fim, z_inicio

                for x in range(x_inicio, x_fim + 1):
                    z = self.interpolar_valor(x_inicio, y, z_inicio, x_fim, y, z_fim, x)

                    # Atualiza o Z-Buffer se o novo pixel estiver mais próximo
                    if z < self.zbuffer[x][y]:
                        self.zbuffer[x][y] = z
                        self.pixels[(x, y)] = z  # Aqui poderia ser uma cor, se necessário


    def obter_pixels(self):
        """Retorna os pixels renderizados com suas profundidades."""
        return self.pixels


# Exemplo de uso da classe com os dados fornecidos
largura, altura = 400, 300
rasterizador = RasterizadorScanline(largura, altura)

# Dados fornecidos
vertices = [
    [93, 251, -22.807, 1],  # Coordenadas X
    [198, 241, -20.129, 1],  # Coordenadas Y
    [85, 192, -32.570, 1],   # Coordenadas Z
    [125, 107, -21.815, 1]   # Coordenadas W (Homogêneas)
]

viewport = [0, 0, 399, 299]  # Definição da viewport
indices_faces = [[0, 1, 3], [2, 1, 3]]  # Índices das faces

# Rasterizar os polígonos
rasterizador.rasterizar_poligono(vertices, [], indices_faces, viewport)

# Exibir os pixels gerados
pixels_resultantes = rasterizador.obter_pixels()
for (x, y), z in pixels_resultantes.items():
    print(f"Pixel: ({x}, {y}), Z: {z}")
