# Criptoanálisis de Cifrados de Sustitución con Técnicas de Fuerza Bruta
### Liceo de Cervantes Barranquilla
### Alberto Orozco



## Cifrado César: 
Un cifrado de sustitución simple donde cada letra se desplaza por un valor fijo k (clave, 0 ≤ k < 26) en el alfabeto. Ejemplo: "A" con k=3 → "D". Matemáticamente: c = (p + k) mod 26.
Vulnerabilidad: Preserva las frecuencias de letras del idioma (e.g., en inglés: E ~12.7%, T ~9.1%). El análisis de frecuencias compara distribuciones observadas con esperadas para identificar el k correcto.
Fuerza Bruta Naiva: Prueba todos los 26 shifts. Para cada uno:

## Conteo de frecuencias: 
Escanea el texto L veces por cada una de las 26 letras (26 × 26 × L comparaciones '==').
Puntuación: Suma de |obs_freq - exp_freq| (26 operaciones por shift).
Total ops: ~676L + 676 (dominante en L).


## Pregunta de Investigación: 
"¿Cuántas operaciones de comparación de frecuencias se requieren, en promedio, para romper un cifrado César en textos de L ∈ {1000, 5000, 10000}, y cómo crece con L?" Respuesta: Determinista ~676L + 676 por trial; crece linealmente (O(L)).
Asunciones: Alfabeto inglés uppercase (A-Z); textos generados con frecuencias reales para simular promedios. Tasa de éxito ~100% para L grande por convergencia estadística.
Complejidad: Temporal O(676L) ≈ O(L); espacial O(1).
