# Informe — Clasificación de variables y población vs. muestra

**Para:** Gerencia de RetailAndina S.A. · **De:** Equipo de Business Intelligence
**Fecha:** 21/10/2026 · **Asunto:** Base de fidelización: tipos de variables y estimación por muestreo

---

## Resumen ejecutivo

Se analizaron los datos del sistema de fidelización compuesto por 400 clientes mediante la clasificación de las variables presentes, mediante el uso de conceptos y software estadístico como Python y R. Además, se hizo un análisis de sesgos dados diseños de muestreo con n=20, se concluye gracias a las pruebas realizadas que mediante la muestra se omiten regiones enteras, provocando un sesgo de selección claro. El siguiente paso para gerencia deberá ser exigir muestreos representativos y equitativos para todas las regiones.

## Parte A — Clasificación de las variables

*Completa la tabla usando el **criterio** (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?), no el ejemplo. En «verificación» anota qué mostró el código: dtype, número de valores únicos y, si declaraste el orden, cómo lo comprobaste.*

| Variable | Tipo | Justificación (criterio) | Verificación en código |
|---|---|---|---|
| `cliente_id` |Categórica Nominal |Es un identificador, no tiene sentido hacer operaciones estadísticas de ningún tipo con este valor. |dtype = object (Python), character (R) |
| `edad` |Numérica Discreta |Variable cuantitativa que describe los años cumplidos, no toma valores decimales. |dtype = int64 (Python), integer (R) |
| `numero_hijos` |Numérica Discreta |Cantidad contable de personas, no podemos contar "la mitad" de una persona, por lo tanto no toma valores decimales |dtype = int64 (Python), integer (R) |
| `genero` |Categórica Nominal |No existe ningún orden o prioridad y las respuestas son binarias (Masculino, Femenino, Otro) |dtype = object (Python), character (R) |
| `nivel_educacion` |Categórica Ordinal |Se propone como una secuencia, es decir, va desde primaria hasta posgrado, existe una jerarquía |Usé CategoricalDtype y métodos .min() y .max() para demostrar esta jerarquía |
| `ciudad` |Categórica Nominal |No existe ninguna jerarquía y solo describe la ubicación geográfica |dtype = object (R), character (R) |
| `ingresos_mensuales` |Numérica Contínua |Se trata del sueldo de una persona, suele contener valores decimales. |dtype = int64 (Python), float64 (R) |
| `satisfaccion` |Categórica Ordinal |Se puede medir mediante una jerarquía, es decir, 1: menos satisfecho, 5: más satisfecho. |dtype = int64 (Python), integer (R) |

**P1.** ¿Qué te dijo el dtype de `satisfaccion` y por qué no basta para clasificarla? ¿Qué pasa si una ordinal queda como texto sin declarar el orden?

A los ojos del software, la variable "satisfaccion" devolvió un tipo entero para ambos lenguajes, no es suficiente para clasificarla dado que ningún software sabe nada sobre conceptos, es decir, el software no puede saber el contexto ni el concepto estadístico asociado a esta variable, es por eso que en alguno de los TODOs se planteaba la pregunta sobre si un nivel 4 de satisfacción es el "doble" de un nivel 2 satisfacción, podemos responder que no, para el software puede ser el doble porque se trata de simplemente un número entero, pero para la interpretación si yo declaro que mi satisfacción es de 4, no quiere decir necesariamente que estoy el doble de satisfecho que alguien que escogió un nivel 2 de satisfacción.

## Parte B — Población vs. muestra

### La población y su parámetro

| Concepto | Valor |
|---|---|
| Población (N) |400 clientes |
| Variable de interés |Ingresos mensuales (ingresos_mensuales) |
| Parámetro poblacional (media) |1330.72 USD |

*¿Por qué se muestrea si aquí el parámetro existe y se calculó?*

Dado que tenemos a la mano los datos en clientes_400.csv podemos evaluar el diseño muestral y comprobar su precisión teniendo en cuenta a toda la población. En casos de la vida real es muy difíicil o costoso ya que la población pueden ser como miles o hasta millones.

### Los tres diseños

*Corre tu script y registra las salidas. La composición por ciudad es la que delata el sesgo: anótala tal como salió.*

