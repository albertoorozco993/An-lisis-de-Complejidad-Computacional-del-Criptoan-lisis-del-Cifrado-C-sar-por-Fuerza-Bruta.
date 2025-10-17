# [CODIGO](script.py)
# Informe Técnico: Análisis de Complejidad Computacional del Criptoanálisis del Cifrado César

![Análisis Computacional](https://img.shields.io/badge/Análisis-Complejidad_Computacional-blue.svg)
![Criptografía Clásica](https://img.shields.io/badge/Criptografía-Clásica-lightgrey.svg)
![Complejidad](https://img.shields.io/badge/Complejidad-O(L)-green.svg)

# [CODIGO](script.py)

Este repositorio contiene el análisis técnico y los materiales de presentación sobre la complejidad computacional del criptoanálisis del **Cifrado César**. El objetivo principal es utilizar este cifrado clásico como un caso de estudio para explorar conceptos fundamentales de eficiencia algorítmica, análisis asintótico (Notación Big O) y su relevancia en la seguridad de los sistemas criptográficos modernos.

## 📜 Contenido

1.  [Introducción al Cifrado César y su Relevancia](#1-introducción-al-cifrado-césar-y-su-relevancia-en-el-análisis-algorítmico)
2.  [La Vulnerabilidad Fundamental: Preservación de Frecuencias](#2-la-vulnerabilidad-fundamental-preservación-de-frecuencias)
3.  [Metodología del Criptoanálisis: Fuerza Bruta Asistida](#3-metodología-del-criptoanálisis-fuerza-bruta-asistida-por-análisis-estadístico)
4.  [Derivación Formal de la Complejidad Computacional](#4-derivación-formal-de-la-complejidad-computacional)
5.  [Análisis de Rendimiento Real: El Impacto de las Constantes](#5-análisis-de-rendimiento-real-el-impacto-de-las-constantes)
6.  [Análisis Comparativo de Complejidad: César vs. Vigenère](#6-análisis-comparativo-de-complejidad-césar-vs-vigenère)
7.  [Conclusiones e Implicaciones para la Criptografía Moderna](#7-conclusiones-e-implicaciones-para-la-criptografía-moderna)
8.  [Cómo Usar este Repositorio](#8-cómo-usar-este-repositorio)
9.  [Licencia](#9-licencia)

---

### 1. Introducción al Cifrado César y su Relevancia en el Análisis Algorítmico

El **Cifrado César**, atribuido históricamente a Julio César, es un cifrado de sustitución monoalfabético donde cada letra del texto plano se desplaza un número fijo de posiciones, $k$, en el alfabeto. Aunque su seguridad es nula para los estándares actuales, su simplicidad lo convierte en un laboratorio ideal para el estudio de la **complejidad algorítmica**.

Formalmente, su operación se define mediante aritmética modular con las siguientes fórmulas:

-   **Cifrado:** $c = (p + k) \pmod{26}$
-   **Descifrado:** $p = (c - k) \pmod{26}$

Donde:
-   `p` es el valor numérico de la letra del texto plano (A=0, B=1, ...).
-   `c` es el valor numérico de la letra del texto cifrado.
-   `k` es la clave secreta o desplazamiento.

El propósito de este informe es realizar un análisis riguroso de la complejidad computacional del criptoanálisis por **fuerza bruta** del Cifrado César, derivando su notación Big O para demostrar cómo los conceptos de coste y eficiencia son cruciales para la evaluación de cualquier sistema criptográfico.

---

### 2. La Vulnerabilidad Fundamental: Preservación de Frecuencias

La debilidad principal del Cifrado César no reside en su transformación, sino en una propiedad crítica que no logra ocultar: la distribución estadística de los caracteres del texto original. Esta vulnerabilidad se conoce como **"Preservación de Frecuencias"**.

El cifrado únicamente desplaza el histograma de frecuencias de las letras del idioma, pero no altera su forma. Si la 'E' es la letra más común en el texto plano, la letra cifrada correspondiente será la más frecuente en el texto cifrado. Este patrón estadístico se mantiene intacto y proporciona una "huella digital" del idioma original que un algoritmo de criptoanálisis puede explotar para validar cuál de las 25 claves posibles es la correcta.



---

### 3. Metodología del Criptoanálisis: Fuerza Bruta Asistida por Análisis Estadístico

La estrategia para romper el Cifrado César combina la búsqueda exhaustiva con una evaluación estadística. Este enfoque automatiza la identificación de la solución correcta al medir la verosimilitud de cada posible descifrado.

El algoritmo sigue los siguientes pasos:

1.  **Iterar el Espacio de Claves**: El algoritmo prueba sistemáticamente todas las claves posibles en el espacio $k \in \{1, 2, ..., 25\}$.
2.  **Generar Texto Candidato**: Para cada clave $k$, se aplica la fórmula de descifrado $p = (c - k) \pmod{26}$ a todo el texto cifrado, generando un texto plano candidato.
3.  **Evaluar Legibilidad (Función de Puntuación)**: Se cuantifica la verosimilitud del texto candidato comparando su distribución de frecuencias de letras con las frecuencias conocidas del idioma español, utilizando una métrica como el Error Cuadrático Medio (MSE).
4.  **Seleccionar la Clave Óptima**: La clave que minimiza el error (o maximiza la similitud) se selecciona como la correcta, y el texto candidato correspondiente se considera el mensaje original.

---

### 4. Derivación Formal de la Complejidad Computacional

Para formalizar el coste del algoritmo, definimos la función de tiempo $T(L)$, donde $L$ es la longitud del texto cifrado y $|\Sigma|$ es el tamaño del alfabeto (26 para el español).

El coste total es la suma de los costes de descifrado y puntuación para cada clave posible:
$$
T(L) = |\Sigma| \times (\text{Coste de Descifrado} + \text{Coste de Puntuación})
$$
Una implementación eficiente realiza el descifrado y el conteo de frecuencias en una sola pasada de $L$ operaciones. La comparación de estas frecuencias es un coste constante $C_{\text{score}}$ (proporcional a $|\Sigma|$).

$$
T(L) = |\Sigma| \times (L + C_{\text{score}}) = 26L + 26 \cdot C_{\text{score}}
$$

Para el análisis asintótico (cuando $L \to \infty$), el término dominante es $26L$. Descartando las constantes multiplicativas y los términos de menor orden, llegamos a la conclusión formal:

> La complejidad computacional del criptoanálisis del Cifrado César es **$O(L)$ (Complejidad Lineal)**.

---

### 5. Análisis de Rendimiento Real: El Impacto de las Constantes

La notación Big O describe el comportamiento asintótico, pero en la práctica, las constantes son importantes. Asumiendo que el coste de puntuación $C_{\text{score}}$ es 26 (una comparación por cada letra del alfabeto), la función de tiempo concreta es:

$$
T(L) = 26L + (26 \times 26) = 26L + 676
$$

La siguiente tabla muestra cómo evoluciona el número total de operaciones para diferentes longitudes de texto:

| Longitud del Texto (L) | Operaciones Totales T(L) |
| :--------------------- | :----------------------- |
| 100                    | 3,276                    |
| 1,000                  | 26,676                   |
| 10,000                 | 260,676                  |

A medida que $L$ crece, el término $26L$ se vuelve dominante, y el coste total crece de manera casi perfectamente lineal, validando empíricamente la notación **$O(L)$**.

---

### 6. Análisis Comparativo de Complejidad: César vs. Vigenère

El valor de este análisis se magnifica al compararlo con cifrados más robustos como el **Cifrado Vigenère**.

* **Cifrado César**: La complejidad de su criptoanálisis es **$O(L)$**. El coste crece proporcionalmente a la longitud del texto.
* **Cifrado Vigenère**: Su criptoanálisis es mucho más costoso. Requiere pasos previos como el método Kasiski para determinar la longitud de la clave ($m$), elevando la complejidad a **$O(L^2)$** o incluso **$O(L \cdot m^2)$**.

Pasar de una complejidad lineal a una cuadrática representa un aumento monumental en los recursos necesarios para la rotura. Si se duplica la longitud del texto, el coste para romper el César se duplica, pero para Vigenère, se cuadruplica. Esto ilustra el principio fundamental de la criptografía: hacer que el coste del criptoanálisis sea computacionalmente inviable.

---

### 7. Conclusiones e Implicaciones para la Criptografía Moderna

El análisis demuestra rigurosamente que el criptoanálisis del Cifrado César tiene una complejidad lineal, **$O(L)$**, lo que lo hace trivialmente rompible. Las implicaciones de este hallazgo son fundamentales:

* **Base para Sistemas Robustos**: El análisis $O(L)$ establece una línea de base. Los cifrados modernos deben basarse en problemas con complejidad intrínsecamente superior (exponencial o subexponencial).
* **Funciones Hash (SHA-256)**: Aunque su cálculo puede ser $O(L)$, su seguridad radica en la intratabilidad de invertir la función (resistencia a la preimagen).
* **Algoritmos Asimétricos (RSA)**: Su seguridad se basa en la dificultad de problemas como la factorización de números primos grandes, cuya complejidad subexponencial está órdenes de magnitud por encima del coste lineal del criptoanálisis del César.

Es imposible validar una clave sin leer, como mínimo, la totalidad del texto, lo que establece a **$O(L)$** como el coste óptimo y el límite inferior teórico para este tipo de criptoanálisis.

---

### 8. Cómo Usar este Repositorio

Este repositorio puede ser utilizado como material de referencia y estudio. En él encontrarás:

* `/informe`: El documento completo del informe técnico en formato PDF.
* `/presentacion`: Las diapositivas utilizadas en la exposición del análisis.
* `/src`: El código fuente (por ejemplo, en Python) utilizado para implementar el algoritmo de criptoanálisis y generar los datos de rendimiento.

---

### 9. Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
