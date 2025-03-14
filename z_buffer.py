import numpy as np
import matplotlib.pyplot as plt

# Definições do tamanho da tela
width, height = 200, 200
framebuffer = np.zeros((height, width, 3), dtype=np.uint8)  # Imagem RGB
zbuffer = np.full((height, width), np.inf)  # Inicializa com infinito

# Função para rasterizar uma linha
def draw_scanline(y, x1, z1, x2, z2, color):
    if x1 > x2:
        x1, x2, z1, z2 = x2, x1, z2, z1
    
    dz = (z2 - z1) / (x2 - x1) if x2 != x1 else 0
    z = z1
    
    for x in range(int(x1), int(x2) + 1):
        if 0 <= x < width and 0 <= y < height and z < zbuffer[y, x]:
            zbuffer[y, x] = z
            framebuffer[y, x] = color
        z += dz

class Sombreamento_constante:
    def __init__(self, ila, il, ka, kd, ks, n, luz_pos, centroides, normais, vetores_s):
        self.ila = np.array(ila)  # Luz ambiente (R, G, B)
        self.il = np.array(il)    # Intensidade da lâmpada (R, G, B)
        self.ka = np.array(ka)    # Coeficiente de reflexão ambiente (R, G, B)
        self.kd = np.array(kd)    # Coeficiente de reflexão difusa (R, G, B)
        self.ks = np.array(ks)    # Coeficiente de reflexão especular (R, G, B)
        self.n = n                # Expoente especular
        self.luz_pos = np.array(luz_pos)  # Posição da luz
        self.centroides = np.array(centroides)  # Lista de centroides
        self.normais = np.array(normais)        # Lista de vetores normais
        self.vetores_s = np.array(vetores_s)    # Lista de vetores S (direção do observador)

    def Calcular_iluminacao_ambiente(self):  # Iluminação ambiente [Ia = Ila . Ka]
        return self.ila * self.ka

    def Calcular_iluminacao_difusa(self):  # Iluminação difusa [Id = Il . Kd . (n.l)]
        vetor_L = self.luz_pos - self.centroides  # Vetor L = (luz - centroide da face)
        vetor_L = np.squeeze(vetor_L)  # Remover qualquer dimensão extra e garantir que seja 1D
        vetor_L /= np.linalg.norm(vetor_L)  # Vetor L normalizado

        # Certifique-se de que `self.normais` seja um vetor 1D
        norm = np.squeeze(self.normais)  # Remover dimensões extras, se necessário

        n_dot_l = max(np.dot(norm, vetor_L), 0)  # Produto escalar (n . l)

        return self.il * self.kd * n_dot_l

    def Calcular_iluminacao_especular(self):  # Iluminação especular [Is = Il . Ks . (r.s)^n]
        vetor_L = self.luz_pos - self.centroides   # Vetor L
        vetor_L = np.squeeze(vetor_L)  # Remover qualquer dimensão extra para garantir que seja 1D
        vetor_L /= np.linalg.norm(vetor_L)  # Vetor L normalizado
    
        # Remover qualquer dimensão extra de norm para garantir que seja 1D
        norm = np.squeeze(self.normais)  # Certificar-se de que norm é 1D

        n_dot_l = max(np.dot(norm, vetor_L), 0)  # Produto escalar (n . l)
    
        vetor_R = 2 * n_dot_l * norm - vetor_L
        vetor_R /= np.linalg.norm(vetor_R)  # Vetor R normalizado
    
        # Garantir que self.vetores_s seja 1D
        vetor_s = np.squeeze(self.vetores_s)  # Remover dimensões extras, se necessário
    
        r_dot_s = max(np.dot(vetor_R, vetor_s), 0)  # Produto escalar (r . s)
        return self.il * self.ks * (r_dot_s ** self.n)

    def Calcular_iluminacao_total(self):  # Iluminação total [It = Ia + Id + Is]
        iluminacoes = []
        Ia = self.Calcular_iluminacao_ambiente()

        # Chamada sem argumento
        Id = self.Calcular_iluminacao_difusa()
        Is = self.Calcular_iluminacao_especular()
        Itotal = Ia + Id + Is
        iluminacoes.append(Itotal)

        return iluminacoes[0]  # Retorna a iluminação total corretamente

# Definindo parâmetros de iluminação
ila = (120, 20, 30)  # Luz ambiente
il = (150, 100, 20)  # Intensidade da lâmpada
luz_pos = [70, 20, 35]  # Posição da lâmpada
ka = (0.4, 0.4, 0.4)  # Coeficiente de reflexão ambiente
kd = (0.7, 0.4, 0.4)  # Coeficiente de reflexão difusa
ks = (0.5, 0.4, 0.4)  # Coeficiente de reflexão especular
n = 2.15  # Expoente especular

# Centroides, normais e vetores S para o sombreamento
centroides_faces_visiveis = np.array([[100, 50, 0.5]])  # Exemplo de centroide para a face visível
vetores_normais_visiveis = np.array([[0.669, 0.378, 0.639]])  # Normal da face
vetores_s = np.array([[-0.002, 0.143, 0.990]])  # Vetor S (direção do observador)

# Instanciando a classe de sombreamento constante
sombrear = Sombreamento_constante(ila, il, ka, kd, ks, n, luz_pos, centroides_faces_visiveis, vetores_normais_visiveis, vetores_s)

# Calculando a iluminação total para a face
iluminacao_total = sombrear.Calcular_iluminacao_total()

# Simulação de um triângulo (exemplo)
p1, p2, p3 = (50, 50, 0.5), (150, 50, 0.2), (100, 150, 0.8)
vertices = sorted([p1, p2, p3], key=lambda p: p[1])  # Ordena por Y

(y1, y2, y3) = vertices[0][1], vertices[1][1], vertices[2][1]
(x1, z1), (x2, z2), (x3, z3) = (vertices[0][0], vertices[0][2]), (vertices[1][0], vertices[1][2]), (vertices[2][0], vertices[2][2])

# Preenchimento por scanlines com sombreamento
for y in range(int(y1), int(y3) + 1):
    if y < y2:
        xa = x1 + (x3 - x1) * (y - y1) / (y3 - y1)
        za = z1 + (z3 - z1) * (y - y1) / (y3 - y1)
        xb = x1 + (x2 - x1) * (y - y1) / (y2 - y1) if y2 != y1 else x2
        zb = z1 + (z2 - z1) * (y - y1) / (y2 - y1) if y2 != y1 else z2
    else:
        xa = x1 + (x3 - x1) * (y - y1) / (y3 - y1)
        za = z1 + (z3 - z1) * (y - y1) / (y3 - y1)
        xb = x2 + (x3 - x2) * (y - y2) / (y3 - y2)
        zb = z2 + (z3 - z2) * (y - y2) / (y3 - y2)
    
    # Aplique a iluminação ao calcular a cor
    color = iluminacao_total.astype(np.uint8)  # A iluminação total agora é o valor da cor
    draw_scanline(y, xa, za, xb, zb, color)
print(framebuffer)

# Exibir a imagem
plt.imshow(framebuffer)
plt.axis('off')
plt.show()
