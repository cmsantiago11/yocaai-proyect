# Manual y Estándar de trabajo colaborativo

# YoKaAi Project

Versión 1.0

**Objetivo**: Eliminar la ambigüedad. Si no está escrito aquí, se discute en el *Pull Request*. Si está escrito aquí, se cumple sin excepción.

## Flujo de trabajo

*Regla de Oro: Nunca se hace Push directo a main.*

### Frecuencia y Protocolo de Sincronización

- Comando `pull`: cada momento antes de escribir una sola línea. Y cada vez que retomes el código después de 2 horas.

De no hacerlo se corre el riesgo de un conflicto masivo.

El responsable del conflicto debe intentar resolverlo él mismo antes de pedir ayuda, de lo contrario avisar con tiempo para
evitar que se generen más conflictos.

- Comando `commit`: cada bloque lógico funcional, con un máximo de 150 líneas cambiadas o agregadas.

No se debe hacer un solo *commit* cuando se han modificado más de tres archivos.
Si el *commit* no compila o rompe alguna función del código, se revierte ese *commit* sin preguntar.

Para devolver un commit se ejecuta el siguiente comando:

`git reset --soft HEAD~1`

Para devolver un solo *commit*, si se quiere devolver más atrás se ubica la cantidad de pasos a devolver después
la instrucción *HEAD~*

`git reset --soft HEAD~3`

Por ejemplo, en este comando se devuelve tres *commits* hacia atrás.

> Estos pasos son solamente si no se ha hecho *push* a la rama donde se esta trabajando.

Si ya se hizo el *commit* deberá ejecutar:

`git revert [COMMIT ID]`

Esto creará un nuevo commit que deshace los cambios del commit especificado.
En otras palabras el estado de tu proyecto después de ejecutar git revert será 
como si el commit especificado nunca hubiese ocurrido, pero sin eliminar el 
historial de cambios.

- Comando `push`: al finalizar la tarea. Aunque el código no funcione como al principio se planeo, debe estar en el servidor del controloador de cambios.

- Comando `merge`: debe realizarse cuando la tarea haya finalizado completamente y preferiblemente, con todos los integrantes del proyecto.

#### Plantilla de checklist para un *pull request*

#####  Descripción Corta

Explicar que hacen los cambios, esto, en pocas líneas.

#####  Checklist de Calidad (Obligatorio marcar todas)

- [ ] Probado.
- [ ] No contiene claves de API, tokens o contraseñas en texto plano.
- [ ] El código está comentado **solo donde es necesario**.
- [ ] He resuelto los conflictos con `main` antes de abrir este PR.

#####  Evidencia Visual

Obervar el entorno gráfico que generado por el código y determinar si es compatible con lo planeado o debe sufrir modificaciones.
En caso de que deba modificarse, indicar cuales cambios deben realizarse en el entorno.

## Estándar para el código

En este apartado se encontrará la forma en que el proyecto será o es codificado. La legibilidad es prioridad absoluta.

### Convenciones de nomenclaturas

| Tipo de identificador | Convención | Ejemplo Correcto | Incorrecto |
| :--- | :--- | :--- | :--- |
| Variables y funciones | `snake_case` | `user_count`, `calculate_total()` | `userCount`, `CalculateTotal` |
| Clases | `PascalCase` | `EmailSender`, `UserProfile` | `email_sender`, `userProfile` |
| Constantes globales | `UPPER_SNAKE_CASE` | `MAX_RETRIES = 3` | `maxRetries` |
| Variables booleanas | Prefijo `is_`, `has_`, `can_` | `is_active`, `has_permission` | `active`, `flag` |
| Atributos/Métodos privados | Prefijo `_` simple | `_cache`, `_internal_helper()` | N/A |


### Manejo de los logs del sistema

Regla primordial, la función `print()` es para depuración local efímera. *logging* es para comprender el sistema en producción.
A continuación la configuración básica:

~~~
import logging
import sys

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,  # Usar DEBUG solo en entorno local
    format=LOG_FORMAT,
    )
~~~

> Para una mejor configuración ver los niveles de *logs* [aquí.][https://docs.python.org/es/3/howto/logging-cookbook.html]

### Comentarios

Como principio manejaremos la filosofía: *El código explica cómo. Los comentarios explican por qué.*

Ejemplos:

~~~
# ❌ MAL (Código muerto y obvio)
# total = total + 10
total = total + 10  # sumamos 10 al total

# ✅ BIEN (Explicación del contexto)
# Añadimos 100ms de pausa porque la API externa tiene un límite estricto
# de 10 peticiones por segundo y devuelve HTTP 429 si se supera.
time.sleep(0.1)
~~~

## Documentación

> Esta será construida en la medida que se avance el código.




