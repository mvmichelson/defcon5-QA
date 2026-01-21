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
    

def extraer_desde_char(cadena, char, n_chars=None):
    """
    Extrae caracteres desde la derecha hasta encontrar `char`.
    Si n_chars se indica, devuelve hasta n_chars antes del char.
    """
    pos = cadena.rfind(char)
    if pos == -1:
        return cadena[-n_chars:] if n_chars else cadena
    if n_chars:
        inicio = max(0, pos - n_chars)
        return cadena[inicio:pos]
    return cadena[pos+1:]


def resta_string(a: str, b: str, all_occurrences: bool = True) -> str:
    """
    Resta el string b del string a.

    Parámetros:
    - a: string original
    - b: string a eliminar de a
    - all_occurrences: si True elimina todas las ocurrencias de b, 
                       si False solo la primera
    
    Retorna:
    - Nuevo string resultante

    ej:
    s = "abcdeabcde"

    print(resta_string(s, "bc"))          # "adeade"  → elimina todas las ocurrencias
    print(resta_string(s, "bc", False))   # "adeabcde" → elimina solo la primera
    print(resta_string(s, "xy"))          # "abcdeabcde" → no hace nada si no existe

    """
    if all_occurrences:
        return a.replace(b, "")
    else:
        return a.replace(b, "", 1)



