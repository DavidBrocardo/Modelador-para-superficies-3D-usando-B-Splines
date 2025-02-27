import numpy as np

class Visibilidade_Normal:

    def __init__(self):
        pass  # Nenhuma inicialização necessária

    def Calcular_vet_normal_unitario_face(self, pontos_face):
        """ Calcula o vetor normal unitário de uma única face usando seus pontos diretamente """
        pontos = np.array(pontos_face)  # Converter para numpy array

        if pontos.shape[0] < 3:
            raise ValueError("Uma face precisa de pelo menos 3 pontos para calcular o vetor normal.")

        p0, p1, p2 = pontos[:3]  # Pegando os três primeiros pontos da face

        v1 = np.array(p1) - np.array(p0)
        v2 = np.array(p2) - np.array(p0)  # Vetores para calcular normal

        Vnormal = np.cross(v1, v2)  # Produto vetorial v1 x v2
        norma = np.linalg.norm(Vnormal)

        if norma == 0:
            return np.array([0, 0, 0])  # Evitar divisão por zero
        
        return Vnormal / norma  # Vetor normal unitário

    def Calcular_centroide_face(self, pontos_face):
        """ Calcula o centroide da face usando seus pontos diretamente """
        pontos = np.array(pontos_face)
        return np.mean(pontos, axis=0)  # Média das coordenadas (x, y, z)

    def Calcular_vet_observacao_face(self, VRP, pontos_face):
        """ Calcula o vetor de observação da face usando seus pontos diretamente """
        VRP = np.array(VRP[:3])  # Garantir que estamos usando apenas (x, y, z)
        centroide = self.Calcular_centroide_face(pontos_face)
        vet_observacao = VRP - centroide  # Vetor de observação

        norma = np.linalg.norm(vet_observacao)
        if norma == 0:
            return np.array([0, 0, 0])  # Evitar divisão por zero
        
        return vet_observacao / norma  # Vetor de observação unitário

    def Verificar_visibilidade_face(self, VRP, pontos_face):
        """ Verifica se uma única face é visível """
        normal = self.Calcular_vet_normal_unitario_face(pontos_face)
        observacao = self.Calcular_vet_observacao_face(VRP, pontos_face)
        produto_escalar = np.dot(normal, observacao)  # Produto escalar

        # Se o produto escalar for negativo, inverter a normal
        if produto_escalar < 0:
            normal = -normal
            produto_escalar = np.dot(normal, observacao)

        return produto_escalar >= 0  # Retorna True se a face for visível


if __name__ == "__main__":
    VRP = [1, 1, 1, 1]  # Ponto de visão

    # Definição das faces diretamente com seus pontos
    face_0 = [
        (250.0, 246.9422254266286, -0.8671815531005864),
        (222.03337437689925, 262.866939649663, 8.329421601481734),
        (250.0, 280.0736078814987, 17.163433406946957),
        (277.96662562310075, 268.90782000217405, 6.620802616842856)
    ]  # Face 0 (quadrangular)

    visi = Visibilidade_Normal()  # Instância da classe

    # Teste para a Face 0
    visivel_0 = visi.Verificar_visibilidade_face(VRP, face_0)
    print(f"Face 0: {'Visível' if visivel_0 else 'Não Visível'}")
