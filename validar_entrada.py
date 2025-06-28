def pega_numero_negativo(texto):
    while True:
        try:
            entrada = int(input(texto))
            if entrada < 0 or not entrada:
                raise ValueError
            else:
                return entrada
        except ValueError:
            print("Digite uma entrada válida, sem letras ou caracteres especiais.")
def pega_string(texto):
    while True:
        entrada = str(input(texto))
        if all(char.isalpha() or char.isspace() for char in entrada):
            return entrada
        else:
            print("Digite uma entrada válida, sem números ou caracteres especiais.")


