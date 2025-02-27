def calcular_nota(AV1, AV2, AV3, TP1, TP2, LE1, LE2, LE3, LE4, HG1):
    nota = (25*AV1 + 25*AV2 + 25*AV3 + 5*TP1 + 15*TP2 + 5*((LE1+LE2+LE3+LE4+HG1)/5)) / 100
    return nota

AV1, AV2, AV3 = 90, 90, 65  #Notas das provas
TP1, TP2 = 98, 0  #Notas dos trabalhos
LE1, LE2, LE3, LE4, HG1 = 100, 98, 100, 50, 100  #Notas das listas de exercicicos

nota_final = calcular_nota(AV1, AV2, AV3, TP1, TP2, LE1, LE2, LE3, LE4, HG1)

print(f"Nota final é: {nota_final:.2f}")