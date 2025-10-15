import string
from typing import Tuple, Dict
from collections import Counter

# Frecuencias del idioma español (Fuente: datos estadísticos)
FRECUENCIAS_ESPANOL: Dict[str, float] = {
    'A': 0.1253, 'B': 0.0142, 'C': 0.0468, 'D': 0.0586, 'E': 0.1368,
    'F': 0.0069, 'G': 0.0101, 'H': 0.0070, 'I': 0.0625, 'J': 0.0044,
    'K': 0.0000, 'L': 0.0524, 'M': 0.0301, 'N': 0.0742, 'O': 0.0962,
    'P': 0.0250, 'Q': 0.0092, 'R': 0.0687, 'S': 0.0798, 'T': 0.0463,
    'U': 0.0393, 'V': 0.0090, 'W': 0.0000, 'X': 0.0017, 'Y': 0.0090,
    'Z': 0.0049
}

ALFABETO = string.ascii_uppercase
TAMANO_ALFABETO = len(ALFABETO)

def cifrar_cesar(texto: str, clave: int) -> str:
    """
    Cifra un texto usando el cifrado César.
    Args:
        texto (str): Texto claro.
        clave (int): Clave de cifrado (desplazamiento).
    Returns:
        str: Texto cifrado.
    """
    resultado = ""
    for char in texto.upper():
        if char in ALFABETO:
            valor_ascii = ord(char) - ord('A')
            valor_cifrado = (valor_ascii + clave) % TAMANO_ALFABETO
            resultado += chr(valor_cifrado + ord('A'))
        else:
            resultado += char
    return resultado

def descifrar_cesar(texto_cifrado: str, clave: int) -> str:
    """
    Descifra un texto cifrado con César.
    Args:
        texto_cifrado (str): Texto cifrado.
        clave (int): Clave de cifrado (desplazamiento).
    Returns:
        str: Texto descifrado.
    """
    return cifrar_cesar(texto_cifrado, -clave % TAMANO_ALFABETO)

def calcular_puntuacion(texto_candidato: str) -> Tuple[float, int]:
    """
    Calcula el Error Cuadrático Medio (MSE) de las frecuencias.
    Args:
        texto_candidato (str): Texto candidato a evaluar.
    Returns:
        Tuple[float, int]: Puntuación (MSE) y coste de operaciones.
    """
    operaciones = 0
    letras = [c for c in texto_candidato.upper() if c in ALFABETO]
    total_letras = len(letras)
    operaciones += len(texto_candidato)
    if total_letras == 0:
        return 1e9, operaciones
    frecuencias_observadas = Counter(letras)
    puntuacion = 0.0
    for char in ALFABETO:
        operaciones += 1
        frec_observada = frecuencias_observadas.get(char, 0) / total_letras
        frec_esperada = FRECUENCIAS_ESPANOL.get(char, 0)
        puntuacion += (frec_observada - frec_esperada) ** 2
    return puntuacion, operaciones

def criptoanalisis_fuerza_bruta(texto_cifrado: str) -> Tuple[int, str, int]:
    """
    Criptoanálisis fuerza bruta para encontrar la clave César.
    Args:
        texto_cifrado (str): Texto cifrado.
    Returns:
        Tuple[int, str, int]: Mejor clave, mejor texto, operaciones totales.
    """
    mejor_puntuacion = 1e9
    mejor_clave = 0
    mejor_texto = ""
    operaciones_totales = 0

    for k in range(TAMANO_ALFABETO):
        operaciones_totales += 1
        texto_descifrado = descifrar_cesar(texto_cifrado, k)
        puntuacion_actual, ops_puntuacion = calcular_puntuacion(texto_descifrado)
        operaciones_totales += ops_puntuacion
        if puntuacion_actual < mejor_puntuacion:
            mejor_puntuacion = puntuacion_actual
            mejor_clave = k
            mejor_texto = texto_descifrado
    return mejor_clave, mejor_texto, operaciones_totales

def ejecutar_analisis_linealidad(texto_base: str, clave: int = 5):
    """
    Genera textos de diferente longitud para probar la linealidad O(L).
    Args:
        texto_base (str): Texto base.
        clave (int): Clave para cifrado.
    """
    print("\n--- ANÁLISIS DE VALIDACIÓN O(L) ---")
    L1_texto = texto_base * 2
    texto_cifrado_L1 = cifrar_cesar(L1_texto, clave)
    L2_texto = texto_base * 4
    texto_cifrado_L2 = cifrar_cesar(L2_texto, clave)
    _, _, ops_L1 = criptoanalisis_fuerza_bruta(texto_cifrado_L1)
    _, _, ops_L2 = criptoanalisis_fuerza_bruta(texto_cifrado_L2)
    proporcion_L = len(texto_cifrado_L2) / len(texto_cifrado_L1)
    proporcion_ops = ops_L2 / ops_L1
    print(f"L1 (Longitud): {len(texto_cifrado_L1):<5} | Operaciones: {ops_L1}")
    print(f"L2 (Longitud): {len(texto_cifrado_L2):<5} | Operaciones: {ops_L2}")
    print(f"Relación Longitud (L2/L1): {proporcion_L:.2f}")
    print(f"Relación Coste (Ops2/Ops1): {proporcion_ops:.2f}")
    assert 1.95 < proporcion_ops < 2.05, (
        f"La complejidad no es lineal O(L)! Proporción observada: {proporcion_ops:.2f}"
    )
    print("\n✅ VALIDACIÓN O(L) EXITOSA: El coste se duplica al duplicar la longitud, confirmando la linealidad.")

def ejecutar_pruebas_correccion():
    """
    Prueba simple para validar que la clave se encuentra correctamente.
    Returns:
        str: Texto claro base.
    """
    texto_claro_base = "ESTEESUNTEXTOMUYLARGOENLENGUAJECASCASTELLANO"
    texto_cifrado = cifrar_cesar(texto_claro_base, 5)
    clave_encontrada, texto_descifrado, ops = criptoanalisis_fuerza_bruta(texto_cifrado)
    assert clave_encontrada == 5, f"La clave encontrada ({clave_encontrada}) no es correcta."
    assert texto_descifrado == texto_claro_base.upper(), "El texto descifrado no coincide con el original."
    print(f"\n--- PRUEBA DE CORRECCIÓN EXITOSA ---")
    print(f"Clave Encontrada: {clave_encontrada} | Coste Total: {ops}")
    return texto_claro_base

if __name__ == "__main__":
    texto_base = ejecutar_pruebas_correccion()
    ejecutar_analisis_linealidad(texto_base)
