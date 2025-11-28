# bcp/utils.py

def substring(texto, inicio=0, longitud=None):
    """
    Extrae una subcadena desde una posición inicial y con una longitud dada.

    Parámetros:
        texto (str): Texto original del que se extrae la subcadena.
        inicio (int): Posición inicial (desde 0, izquierda a derecha).
        longitud (int | None): Cantidad de caracteres a extraer. 
                               Si es None, devuelve hasta el final.

    Retorna:
        str: Subcadena resultante. Si el texto es None, devuelve "".
    """
    if texto is None:
        return ""

    texto = str(texto)
    if longitud is None:
        return texto[inicio:]
    else:
        return texto[inicio:inicio + longitud]




