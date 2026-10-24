# Documento de Decisiones de Diseño

**Sistema de Gestión Académica — Actividad Colaborativa N.º 2**

Universidad de Manizales

Facultad de Ciencias e Ingenierías

**Integrantes**

- Juan Jose Lopera Morales
- Jesus David Becerra Tascon

**Fecha:** 24 de octubre de 2026

## Introducción

La segunda actividad amplía el sistema de gestión académica de la primera entrega. El propósito es incorporar grupos académicos y operaciones de matrícula sin sustituir las clases y comportamientos existentes. Para ello se utilizan una clase abstracta, relaciones entre objetos, composición y excepciones personalizadas.

Este documento explica las decisiones que se reflejan en `ActividadUni.py`. Se conservaron los métodos de consulta y modificación de la primera versión y se mantuvo el reporte polimórfico de las personas. La validación se realiza mediante la demostración de `main()` y pruebas automatizadas.

## Descripción general de la solución

El sistema mantiene las clases `ProgramaAcademico`, `Asignatura`, `Persona`, `Estudiante`, `Docente` y `Administrativo`. Se agregan `Horario` y `GrupoAcademico`, cinco excepciones personalizadas y las funciones `buscar_asignatura()` y `buscar_programa()`.

`main()` crea los objetos de ejemplo y demuestra las operaciones. Las colecciones de programas, asignaturas y estudiantes se almacenan en memoria. Esta decisión permite concentrarse en los conceptos de programación orientada a objetos solicitados, sin introducir una base de datos ni otras dependencias.

## Desarrollo de las decisiones

### Persona como clase abstracta

`Persona` reúne los datos que comparten todos los integrantes de la comunidad universitaria: identificación, nombre y correo. Sin embargo, una persona vinculada debe tener un rol concreto para determinar su actividad principal. Por esa razón hereda de `ABC` y marca `realizar_actividad_principal()` con `@abstractmethod`.

Esta decisión impide construir una persona genérica sin comportamiento definido. La restricción la aplica Python: intentar crear `Persona(...)` produce `TypeError`. La demostración captura ese error y continúa. Una nueva subclase también tendrá que implementar el método antes de poder instanciarse.

### Responsabilidades de las subclases

`Estudiante`, `Docente` y `Administrativo` llaman a `super().__init__()` para inicializar los datos compartidos. Cada una implementa la actividad propia de su rol: el estudiante informa el programa y el semestre que cursa; el docente indica la facultad donde orienta clases; y el administrativo informa su cargo y dependencia.

Las tres clases también sobrescriben `mostrar_informacion()`. Primero reutilizan la presentación de los datos comunes y luego agregan los particulares. Los métodos de consulta y modificación de esos atributos se conservan o completan para que otras partes del sistema no necesiten acceder a ellos directamente. Por ejemplo, el grupo usa `get_codigo_estudiantil()` para identificar a un estudiante.

### Relaciones del grupo académico

`GrupoAcademico` tiene un código, capacidad máxima, una asignatura, un docente, una lista de estudiantes y un horario. La asignatura y el docente se reciben como objetos ya creados, lo que permite consultar su información y mantener la identidad de esos objetos. No se guardan únicamente nombres o códigos aislados.

La lista de estudiantes se crea dentro de cada grupo. Así, matricular o retirar a una persona en un grupo no modifica la lista de otro. Una asignatura puede ser utilizada por varios grupos, cada uno con su propia capacidad, matrícula y organización horaria.

La matrícula compara códigos estudiantiles. Dos objetos diferentes con el mismo código se consideran el mismo estudiante para evitar matrículas duplicadas. Primero se verifica esa condición y luego la capacidad. El retiro busca el código recibido y elimina solamente al estudiante encontrado.

### Composición entre grupo y horario

`Horario` contiene día, hora de inicio, hora de finalización y salón. El grupo integra un objeto de esa clase en su atributo `_horario`, y `mostrar_informacion_grupo()` utiliza su información para presentar cuándo y dónde se desarrolla el grupo.

La relación corresponde a un grupo que contiene un horario, no a una especialización: un grupo académico no es un horario. Por ello no existe herencia entre esas clases. En la demostración se construye un horario distinto para cada grupo y se suministra al constructor del grupo al organizarlo.

