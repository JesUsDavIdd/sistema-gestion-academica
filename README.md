# Sistema de Gestión Académica

Proyecto académico de la Universidad de Manizales, Facultad de Ciencias e Ingenierías, desarrollado en Python para aplicar los conceptos de programación orientada a objetos.

## Integrantes

- Juan Jose Lopera Morales
- Jesus David Becerra Tascon

## Descripción general

El sistema representa la información básica de la comunidad universitaria mediante las clases `Persona`, `Estudiante`, `Docente` y `Administrativo`. También incluye las clases `ProgramaAcademico` y `Asignatura` para organizar los programas y las asignaturas que pertenecen a ellos.

El programa principal crea dos programas académicos, dos asignaturas y seis personas: dos estudiantes, dos docentes y dos administrativos. Demuestra la consulta de información, una modificación válida de correo, el rechazo de tres modificaciones inválidas y la generación de un reporte mediante una colección de personas.

Los datos se almacenan en memoria durante la ejecución. Esta versión funciona en consola y no utiliza una base de datos.

## Estructura de los archivos

El proyecto reúne el código recibido, este documento y las pruebas realizadas:

```text
proyecto/
├── .gitignore              # Archivos temporales excluidos de Git
├── ActividadUni.py          # Clases del sistema y función principal main()
├── README.md                # Descripción e instrucciones del proyecto
├── test_actividad_uni.py     # Pruebas unitarias con unittest
└── resultado_pruebas.txt    # Resultado de la validación del código revisado
```

Las clases y el programa principal están definidos en un único archivo, `ActividadUni.py`. El archivo de pruebas valida ese mismo sistema; no implementa otra versión del proyecto.

## Requisitos y ejecución

Se requiere Python 3.10 o superior para ejecutar tanto el sistema como las pruebas proporcionadas. No se necesitan paquetes externos.

Desde una terminal, ubicarse en la carpeta del proyecto y ejecutar:

```bash
python ActividadUni.py
```

En Windows, si Python está disponible mediante el lanzador `py`, se puede usar:

```powershell
py ActividadUni.py
```

La ejecución muestra los programas y las asignaturas, una actualización válida de correo, los mensajes de rechazo de valores inválidos y el reporte de las seis personas.

### Pruebas unitarias

Con los archivos de la estructura anterior en la misma carpeta, ejecutar:

```bash
python test_actividad_uni.py ActividadUni.py
```

En Windows también se puede ejecutar:

```powershell
py test_actividad_uni.py ActividadUni.py
```

Las pruebas verifican los datos inicializados, los métodos de consulta y modificación, las validaciones, la herencia, la sobrescritura, la información presentada, las actividades particulares y el recorrido polimórfico del programa principal.

## Aplicación de la programación orientada a objetos

### Herencia

`Estudiante`, `Docente` y `Administrativo` heredan de `Persona`. La clase base reúne la identificación, el nombre y el correo electrónico, así como los métodos comunes para consultar y modificar esos datos. Las subclases llaman a `super().__init__()` para inicializar la información compartida y agregan sus propios atributos.

### Sobrescritura

Las tres subclases sobrescriben `mostrar_informacion()` para presentar los datos generales de la persona y los datos de su rol. Cada implementación llama primero a `super().mostrar_informacion()`.

También sobrescriben `realizar_actividad_principal()`: el estudiante informa el programa y semestre que cursa; el docente indica la facultad en la que orienta clases; y el administrativo informa su cargo y dependencia.

### Polimorfismo

En `main()`, la lista `coleccion_personas` contiene estudiantes, docentes y administrativos. Un único ciclo llama a `mostrar_informacion()` y `realizar_actividad_principal()` sobre cada objeto. Python ejecuta la implementación correspondiente a su clase, sin condicionales que consulten el tipo de persona.

### Encapsulamiento y validaciones

Los atributos usan el prefijo `_` para indicar que son de uso interno. `Persona`, `ProgramaAcademico` y `Asignatura` incluyen métodos `get_` y `set_` para consultar y modificar sus datos. El código rechaza un correo vacío, un número de semestres menor o igual a cero y un número de créditos menor o igual a cero. En estas modificaciones inválidas, informa el error y conserva el valor anterior.

## Estado de la validación

La revisión del código recibido ejecutó **43 pruebas: 28 aprobaron y 15 fallaron**. Se identificaron los siguientes pendientes:

- Doce pruebas fallaron porque los atributos propios de `Estudiante`, `Docente` y `Administrativo` no tienen métodos de consulta y modificación.
- Tres pruebas adicionales de robustez fallaron porque un correo vacío, cero semestres o cero créditos en el constructor dejan objetos incompletos que producen `AttributeError` al consultar sus datos.

El prefijo `_` indica una convención de uso interno en Python, pero no bloquea las asignaciones directas. Los problemas identificados no se han corregido en el código revisado.

## Uso de inteligencia artificial

Se utilizó OpenAI Codex como apoyo para revisar el código y resolver algunos errores.

