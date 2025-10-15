import string
from typing import Tuple, Dict, List

# Frecuencias del idioma español (Fuente: datos estadísticos)
FRECUENCIAS_ESPANOL: Dict[str, float] = {
    'A': 0.1253, 'B': 0.0142, 'C': 0.0468, 'D': 0.0586, 'E': 0.1368,
    'F': 0.0069, 'G': 0.0101, 'H': 0.0070, 'I': 0.0625, 'J': 0.0044,
    'K': 0.0000, 'L': 0.0524, 'M': 0.0301, 'N': 0.0742, 'O': 0.0962,
    'P': 0.0250, 'Q': 0.0092, 'R': 0.0687, 'S': 0.0798, 'T': 0.0463,
    'U': 0.0393, 'V': 0.0090, 'W': 0.0000, 'X': 0.0017, 'Y': 0.0090,
    'Z': 0.0049
}

def descifrar_cesar(texto_cifrado: str, clave: int) -> str:
    """Aplica la fórmula modular p = (c - k) mod 26 para descifrar."""
    resultado = ""
    # O(L) - Bucle lineal sobre la longitud del texto
    for char in texto_cifrado.upper():
        if 'A' <= char <= 'Z':
            # 1. Mapear a 0-25
            valor_ascii = ord(char) - ord('A')
            # 2. Aplicar la fórmula: asegura que el resultado es positivo con +26
            valor_descifrado = (valor_ascii - clave + 26) % 26
            # 3. Mapear de vuelta a letra
            resultado += chr(valor_descifrado + ord('A'))
        else:
            resultado += char
    return resultado

def calcular_puntuacion(texto_candidato: str) -> Tuple[float, int]:
    """
    Calcula el Error Cuadrático Medio (MSE) de las frecuencias.
    Retorna la puntuación (MSE) y el coste de operaciones (O(L) + O(Sigma)).
    """
    operaciones: int = 0
    frecuencias_observadas: Dict[str, int] = {}
    total_letras: int = 0

    # 1. O(L): Conteo de frecuencias y coste lineal
    for char in texto_candidato.upper():
        operaciones += 1  # Coste 1: Lectura y procesamiento de cada caracter (FACTOR L)
        if 'A' <= char <= 'Z':
            frecuencias_observadas[char] = frecuencias_observadas.get(char, 0) + 1
            total_letras += 1
    
    if total_letras == 0:
        return 1e9, operaciones

    # 2. O(|Sigma|): Cálculo del MSE (La constante 26)
    puntuacion: float = 0.0
    for char in string.ascii_uppercase:
        operaciones += 1  # Coste 2: Una operación por cada letra (FACTOR 26)
        
        # Calcular frecuencias relativas
        frec_observada = frecuencias_observadas.get(char, 0) / total_letras
        frec_esperada = FRECUENCIAS_ESPANOL.get(char, 0)
        
        # Sumar el error cuadrático (MSE)
        puntuacion += (frec_observada - frec_esperada) ** 2

    # Una puntuación más baja indica una mayor similitud con el español
    return puntuacion, operaciones

def criptoanalisis_fuerza_bruta(texto_cifrado: str) -> Tuple[int, str, int]:
    """
    Función principal de criptoanalisis. Itera las 26 claves.
    Complejidad Total: O(|Sigma| * L) => O(L)
    """
    mejor_puntuacion: float = 1e9  # Inicialización a valor muy alto
    mejor_clave: int = 0
    mejor_texto: str = ""
    operaciones_totales: int = 0
    
    # Bucle Principal O(|Sigma|)
    for k in range(26):
        operaciones_totales += 1 # Contar la iteración del bucle principal (FACTOR 26)
        
        # 1. Descifrado O(L) - La complejidad está dominada por aquí.
        texto_descifrado = descifrar_cesar(texto_cifrado, k)
        
        # 2. Puntuación O(L + |Sigma|)
        puntuacion_actual, ops_puntuacion = calcular_puntuacion(texto_descifrado)
        
        # Sumar el coste total acumulado de la iteración
        operaciones_totales += ops_puntuacion
        
        # 3. Actualización del mejor resultado
        if puntuacion_actual < mejor_puntuacion:
            mejor_puntuacion = puntuacion_actual
            mejor_clave = k
            mejor_texto = texto_descifrado

    return mejor_clave, mejor_texto, operaciones_totales

# --- PRUEBAS AUTOMATIZADAS Y ANÁLISIS DE LINEALIDAD ---

def ejecutar_analisis_linealidad(texto_base: str, clave: int = 5):
    """
    Genera dos textos, uno el doble de largo que el otro, para probar la linealidad O(L).
    """
    print("\n--- ANÁLISIS DE VALIDACIÓN O(L) ---")
    
    # Generar Caso 1: L_pequeña (ej. 100 caracteres)
    L1_texto = texto_base * 2 
    texto_cifrado_L1 = descifrar_cesar(L1_texto, clave)
    
    # Generar Caso 2: L_grande (el doble de L1)
    L2_texto = texto_base * 4 
    texto_cifrado_L2 = descifrar_cesar(L2_texto, clave)
    
    # 1. Ejecutar y medir el coste
    _, _, ops_L1 = criptoanalisis_fuerza_bruta(texto_cifrado_L1)
    _, _, ops_L2 = criptoanalisis_fuerza_bruta(texto_cifrado_L2)
    
    proporcion_L = len(texto_cifrado_L2) / len(texto_cifrado_L1)
    proporcion_ops = ops_L2 / ops_L1
    
    print(f"L1 (Longitud): {len(texto_cifrado_L1):<5} | Operaciones: {ops_L1}")
    print(f"L2 (Longitud): {len(texto_cifrado_L2):<5} | Operaciones: {ops_L2}")
    print(f"Relación Longitud (L2/L1): {proporcion_L:.2f}")
    print(f"Relación Coste (Ops2/Ops1): {proporcion_ops:.2f}")

    # Afirmación clave de O(L): La proporción debe ser cercana a 2.0
    assert 1.95 < proporcion_ops < 2.05, "La complejidad no es lineal O(L)!"
    print("\n✅ VALIDACIÓN O(L) EXITOSA: El coste se duplica al duplicar la longitud, confirmando la linealidad.")
    
def ejecutar_pruebas_correccion():
    """Prueba simple para validar que la clave se encuentra correctamente."""
    texto_claro_base = "ESTEESUNTEXTOMUYLARGOENLENGUAJECASCASTELLANO"
    texto_cifrado = descifrar_cesar(texto_claro_base, 5) # Clave: 5
    
    clave_encontrada, texto_descifrado, ops = criptoanalisis_fuerza_bruta(texto_cifrado)
    
    assert clave_encontrada == 5
    assert texto_descifrado == texto_claro_base.upper()
    print(f"\n--- PRUEBA DE CORRECCIÓN EXITOSA ---")
    print(f"Clave Encontrada: {clave_encontrada} | Coste Total: {ops}")
    
    return texto_claro_base

if __name__ == "__main__":
    texto_base = ejecutar_pruebas_correccion()
    ejecutar_analisis_linealidad(texto_base)
