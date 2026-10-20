# clasificacion_variables.R — Parte A: clasificación de las variables de clientes.csv.
#
# El archivo data/clientes.csv tiene 12 clientes y 7 variables (más el id).
# El objetivo: clasificar cada variable (numérica continua/discreta, categórica
# binaria/ordinal/nominal) y verificar la clasificación en código.
#
# Regla del capítulo 3: el tipo que infiere el lenguaje es una pista, no la
# clasificación — el criterio (¿tiene sentido la mitad del valor? ¿hay orden
# entre las categorías?) decide.
#
# Uso (desde la raíz del repositorio):  Rscript scripts/clasificacion_variables.R

clientes <- read.csv("data/clientes.csv", stringsAsFactors = FALSE)

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
cat(sprintf("Dimensiones: %d filas × %d columnas\n", nrow(clientes), ncol(clientes)))
print(clientes)

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (str) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
str(clientes)
# TODO 1: ¿qué columnas llegan como número (int) y cuáles como texto
#         (character)? Anótalo para el informe. Ojo con satisfaccion: llega
#         como número y es ordinal ("4 no es el doble de 2") — la justificación
#         va en el informe.
# - columnas que llegan como número (int / num):
#     • cliente_id (int)
#     • edad (int)
#     • numero_hijos (int)
#     • ingresos_mensuales (num)
#     • satisfaccion (int): llega como entero (1 a 5), pero es categórica ordinal.
#       justificación: "4 no es el doble de 2", representa un nivel subjetivo de satisfacción y no una cantidad medible.
# - columnas que llegan como texto (chr):
#     • genero (chr)
#     • nivel_educacion (chr)
#     • ciudad (chr)
# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
# TODO 2: completa el bucle para imprimir, por columna, cuántos valores únicos
#         hay y cuáles son. Pista: for (columna in names(clientes)) { ... } con
#         unique() y length(). ¿Cuántas categorías tiene genero?
for (columna in names(clientes)) {
  valores <- unique(clientes[[columna]])
  cantidad <- length(valores)
  cat(columna, ": ", cantidad, "-> ", paste(valores, collapse = ", "), "\n")
  cat("\n")
}

# Al igual que en Python, genero tiene 3 categorias

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# Una ordinal se guarda como texto y su orden natural se pierde: alfabéticamente
# "Posgrado" iría antes que "Primaria", que no tiene sentido. En R, eso se
# declara con el factor ordenado.
#
# TODO 3: convierte nivel_educacion con factor(..., levels = c(...), ordered = TRUE).
#         Comprueba con min(): debe devolver "Primaria".

orden_niveles <- c("Primaria", "Secundaria", "Universidad", "Posgrado")
clientes$nivel_educacion <- factor(clientes$nivel_educacion, levels = orden_niveles, ordered = TRUE)
cat("Mínimo nivel_educacion:", as.character(min(clientes$nivel_educacion, na.rm = TRUE)), "\n")
cat("Máximo nivel_educacion:", as.character(max(clientes$nivel_educacion, na.rm = TRUE)), "\n\n")

# TODO 4: haz lo mismo con satisfaccion (escala 1–5 como etiquetas ordenadas).
#         Prueba extra: ¿qué pasa si en levels escribes "Postgrado" (con t) para
#         nivel_educacion? Cuenta los faltantes con sum(is.na(...)) — la trampa
#         del typo es silenciosa.

orden_satisfaccion <- 1:5
clientes$satisfaccion <- factor(clientes$satisfaccion, levels = orden_satisfaccion, ordered = TRUE)

cat("Mínima satisfacción:", as.character(min(clientes$satisfaccion, na.rm = TRUE)), "\n")
cat("Máxima satisfacción:", as.character(max(clientes$satisfaccion, na.rm = TRUE)), "\n\n")

# nota sobre la prueba extra:
# dado que factor() con levels es estricto con la ortografía, si pones "postgrado" no reconocerá los 
# datos que dicen "posgrado" y sum(is.na(...)) 
# devolverá 2, ya que esos 2 registros se convierten en NA al no coincidir con los niveles

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
# TODO 5: completa el resumen con el tipo de cada variable (el criterio que
#         justifica cada clasificación va en el informe).
clasificacion <- c(
  cliente_id         = "Identificador",
  edad               = "Numérica Discreta",
  numero_hijos       = "Numérica Discreta",
  genero             = "Categórica Nominal",
  nivel_educacion    = "Categórica Ordinal",
  ciudad             = "Categórica Nominal",
  ingresos_mensuales = "Numérica Continua",
  satisfaccion       = "Categórica Ordinal"
)
cat("\nResumen de la clasificación (para el informe):\n")
for (variable in names(clasificacion)) {
  cat(sprintf("  %-18s %s\n", variable, clasificacion[[variable]]))
}