La integración se realiza pasando el objeto al constructor, en lugar de usar una cadena de texto con todos sus datos. El programa no impone una regla de destrucción automática del horario ni impide que otro código conserve una referencia; la composición se representa mediante la inclusión del objeto dentro de la organización del grupo.

### Excepciones en matrícula, retiro y búsqueda

Las excepciones se definen como clases que heredan de `Exception`. Cada situación se detecta donde corresponde y se comunica a `main()`, que decide cómo presentarla sin detener la demostración.

| Excepción | Situación controlada | Lugar donde se genera |
| --- | --- | --- |
| `EstudianteYaMatriculadoException` | El código del estudiante ya aparece en la matrícula del grupo. | `GrupoAcademico.matricular_estudiante()` |
| `GrupoCapacidadExcedidaException` | No quedan cupos disponibles. | `GrupoAcademico.matricular_estudiante()` |
| `EstudianteNoMatriculadoException` | El código solicitado para retiro no está en el grupo. | `GrupoAcademico.retirar_estudiante()` |
| `AsignaturaNoEncontradaException` | Ninguna asignatura registrada tiene el código buscado. | `buscar_asignatura()` |
| `ProgramaNoEncontradoException` | Ningún programa registrado tiene el código buscado. | `buscar_programa()` |

Las funciones de búsqueda recorren las listas recibidas. Si encuentran el código, devuelven el mismo objeto; si terminan sin encontrarlo, lanzan la excepción. Esto evita simular una búsqueda mediante un `raise` escrito directamente en el programa principal.

Los rechazos de matrícula se producen antes de modificar la lista, de modo que una matrícula fallida conserva los datos anteriores. Después de cada excepción prevista, `main()` continúa con la siguiente operación. Además, los constructores rechazan con `ValueError` un correo vacío, semestres o créditos no positivos y capacidad no positiva, para evitar objetos inicialmente incompletos.

### Conservación del polimorfismo y de la primera entrega

El reporte original mantiene una colección con estudiantes, docentes y administrativos. Un único ciclo invoca `mostrar_informacion()` y `realizar_actividad_principal()` sin preguntar a qué clase pertenece cada objeto. Convertir `Persona` en abstracta no cambia esa forma de recorrer las personas; exige que los objetos concretos aporten la implementación necesaria.

La evolución conserva los métodos agregados en AC1, incluidos los de `Estudiante` y `Docente`. El historial del repositorio permite consultar la primera versión en el commit `d7e117e9cb25632b707961328318fa7dcaef0215`. Los cambios de AC2 se incorporan después de ese commit, sin reescribirlo.

### Validación y límites de esta versión

Las pruebas verifican la abstracción, las relaciones con objetos, las matrículas válidas y duplicadas, la capacidad, el retiro, las consultas y las búsquedas. También comprueban que el programa principal inicia y llega al final después de capturar las excepciones previstas. Las pruebas de la primera actividad se adaptaron para usar una subclase concreta al comprobar los datos comunes de `Persona`.

La versión se validó con 78 pruebas aprobadas. Esto cubre los escenarios evaluados y no significa que se hayan probado todas las entradas posibles. Esta entrega no guarda datos entre ejecuciones, no controla cruces de horarios ni aplica reglas sobre pertenencia del estudiante al programa de la asignatura, porque esos procesos no fueron solicitados en la actividad.

## Conclusiones

La clase abstracta evita representar personas sin un rol definido y mantiene el comportamiento común mediante herencia. Las relaciones entre objetos permiten que los grupos utilicen las asignaturas, docentes y estudiantes existentes, mientras que `Horario` organiza la información de tiempo y lugar de cada grupo.

Las excepciones separan la detección del problema de su presentación al usuario y permiten continuar después de las situaciones previstas. La conservación de los métodos anteriores y las pruebas de ambas actividades permiten revisar la evolución del mismo sistema.

## Uso de inteligencia artificial

Se utilizó OpenAI Codex como apoyo para revisar y corregir el código, preparar la documentación y generar y ejecutar pruebas.