| Diseño | n | Media estimada | Composición por ciudad | Diferencia vs. parámetro |
|---|---|---|---|---|
| Conveniencia (`head`) | 20|1348.50 USD |Quito: 20, Guayaquil: 0, Cuenca: 0|+17.78 USD |
| Aleatorio simple (`sample`) |20 |1336.00 USD|Quito: 8, Cuenca: 8, Guayaquil: 4 |+5.28 USD |
| Estratificado (`groupby` + 5 %) |20 |1287.50 USD |Quito: 10, Guayaquil: 6, Cuenca: 4|-43.22 USD |

*Anota también las medias de 5 sorteos distintos del aleatorio simple (semillas 1 a 5):*

| Semilla | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Media |1336.00 USD |1405.00 USD |1235.00 USD |1491.50 USD |1288.00 USD |

**P2.** ¿Cuánto vale el parámetro poblacional y cuánto estimó cada diseño? ¿Cuál quedó más cerca y por qué eso **no** alcanza para declarar un ganador?

El parámetro poblacional es 1330.72 USD, las estimaciones por diseño son: Conveniencia: 1348.50 USD, Aleatorio Simple (semilla 1): 1336.00, Estratificado (semilla 1): 1287.50 USD, el aleatorio simple quedó más cerca con un +5.28 USD pero no es correcto declararla ganadora ya que se trata de la primera semilla, durante la ejecución de otras semillas, pude observar que se aleja más, como en la semilla 4 que dio 1491.50 USD, es decir, para evaluar correctamente, necesitamos realizar varios intentos y tratar de eliminar sesgos.

**P3.** La muestra por conveniencia también tiene 20 filas. ¿Qué defecto tiene y cómo lo delatas en la composición por ciudad? ¿Se corrige tomando más filas?

Tiene un sesgo de selección, me dí cuenta de esto al notar que al ejecutar se registra como que el 100% de los clientes fueran de Quito al tomar simplemente los primeros 20 registros, omitiendo el resto de ciudades, no se puede corregir tomando más filas, si no cambiando de técnica a una probabilística, donde tomamos 20 registros, si, pero de forma equitativa para lo que nos sugieren los datos.

**P4.** El sorteo aleatorio dio un número distinto en cada semilla. ¿Qué implica esa variabilidad para una empresa que va a decidir con un solo estudio?

Implica que estamos ante incertidumbre de los datos y un error de muestreo, pude comprobar que entre semillas existe una variabilidad de más de 200 USD, en un negocio real no es correcto tomar decisiones basándose en estimaciones hechas al azar, es necesario tener en cuenta el margen de error y realizar intervalos de confianza.

**P5.** ¿Cuándo usarías cada diseño en la práctica? Relaciona cada uno con un uso real (piloto, subgrupos que deben aparecer, conclusión sobre toda la población).

- Muestreo por Conveniencia: Útil al hacer pruebas piloto, validaciones de formato, pruebas en el código, por ejemplo, comprobar que el lenguaje procese correctamente los datos, etc. No deberá ser usado para estimaciones reales de negocio.

- Muestreo Aleatorio Simple: Útil para sacar conclusiones cuando la población total está a la mano y es homogénea.

- Muestreo Estratificado: Útil cuando existen subgrupos o estratos clave que deben tener su respectiva representatividad al realizar mediciones.

## Conclusiones

- Aprendí que el software es muy útil para determinar los tipos de datos de las variables, sin embargo, siempre hay que hacer análisis extra que tomen en cuenta la lógica de negocio y los conceptos estadísticos correspondientes.

- Aprendí que durante diversas mediciones pueden aparecer un sinfín de sesgos, aprender a manejarlos de manera efectiva e incluso evitarlos será siempre la mejor decisión para asegurar la veracidad de mi análisis.

Un consejo para la gerencia puede ser no aprobar estudios ni mediciones basados en una sola estimación, es necesario tener en cuenta otros factores como la variabilidad dentro de los datos, sesgos de selección entre otros. Realizar mediciones extra que nos permitan eliminar estas limitaciones es clave para generar análisis estadísticos claros que aporten de manera positiva al negocio.