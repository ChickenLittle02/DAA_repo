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
    """Versión completa con dos pasadas (verificación exacta)."""
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
    
    return sorted([c for c in candidatos if A.count(c) > n // 3])

def generar_instancia_que_no_atrapa(n, alfabeto_tam, seed=None):
    """
    Generador de la Conferencia (El que NO atrapa el error):
    Planta DOS elementos frecuentes por construcción. 
    Al haber dos mayorías reales, llenan la tabla y el atajo siempre acierta.
    """
    rng = random.Random(seed)
    simbolos = [f"elem_{i}" for i in range(alfabeto_tam)]
    
    # Aseguramos al menos 2 símbolos distintos para plantar
    frec1 = simbolos[0]
    frec2 = simbolos[1] if len(simbolos) > 1 else simbolos[0]
    
    umbral = n // 3
    k_frec = umbral + 1  # Cada uno supera estrictamente n/3
    
    # Plantamos los dos frecuentes (cuidando no exceder n)
    A = [frec1] * k_frec + [frec2] * k_frec
    
    # Rellenar el resto del arreglo con símbolos aleatorios
    resto_simbolos = simbolos[2:] if len(simbolos) > 2 else [frec1]
    while len(A) < n:
        A.append(rng.choice(resto_simbolos))
        
    rng.shuffle(A)
    return A

def probar_generador_que_escapa():
    n = 30
    semilla = 42
    
    print(f"=== PRUEBA CON EL GENERADOR QUE 'NO' ATRAPA EL ERROR (Semilla: {semilla}, n = {n}) ===")
    A = generar_instancia_que_no_atrapa(n, alfabeto_tam=3, seed=semilla)
    
    res_atajo = atajo(A)
    res_correcto = solucion_correcta(A)
    
    print(f"Arreglo generado: {A}")
    print(f"Resultado Atajo (sin verificar): {res_atajo}")
    print(f"Resultado Correcto (con verificar): {res_correcto}")
    print(f"¿Coinciden exactamente (el atajo se escapó del error)?: {res_atajo == res_correcto}")

if __name__ == "__main__":
    probar_generador_que_escapa()