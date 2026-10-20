# clasificacion_variables.py — Parte A: clasificación de las variables de clientes.csv.
#
# El archivo data/clientes.csv tiene 12 clientes y 7 variables (más el id).
# El objetivo: clasificar cada variable (numérica continua/discreta, categórica
# binaria/ordinal/nominal) y verificar la clasificación en código.
#
# Regla del capítulo 3: el dtype es una pista, no la clasificación — el criterio
# (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?) decide.
#
# Uso (desde la raíz del repositorio):  python scripts/clasificacion_variables.py

import pandas as pd

clientes = pd.read_csv("data/clientes.csv")

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas")
print()
print("Primeras filas:")
print(clientes.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (dtype) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
print("Tipos inferidos (dtype):")
print(clientes.dtypes)
print()
# TODO 1: ¿qué columnas llegan como número y cuáles como texto? Anótalo para el
#         informe. Ojo con satisfaccion: llega como número y es ordinal
#         ("4 no es el doble de 2") — la justificación va en el informe.

# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
# TODO 2: completa el bucle para imprimir, por columna, cuántos valores únicos
#         hay y cuáles son. Pista: for columna in clientes.columns: ...  con
#         clientes[columna].unique() y len(). ¿Cuántas categorías tiene genero?
for columna in clientes.columns:
    valores = clientes[columna].unique().tolist() ## le pedimos a pandas los valores unicos
    cantidad = len(valores) ## usando len, sabemos cuantos son
    print(f"{columna}: {cantidad} categorias -> {valores}") ## por cada columna, podemos ver cuantas categorias tienen y cuales son sus valores
    print()

#Segun la salida, genero tiene 3 categorias. (se encontrara tambien en el informe.)

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# Una ordinal se guarda como texto (o como número) y su orden natural se pierde:
# alfabéticamente "Posgrado" iría antes que "Primaria", que no tiene sentido.
#
# TODO 3: convierte nivel_educacion a categoría ordenada.
#         Pista: astype(pd.CategoricalDtype(categories=[...], ordered=True)).
#         Comprueba con .min(): debe devolver "Primaria".

## Utilizar esta libreria y en concreto categories y ordered me ayuda a "imponer un orden sobre los datos
# Para este caso utilice una variable orden_niveles para que al usar .astype() no sea tan largo y sea mas legible
from pandas.api.types import CategoricalDtype

orden_niveles = CategoricalDtype(
    categories=["Primaria", "Secundaria", "Universidad", "Posgrado"],
    ordered=True
)
clientes["nivel_educacion"] = clientes["nivel_educacion"].astype(orden_niveles)

print(clientes["nivel_educacion"].min()) ##Imprime el valor menor segun el orden, Primaria
print(clientes["nivel_educacion"].max()) ##Imprimir el valor mayor segun el orden, Posgrado


# TODO 4: haz lo mismo con satisfaccion (escala 1–5 como etiquetas ordenadas).
#         Prueba extra: ¿qué pasa si en la lista de categorías escribes
#         "Postgrado" (con t) para nivel_educacion? Cuenta los faltantes con
#         .isna().sum() — la trampa del typo es silenciosa.

from pandas.api.types import CategoricalDtype

orden_satisfaccion = CategoricalDtype(
    categories=[1, 2, 3, 4, 5],
    ordered=True
)
clientes["satisfaccion"] = clientes["satisfaccion"].astype(orden_satisfaccion)
print(clientes["satisfaccion"].min()) ## Imprimira 2 dado que en los datos nadie se registro con nivel 1 de satisfaccion
print(clientes["satisfaccion"].max()) ## Imprimira 5

# Nota sobre la prueba extra:
'''
Dado que CategoricalDtype es muy estricto con las faltas de ortografia y errores de ese tipo,
si ubico "Postgrado" va a pasar que no lo reconoce dentro de los datos, al contar los faltantes con este
typo con .isna().sum() me devolvera 2, dado que son 2 los registros que fueron clasificados como NaN
(not a number) al no coincidir con Postgrado.
'''

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
# TODO 5: completa el resumen con el tipo de cada variable (el criterio que
#         justifica cada clasificación va en el informe).
clasificacion = {
    "cliente_id": "Identificador",
    "edad": "Numerica Discreta",
    "numero_hijos": "Numerica Discreta",
    "genero": "Categorica Nominal",
    "nivel_educacion": "Categorica Ordinal",
    "ciudad": "Categorica nominal",
    "ingresos_mensuales": "Numerica continua",
    "satisfaccion": "Categorica Ordinal",
}
print("Resumen de la clasificación (para el informe):")
for variable, tipo in clasificacion.items():
    print(f"  {variable:20s} {tipo}")
