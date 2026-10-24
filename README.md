# Sistema de Gestión Académica

Universidad de Manizales — Facultad de Ciencias e Ingenierías.

## Integrantes

- Juan Jose Lopera Morales
- Jesus David Becerra Tascon

## Descripción

La Actividad Colaborativa 2 amplía el mismo sistema construido en la Actividad 1. Conserva los programas, asignaturas y tipos de personas, y agrega la gestión de grupos académicos, sus horarios, la matrícula y el retiro de estudiantes.

El sistema funciona en consola y guarda los datos en memoria durante la ejecución. No utiliza una base de datos ni paquetes externos.

## Archivos

```text
sistema-gestion-academica/
├── ActividadUni.py          # Clases, búsquedas y demostración principal
├── README.md               # Descripción e instrucciones
├── DECISIONES_DISENO.md     # Justificación de las decisiones de AC2
├── test_actividad_uni.py    # Pruebas anteriores adaptadas a Persona abstracta
├── test_actividad_ac2.py    # Pruebas de abstracción, grupos y excepciones
└── .gitignore
```

## Ejecución

Se requiere Python 3.10 o superior para ejecutar el sistema y todas las pruebas. Desde la carpeta del proyecto:

```bash
python ActividadUni.py
```

En Windows también puede utilizarse `py` en lugar de `python`.

La demostración crea programas, asignaturas, dos estudiantes, dos docentes y dos administrativos. Mantiene el reporte polimórfico de la primera actividad. Luego muestra que `Persona` no se puede instanciar, crea dos horarios y dos grupos, realiza matrículas y retiros y controla los casos de estudiante duplicado, falta de cupo, retiro inexistente y búsquedas sin resultado. Al final consulta ambos grupos y realiza búsquedas válidas.

Los mensajes de excepciones capturadas son parte de los casos de prueba; la ejecución continúa después de ellos y termina con el mensaje `Fin de las pruebas de la Actividad 2.`.

## Pruebas automatizadas

Para ejecutar las pruebas de ambas actividades:

```bash
python -m unittest discover -v
```

Para ejecutar solamente las pruebas de AC2:

```bash
python test_actividad_ac2.py
```

La versión corregida se validó con **78 pruebas aprobadas**. Las pruebas incluyen la ejecución completa del programa, la conservación de los métodos de la primera actividad, las búsquedas válidas e inválidas, los límites de matrícula y las excepciones requeridas.

Las pruebas de la clase base usan una subclase concreta exclusiva de los tests. Esto permite comprobar sus atributos sin permitir la creación directa de `Persona` en el sistema.

## Conceptos aplicados

**Herencia:** `Estudiante`, `Docente` y `Administrativo` reutilizan la identificación, el nombre, el correo y los métodos comunes definidos en `Persona`.

**Abstracción:** `Persona` hereda de `ABC` y declara `realizar_actividad_principal()` con `@abstractmethod`. Cada subclase concreta implementa ese método.

**Sobrescritura:** las tres subclases personalizan `mostrar_informacion()` y `realizar_actividad_principal()` según su rol.

**Polimorfismo:** una lista contiene los tres tipos de persona y un único ciclo invoca los mismos métodos, sin consultar el tipo del objeto.

**Composición:** cada grupo integra un objeto `Horario` con el día, las horas y el salón que describen cuándo y dónde se desarrolla. En la demostración se crea un horario distinto para cada grupo. Un grupo contiene un horario; no es una clase de horario ni hereda de él.

**Relaciones entre objetos:** `GrupoAcademico` recibe objetos existentes de `Asignatura` y `Docente` y guarda una lista de objetos `Estudiante`. Las búsquedas devuelven los objetos registrados y no solo sus nombres.

**Excepciones:** las situaciones de matrícula, retiro y búsqueda se detectan en sus respectivos métodos o funciones, que lanzan las excepciones personalizadas. `main()` las captura y muestra sus mensajes.

## Versiones y colaboración

La versión de AC1 corresponde al commit `d7e117e9cb25632b707961328318fa7dcaef0215`. Su contenido se conserva en el historial; los cambios de AC2 se agregan en commits posteriores. La etiqueta requerida para identificar la versión de la segunda entrega se denomina `Entrega_AC2`.

Cada integrante debe aportar al menos un commit significativo relacionado con AC2. Los aportes de AC1 no sustituyen este requisito. Si se realizan nuevas mejoras antes de entregar, deben probarse y acordarse en el equipo antes de cerrar la versión final.

## Decisiones de diseño y uso de IA

La justificación de la abstracción, las relaciones, la composición y el manejo de excepciones, junto con la declaración del apoyo de IA utilizado, se encuentra en [DECISIONES_DISENO.md](DECISIONES_DISENO.md).
