n = 10

a = [i for i in range(n)]
b = [i % 2 for i in range(n)]

for indB in range(len(b)):  # Parcours des indices de b
    value = b[indB]
    
    if value:  # Si la valeur de b[indB] est 1
        # Toutes les valeurs de la liste a qui sont égales ou supérieures à indB prennent -1
        for indA in range(len(a)):
            if a[indA] >= indB:
                a[indA] = a[indA] - 1  # Correction ici, utilisation de '='

print(a)
print(b)
