import random
import math
import matplotlib.pyplot as plt

# ==========================================
# 1. IMPLEMENTACIÓN DE LAS ESTRUCTURAS
# ==========================================

class PilaConMinimo:
    """Solución Original: Guarda el mínimo del prefijo en M."""
    def __init__(self):
        self.S = []
        self.M = []

    def push(self, x):
        self.S.append(x)
        self.M.append(x if not self.M else min(x, self.M[-1]))

    def pop(self):
        if not self.S:
            raise IndexError("pop desde una pila vacía")
        self.M.pop()
        return self.S.pop()

    def tope(self):
        return self.S[-1]

    def minimo(self):
        return self.M[-1]


class PilaConMinimoContador:
    """Variante de Pares: M almacena [valor_minimo, contador]."""
    def __init__(self):
        self.S = []
        self.M = []  # Pares: [valor_minimo, contador]

    def push(self, x):
        self.S.append(x)
        if not self.M or x < self.M[-1][0]:
            self.M.append([x, 1])
        elif x == self.M[-1][0]:
            self.M[-1][1] += 1

    def pop(self):
        if not self.S:
            raise IndexError("pop desde una pila vacía")
        y = self.S.pop()
        if y == self.M[-1][0]:
            self.M[-1][1] -= 1
            if self.M[-1][1] == 0:
                self.M.pop()
        return y

    def tope(self):
        return self.S[-1]

    def minimo(self):
        return self.M[-1][0]


# ==========================================
# 2. PRUEBAS FUNCIONALES CON ASSERT
# ==========================================

def verificar_equivalencia_pilas(num_operaciones=10000):
    pila_original = PilaConMinimo()
    pila_contador = PilaConMinimoContador()
    
    for _ in range(num_operaciones):
        # 60% de probabilidad de push, 40% de pop (si no está vacía)
        if not pila_original.S or random.random() < 0.6:
            x = random.randint(-500, 500)
            pila_original.push(x)
            pila_contador.push(x)
        else:
            pila_original.pop()
            pila_contador.pop()
        
        # Validaciones funcionales
        if pila_original.S:
            assert pila_original.tope() == pila_contador.tope(), "Error: El tope no coincide"
            assert pila_original.minimo() == pila_contador.minimo(), "Error: El mínimo no coincide"
            assert len(pila_original.S) == len(pila_contador.S), "Error: El tamaño de S no coincide"
            
    print(">>> ¡Prueba de equivalencia funcional con assert superada con éxito!\n")


# ==========================================
# 3. EVALUACIÓN Y ANÁLISIS DE CASOS DINÁMICOS
# ==========================================

def medir_uso_memoria_real(pila):
    """
    Calcula el costo en palabras de memoria según la estructura interna:
    - PilaConMinimo: len(S) + len(M)
    - PilaConMinimoContador: len(S) + 2 * len(M) (2 palabras por cada par [v, c])
    """
    if isinstance(pila, PilaConMinimo):
        return len(pila.S) + len(pila.M)
    elif isinstance(pila, PilaConMinimoContador):
        return len(pila.S) + 2 * len(pila.M)
    return 0


