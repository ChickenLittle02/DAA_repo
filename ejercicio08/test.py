import random

def atajo(A):
    """Versión sin verificar (devuelve todos los candidatos con contador > 0)."""
    c1, c2 = None, None
    cnt1, cnt2 = 0, 0
    for x in A:
        if c1 == x: cnt1 += 1
        elif c2 == x: cnt2 += 1
        elif cnt1 == 0: c1, cnt1 = x, 1
        elif cnt2 == 0: c2, cnt2 = x, 1
        else:
            cnt1 -= 1; cnt2 -= 1
            if cnt1 == 0: c1 = None
            if cnt2 == 0: c2 = None
    candidatos = []
    if c1 is not None: candidatos.append(c1)
    if c2 is not None and c2 != c1: candidatos.append(c2)
    return sorted(candidatos)

def solucion_correcta(A):
    """Versión completa con dos pasadas (primera de cancelación + segunda de verificación)."""
    n = len(A)
    c1, c2 = None, None
    cnt1, cnt2 = 0, 0
    for x in A:
        if c1 == x: cnt1 += 1
        elif c2 == x: cnt2 += 1
        elif cnt1 == 0: c1, cnt1 = x, 1
        elif cnt2 == 0: c2, cnt2 = x, 1
        else:
            cnt1 -= 1; cnt2 -= 1
            if cnt1 == 0: c1 = None
            if cnt2 == 0: c2 = None
    
    candidatos = set()
    if c1 is not None: candidatos.add(c1)
    if c2 is not None: candidatos.add(c2)
    
    # Segunda pasada: verificación estricta contra el umbral n // 3
    return sorted([c for c in candidatos if A.count(c) > n // 3])

def generar_instancia_debilidad(n, alfabeto_tam, seed=None):
    """
    Generador reproducible basado en la debilidad de la invariante:
    Usa un generador con seed propia para que la aleatoriedad sea 
    totalmente determinista y replicable.
    """
    # Creamos una instancia local de Random con la semilla dada
    rng = random.Random(seed)
    
    simbolos = [f"elem_{i}" for i in range(alfabeto_tam)]
    frecuente = simbolos[0]
    umbral = n // 3
    k_frec = umbral + 1  # Garantiza que sea estrictamente frecuente
    
    A = [frecuente] * k_frec
    resto_simbolos = simbolos[1:] if len(simbolos) > 1 else [frecuente]
    
    while len(A) < n:
        A.append(rng.choice(resto_simbolos))
        
    rng.shuffle(A)
    return A

def ejecutar_simulacion_reproducible():
    n = 30
    semilla_prueba = 12345  # Semilla fija para replicar el experimento
    
    print(f"=== PRUEBA REPRODUCIBLE (Semilla: {semilla_prueba}, n = {n}) ===")
    
    # Generamos una instancia usando la semilla
    A1 = generar_instancia_debilidad(n, alfabeto_tam=3, seed=semilla_prueba)
    print(f"Arreglo generado 1: {A1}")
    print(f"Resultado Atajo: {atajo(A1)}")
    print(f"Resultado Correcto: {solucion_correcta(A1)}")
    
    print("-" * 60)
    
    # Volvemos a generar con LA MISMA semilla para comprobar que se replica idéntico
    A2 = generar_instancia_debilidad(n, alfabeto_tam=3, seed=semilla_prueba)
    print(f"Arreglo generado 2: {A2}")
    print(f"¿Los arreglos son idénticos?: {A1 == A2}")

if __name__ == "__main__":
    ejecutar_simulacion_reproducible()