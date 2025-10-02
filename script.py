import random
import string
import matplotlib.pyplot as plt

EXPECTED_FREQS = {
    'A': 0.0817, 'B': 0.0149, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270,
    'F': 0.0223, 'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015,
    'K': 0.0077, 'L': 0.0403, 'M': 0.0241, 'N': 0.0675, 'O': 0.0751,
    'P': 0.0193, 'Q': 0.0009, 'R': 0.0599, 'S': 0.0633, 'T': 0.0906,
    'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015, 'Y': 0.0197, 'Z': 0.0007
}

def generate_plain_text(length, expected_freqs):
    """
    Genera un texto plano de longitud 'length' siguiendo las frecuencias esperadas.
    - Por qué: Simula textos realistas para pruebas representativas.
    - Cómo: Selección probabilística cumulativa.
    - Retorna: str (texto uppercase).
    """
    text = ''
    total_freq = sum(expected_freqs.values())
    for _ in range(length):
        rand = random.random() * total_freq
        cumulative = 0
        for letter, freq in expected_freqs.items():
            cumulative += freq
            if rand <= cumulative:
                text += letter
                break
        else:
            text += 'E'  
    return text

def caesar_cipher(text, shift):
    """
    Cifra el texto con desplazamiento 'shift'.
    - Por qué: Implementa el cifrado base.
    - Cómo: Aritmética modular mod 26.
    - Retorna: str (texto cifrado).
    """
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def break_caesar_naive(cipher_text, expected_freqs):
    """
    Rompe el cifrado con fuerza bruta naiva, contando comparaciones.
    - Por qué: Mide ops para tu pregunta (676L + 676 approx).
    - Cómo: Para cada shift, conteo naivo (26 letras × L escaneos) + score.
    - Retorna: (best_shift, total_comparisons, best_score, scores_list).
    """
    total_comparisons = 0
    best_shift = 0
    best_score = float('inf')
    scores = []
    
    for shift in range(26):
        comparisons = 0
        freq_count = {letter: 0 for letter in string.ascii_uppercase}
        for target_letter in string.ascii_uppercase:
            count = 0
            for char in cipher_text:
                if char.isalpha():
                    deciphered = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    if deciphered == target_letter:
                        count += 1
                    comparisons += 1
            freq_count[target_letter] = count
        total_comparisons += comparisons
        
        score_comparisons = 0
        score = 0
        text_length = len(cipher_text)
        for letter in string.ascii_uppercase:
            obs_freq = freq_count[letter] / text_length if text_length > 0 else 0
            diff = abs(obs_freq - expected_freqs[letter])
            score += diff
            score_comparisons += 1
        total_comparisons += score_comparisons
        scores.append(score)
        
        if score < best_score:
            best_score = score
            best_shift = shift
    
    return best_shift, total_comparisons, best_score, scores

def plot_scores_example(scores, true_shift, L):
    """
    Gráfica scores vs. shifts para demo.
    - Por qué: Visualiza el mínimo en el shift correcto.
    - Cómo: Plot con Matplotlib.
    """
    shifts = range(26)
    plt.figure(figsize=(10, 6))
    plt.plot(shifts, scores, marker='o', label=f'Scores para L={L}')
    plt.axvline(true_shift, color='r', linestyle='--', label='Shift Verdadero')
    plt.xlabel('Shift Probado')
    plt.ylabel('Score (Diferencias Absolutas)')
    plt.title('Análisis de Frecuencias en Acción')
    plt.legend()
    plt.grid(True)
    plt.show()

def run_simulation(lengths=[1000, 5000, 10000], num_trials=10):
    """
    Simula múltiples trials para cada L y responde tu pregunta.
    - Por qué: Calcula promedios y genera visuals.
    - Cómo: Genera/cifra/rompe; mide ops/éxito.
    - Retorna: dict con resultados.
    """
    results = {}
    for L in lengths:
        total_ops = []
        successes = 0
        example_scores = None
        example_true_shift = None
        
        print(f"\nSimulando para L={L} ({num_trials} trials)...")
        for trial in range(num_trials):
            plain_text = generate_plain_text(L, EXPECTED_FREQS)
            true_shift = random.randint(1, 25)
            cipher_text = caesar_cipher(plain_text, true_shift)
            
            found_shift, ops, _, scores_list = break_caesar_naive(cipher_text, EXPECTED_FREQS)
            total_ops.append(ops)
            if found_shift == true_shift:
                successes += 1
            
            if trial == 0:
                example_scores = scores_list
                example_true_shift = true_shift
        
        avg_ops = sum(total_ops) / num_trials
        success_rate = (successes / num_trials) * 100
        theoretical = 26 * 26 * L + 26 * 26 
        results[L] = {'avg_ops': avg_ops, 'success_rate': success_rate}
        
        print(f"  - Ops promedio: {avg_ops:.0f} (Teórico: {theoretical})")
        print(f"  - Tasa de éxito: {success_rate:.1f}%")
        
        if example_scores:
            plot_scores_example(example_scores, example_true_shift, L)
    
    print("\nResumen Final:")
    print("| Longitud L | Ops Promedio | Tasa Éxito (%) |")
    print("|------------|--------------|----------------|")
    for L, data in results.items():
        print(f"| {L:10} | {data['avg_ops']:12.0f} | {data['success_rate']:14.1f} |")
    
    return results

if __name__ == "__main__":
    run_simulation()