def analizar_casos_memoria_dinamico(tamanios=None, repeticiones_promedio=5):
    if tamanios is None:
        tamanios = [100, 500, 1000, 2500, 5000, 10000]

    print("=" * 115)
    print(f"{'n (elementos)':<12} | {'Alg. 1 (Prom)':<13} | {'Alg. 1 (Peor)':<13} | {'Alg. 2 (Prom)':<13} | {'Alg. 2 (Peor)':<13} | {'Esperado ($n+2H_n$)':<18} | {'¿Cumple?':<8}")
    print("=" * 115)

    datos_grafico = {
        'n': [],
        'alg1_prom': [], 'alg1_peor': [],
        'alg2_prom': [], 'alg2_peor': [],
        'teorico': []
    }

    for n in tamanios:
        # --- CASO PROMEDIO (Datos Aleatorios i.i.d.) ---
        # Se promedian varias corridas dinámicas para mitigar la varianza aleatoria
        mem_a1_prom_acum = 0
        mem_a2_prom_acum = 0
        
        for _ in range(repeticiones_promedio):
            datos_rand = [random.randint(1, 1000000) for _ in range(n)]
            
            p1_prom = PilaConMinimo()
            p2_prom = PilaConMinimoContador()
            for x in datos_rand:
                p1_prom.push(x)
                p2_prom.push(x)
                
            mem_a1_prom_acum += medir_uso_memoria_real(p1_prom)
            mem_a2_prom_acum += medir_uso_memoria_real(p2_prom)

        mem_alg1_prom = round(mem_a1_prom_acum / repeticiones_promedio, 2)
        mem_alg2_prom = round(mem_a2_prom_acum / repeticiones_promedio, 2)

        # --- PEOR CASO (Secuencia estrictamente decreciente: n, n-1, ..., 1) ---
        datos_peor = list(range(n, 0, -1))
        
        p1_peor = PilaConMinimo()
        p2_peor = PilaConMinimoContador()
        for x in datos_peor:
            p1_peor.push(x)
            p2_peor.push(x)

        mem_alg1_peor = medir_uso_memoria_real(p1_peor)
        mem_alg2_peor = medir_uso_memoria_real(p2_peor)

        # --- VALOR TEÓRICO ESPERADO: n + 2 * H_n ---
        # H_n ≈ ln(n) + gamma (Constante de Euler-Mascheroni ≈ 0.5772156649)
        h_n = math.log(n) + 0.5772156649
        costo_esperado = round(n + 2 * h_n, 2)

        # Verificación de hipótesis
        # Se verifica si Alg. 1 es ~2n en ambos casos, Alg. 2 Peor Caso es 3n y Alg. 2 Promedio bordea n + 2*ln(n)
        cumple_hipotesis = (
            mem_alg1_prom == 2 * n and 
            mem_alg1_peor == 2 * n and 
            mem_alg2_peor == 3 * n and 
            abs(mem_alg2_prom - costo_esperado) < (0.05 * n)  # Margen relativo del 5%
        )
        veredicto = "SÍ" if cumple_hipotesis else "NO"

        # Guardar resultados
        datos_grafico['n'].append(n)
        datos_grafico['alg1_prom'].append(mem_alg1_prom)
        datos_grafico['alg1_peor'].append(mem_alg1_peor)
        datos_grafico['alg2_prom'].append(mem_alg2_prom)
        datos_grafico['alg2_peor'].append(mem_alg2_peor)
        datos_grafico['teorico'].append(costo_esperado)

        print(f"{n:<12} | {mem_alg1_prom:<13} | {mem_alg1_peor:<13} | {mem_alg2_prom:<13} | {mem_alg2_peor:<13} | {costo_esperado:<18} | {veredicto:<8}")

    print("=" * 115)
    return datos_grafico


def generar_grafico_respaldo(datos):
    """Genera una gráfica comparativa detallada para adjuntar al informe/markdown."""
    plt.figure(figsize=(11, 6))

    plt.plot(datos['n'], datos['alg1_prom'], label="Alg. 1 (Original: Fijo $2n$)", color="blue", linestyle="-", marker="o", linewidth=2)
    plt.plot(datos['n'], datos['alg2_peor'], label="Alg. 2 (Peor Caso Estricto: $3n$)", color="red", linestyle=":", marker="^", linewidth=2)
    plt.plot(datos['n'], datos['alg2_prom'], label="Alg. 2 (Caso Promedio Empírico)", color="green", linestyle="--", marker="s", linewidth=2)
    plt.plot(datos['n'], datos['teorico'], label="Costo Esperado Teórico ($n + 2H_n$)", color="orange", linestyle="-.", marker="x", linewidth=1.5)

    plt.xlabel("Tamaño de la secuencia de entrada ($n$)", fontsize=11)
    plt.ylabel("Consumo total de memoria (Palabras)", fontsize=11)
    plt.title("Análisis Empírico de Memoria: Algoritmo Original vs. Variante de Contadores", fontsize=13)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    plt.savefig("comparacion_memoria_dinamica.png", dpi=300)
    print("\n[+] Gráfico guardado exitosamente como 'comparacion_memoria_dinamica.png'.")


if __name__ == "__main__":
    verificar_equivalencia_pilas()
    resultados = analizar_casos_memoria_dinamico()
    generar_grafico_respaldo(resultados)