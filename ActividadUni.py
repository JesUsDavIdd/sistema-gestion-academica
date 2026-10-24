from abc import ABC, abstractmethod

# Excepciones personalizadas (corresponde a la fase 4):

class EstudianteYaMatriculadoException(Exception):

  def __init__(
      self,
      mensaje="El estudiante ya se encuentra matriculado en este grupo.",
  ):
    super().__init__(mensaje)


class GrupoCapacidadExcedidaException(Exception):

  def __init__(
      self, mensaje="El grupo académico ha alcanzado su capacidad máxima."
  ):
    super().__init__(mensaje)


class EstudianteNoMatriculadoException(Exception):

  def __init__(
      self,
      mensaje=(
          "El estudiante que se desea retirar no está matriculado en el grupo."
      ),
  ):
    super().__init__(mensaje)


class AsignaturaNoEncontradaException(Exception):

  def __init__(self, mensaje="La asignatura buscada no existe en el sistema."):
    super().__init__(mensaje)


class ProgramaNoEncontradoException(Exception):

  def __init__(
      self, mensaje="El programa académico buscado no existe en el sistema."
  ):
    super().__init__(mensaje)

# 1. Clase: Programa academico

class ProgramaAcademico:
    def __init__(self, codigo: str, nombre: str, facultad: str, numero_semestres: int):
        self._codigo = codigo
        self._nombre = nombre
        self._facultad = facultad
        if numero_semestres <= 0:
            raise ValueError("El número de semestres debe ser mayor que cero.")
        self.set_numero_semestres(numero_semestres)

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo: str):
        self._codigo = codigo

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def get_facultad(self):
        return self._facultad

    def set_facultad(self, facultad: str):
        self._facultad = facultad

    def get_numero_semestres(self):
        return self._numero_semestres

    def set_numero_semestres(self, numero_semestres: int):
        
        # Validación de modificación controlada:
        
        if numero_semestres > 0:
            self._numero_semestres = numero_semestres
        else:
            print(f"[ERROR] Número de semestres inválido ({numero_semestres}). Debe ser mayor a 0.")

    def mostrar_informacion(self):
        print(f"Programa: {self._nombre} | Codigo: {self._codigo} | Facultad: {self._facultad} | Semestres: {self._numero_semestres}")


# 2. Clase: Asignatura

class Asignatura:
    def __init__(self, codigo: str, nombre: str, numero_creditos: int, programa_academico: ProgramaAcademico):
        self._codigo = codigo
        self._nombre = nombre
        if numero_creditos <= 0:
            raise ValueError("El número de créditos debe ser mayor que cero.")
        self.set_numero_creditos(numero_creditos)
        self._programa_academico = programa_academico

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo: str):
        self._codigo = codigo

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre: str):
        self._nombre = nombre

    def get_numero_creditos(self):
        return self._numero_creditos

    def set_numero_creditos(self, numero_creditos: int):
        
        # Validación de modificación controlada:
        
        if numero_creditos > 0:
            self._numero_creditos = numero_creditos
        else:
            print(f"[ERROR] Número de creditos invalido ({numero_creditos}). Debe ser mayor a 0.")

    def get_programa_academico(self):
        return self._programa_academico

    def set_programa_academico(self, programa_academico: ProgramaAcademico):
        self._programa_academico = programa_academico

    def mostrar_informacion(self):
        print(f"Asignatura: {self._nombre} ({self._codigo}) | Creditos: {self._numero_creditos} | Programa: {self._programa_academico.get_nombre()}")

#Nueva clase: horario:

class Horario:

  def __init__(
      self, dia: str, hora_inicio: str, hora_finalizacion: str, salon: str
  ):
    self._dia = dia
    self._hora_inicio = hora_inicio
    self._hora_finalizacion = hora_finalizacion
    self._salon = salon

  def mostrar_informacion(self):
    return (
        f"Día: {self._dia} | {self._hora_inicio} - {self._hora_finalizacion} |"
        f" Salón: {self._salon}"
    )

# 3. Clase base: Persona (fase 1: heredar de ABC)

class Persona(ABC):

  def __init__(self, identificacion: str, nombre: str, correo: str):
    self._identificacion = identificacion
    self._nombre = nombre
    if not correo or not correo.strip():
      raise ValueError("El correo de la persona no puede estar vacío.")
    self.set_correo(correo)

  def get_identificacion(self):
    return self._identificacion

  def set_identificacion(self, identificacion: str):
    self._identificacion = identificacion

  def get_nombre(self):
    return self._nombre

  def set_nombre(self, nombre: str):
    self._nombre = nombre

  def get_correo(self):
    return self._correo

  def set_correo(self, correo: str):
      
    # Validación de modificación controlada:
    
    if correo and correo.strip() != "":
      self._correo = correo
    else:
      print(
          f"[ERROR] Correo electrónico invalido para {self._nombre}. No puede"
          " estar vacio."
      )

  def mostrar_informacion(self):
    print(
        f"ID: {self._identificacion} | Nombre: {self._nombre} | Correo:"
        f" {self._correo}"
    )

  @abstractmethod
  def realizar_actividad_principal(self):
    pass

# 4. Subclase: Estudiante (herencia de persona)

class Estudiante(Persona):
    def __init__(self, identificacion: str, nombre: str, correo: str, codigo_estudiantil: str, programa: ProgramaAcademico, semestre: int, promedio_acumulado: float):
        super().__init__(identificacion, nombre, correo)
        self._codigo_estudiantil = codigo_estudiantil
        self._programa = programa
        self._semestre = semestre
        self._promedio_acumulado = promedio_acumulado

    def get_codigo_estudiantil(self):
        return self._codigo_estudiantil

    def set_codigo_estudiantil(self, codigo_estudiantil: str):
        self._codigo_estudiantil = codigo_estudiantil

    def get_programa(self):
        return self._programa

    def set_programa(self, programa: ProgramaAcademico):
        self._programa = programa

    def get_semestre(self):
        return self._semestre

    def set_semestre(self, semestre: int):
        self._semestre = semestre

    def get_promedio_acumulado(self):
        return self._promedio_acumulado

    def set_promedio_acumulado(self, promedio_acumulado: float):
        self._promedio_acumulado = promedio_acumulado

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"   [Estudiante] Codigo: {self._codigo_estudiantil} | Programa: {self._programa.get_nombre()} | Semestre: {self._semestre} | Promedio: {self._promedio_acumulado}")

    def realizar_actividad_principal(self):
        print(f"   -> {self.get_nombre()} esta cursando el semestre {self._semestre} del programa {self._programa.get_nombre()}.")

# 5. Subclase: Docente (herencia de persona)

class Docente(Persona):
    def __init__(self, identificacion: str, nombre: str, correo: str, numero_empleado: str, facultad: str, tipo_contratacion: str, horas_semanales: int):
        super().__init__(identificacion, nombre, correo)
        self._numero_empleado = numero_empleado
        self._facultad = facultad
        self._tipo_contratacion = tipo_contratacion
        self._horas_semanales = horas_semanales

    def get_numero_empleado(self):
        return self._numero_empleado

    def set_numero_empleado(self, numero_empleado: str):
        self._numero_empleado = numero_empleado

    def get_facultad(self):
        return self._facultad

    def set_facultad(self, facultad: str):
        self._facultad = facultad

    def get_tipo_contratacion(self):
        return self._tipo_contratacion

    def set_tipo_contratacion(self, tipo_contratacion: str):
        self._tipo_contratacion = tipo_contratacion

    def get_horas_semanales(self):
        return self._horas_semanales

    def set_horas_semanales(self, horas_semanales: int):
        self._horas_semanales = horas_semanales

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"   [Docente] Num. Empleado: {self._numero_empleado} | Facultad: {self._facultad} | Contrato: {self._tipo_contratacion} | Horas/Semana: {self._horas_semanales}")

    def realizar_actividad_principal(self):
        print(f"   -> {self.get_nombre()} orienta clases en la Facultad de {self._facultad}.")

# 6. Subclase: Administrativo (herencia de persona)

class Administrativo(Persona):
    def __init__(self, identificacion: str, nombre: str, correo: str, numero_empleado: str, dependencia: str, cargo: str, jornada: str):
        super().__init__(identificacion, nombre, correo)
        self._numero_empleado = numero_empleado
        self._dependencia = dependencia
        self._cargo = cargo
        self._jornada = jornada

    def get_numero_empleado(self):
        return self._numero_empleado

    def set_numero_empleado(self, numero_empleado: str):
        self._numero_empleado = numero_empleado

    def get_dependencia(self):
        return self._dependencia

    def set_dependencia(self, dependencia: str):
        self._dependencia = dependencia

    def get_cargo(self):
        return self._cargo

    def set_cargo(self, cargo: str):
        self._cargo = cargo

    def get_jornada(self):
        return self._jornada

    def set_jornada(self, jornada: str):
        self._jornada = jornada

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"   [Administrativo] Num Empleado: {self._numero_empleado} | Dependencia: {self._dependencia} | Cargo: {self._cargo} | Jornada: {self._jornada}")

    def realizar_actividad_principal(self):
        print(f"   -> {self.get_nombre()} se desempeña como {self._cargo} en la dependencia de {self._dependencia}.")

# Nueva clase: GrupoAcademico (corresponde a la fase 2 y 3)

class GrupoAcademico:

  def __init__(
      self,
      codigo_grupo: str,
      asignatura: Asignatura,
      docente: Docente,
      capacidad_maxima: int,
      horario: Horario,
  ):
    if capacidad_maxima <= 0:
      raise ValueError("La capacidad máxima del grupo debe ser mayor que cero.")
    self._codigo_grupo = codigo_grupo
    self._asignatura = asignatura
    self._docente = docente
    self._capacidad_maxima = capacidad_maxima
    self._estudiantes_matriculados = []
    self._horario = horario  # Composición

  def matricular_estudiante(self, estudiante: Estudiante):
    for est in self._estudiantes_matriculados:
      if est.get_codigo_estudiantil() == estudiante.get_codigo_estudiantil():
        raise EstudianteYaMatriculadoException(
            f"El estudiante {estudiante.get_nombre()} ya está matriculado en el"
            f" grupo {self._codigo_grupo}."
        )

    if len(self._estudiantes_matriculados) >= self._capacidad_maxima:
      raise GrupoCapacidadExcedidaException(
          f"No se pudo matricular a {estudiante.get_nombre()}. El grupo"
          f" {self._codigo_grupo} alcanzó su capacidad máxima"
          f" ({self._capacidad_maxima})."
      )

    self._estudiantes_matriculados.append(estudiante)
    print(
        f"[MATRÍCULA EXITOSA] Estudiante {estudiante.get_nombre()} matriculado"
        f" en el grupo {self._codigo_grupo}."
    )

  def retirar_estudiante(self, codigo_estudiantil: str):
    for est in self._estudiantes_matriculados:
      if est.get_codigo_estudiantil() == codigo_estudiantil:
        self._estudiantes_matriculados.remove(est)
        print(
            f"[RETIRO EXITOSO] Estudiante con código {codigo_estudiantil}"
            f" retirado del grupo {self._codigo_grupo}."
        )
        return

    raise EstudianteNoMatriculadoException(
        f"El estudiante con código {codigo_estudiantil} no se encuentra"
        " matriculado en este grupo."
    )

  def mostrar_estudiantes(self):
    print(
        f"Estudiantes matriculados en el grupo {self._codigo_grupo}"
        f" ({self._asignatura.get_nombre()}):"
    )
    if not self._estudiantes_matriculados:
      print("   (No hay estudiantes matriculados)")
    for est in self._estudiantes_matriculados:
      print(
          f"   - {est.get_nombre()} (Código: {est.get_codigo_estudiantil()})"
      )

  def mostrar_informacion_grupo(self):
    print(
        f"Grupo: {self._codigo_grupo} | Asignatura:"
        f" {self._asignatura.get_nombre()} | Docente:"
        f" {self._docente.get_nombre()}"
    )
    print(
        f"   Capacidad:"
        f" {len(self._estudiantes_matriculados)}/{self._capacidad_maxima} |"
        f" Horario: {self._horario.mostrar_informacion()}"
    )

# Búsquedas sobre los objetos registrados en el sistema.

def buscar_asignatura(codigo: str, asignaturas: list):
    for asignatura in asignaturas:
        if asignatura.get_codigo() == codigo:
            return asignatura
    raise AsignaturaNoEncontradaException(
        f"La asignatura con código '{codigo}' no existe en el sistema."
    )


def buscar_programa(codigo: str, programas: list):
    for programa in programas:
        if programa.get_codigo() == codigo:
            return programa
    raise ProgramaNoEncontradoException(
        f"El programa académico con código '{codigo}' no existe en el sistema."
    )


# Programa principal: demostración y pruebas de funcionamiento

def main():
    print("==================================================")
    print("      SISTEMA DE GESTIÓN ACADEMICA - PRUEBAS     ")
    print("==================================================\n")

    # 1. Creación de programas académicos y asignaturas
    
    print("--- 1. Creación de Programas Académicos y Asignaturas ---")
    prog_sistemas = ProgramaAcademico("PRG01", "Ingenieria de Sistemas", "Ciencias e Ingenierias", 10)
    prog_derecho = ProgramaAcademico("PRG02", "Derecho", "Ciencias Juridicas", 10)

    programas = [prog_sistemas, prog_derecho]

    prog_sistemas.mostrar_informacion()
    prog_derecho.mostrar_informacion()

    asig_poo = Asignatura("ASI01", "Programación Orientada a Objetos", 3, prog_sistemas)
    asig_constitucional = Asignatura("ASI02", "Derecho Constitucional", 4, prog_derecho)

    asignaturas = [asig_poo, asig_constitucional]

    asig_poo.mostrar_informacion()
    asig_constitucional.mostrar_informacion()
    print()

    # 2. Creación de al menos 6 personas (2 estudiantes, 2 docentes, 2 administrativos)
    
    print("--- 2. Creación de Instancias de Personas ---")
    estudiante1 = Estudiante("1001", "Carlos Gómez", "carlos.gomez@um.edu.co", "EST-01", prog_sistemas, 1, 4.5)
    estudiante2 = Estudiante("1002", "María Rodríguez", "maria.rodriguez@um.edu.co", "EST-02", prog_derecho, 3, 4.2)

    docente1 = Docente("2001", "Dr. Alejandro López", "alejandro.lopez@um.edu.co", "DOC-01", "Ciencias e Ingenierias", "Tiempo Completo", 40)
    docente2 = Docente("2002", "Dra. Sofía Martínez", "sofia.martinez@um.edu.co", "DOC-02", "Ciencias Juridicas", "Cátedra", 12)

    admin1 = Administrativo("3001", "Fernando Torres", "fernando.torres@um.edu.co", "ADM-01", "Admisiones", "Coordinador", "Diurna")
    admin2 = Administrativo("3002", "Laura Morales", "laura.morales@um.edu.co", "ADM-02", "Recursos Humanos", "Analista", "Completa")
    print("6 Personas creadas con éxito.\n")

    # 3. Pruebas de encapsulamiento y validaciones:
    
    print("--- 3. Pruebas de Encapsulamiento y Validaciones ---")
    print("Modificación valida de correo:")
    estudiante1.set_correo("carlos.gomez_actualizado@um.edu.co")
    print(f"Nuevo correo de {estudiante1.get_nombre()}: {estudiante1.get_correo()}\n")

    print("Intentando asignar 3 valores invalidos:")
    # Prueba invalida 1: Correo vacio
    estudiante1.set_correo("")
    # Prueba invalida 2: Semestres menores o iguales a cero
    prog_sistemas.set_numero_semestres(0)
    # Prueba invalida 3: Creditos menores o iguales a cero
    asig_poo.set_numero_creditos(-2)
    print()

    # 4. Coleccion heterogenea y recorrido polimorfico
    print("--- 4. Reporte General de Personas (Demostración de Polimorfismo) ---")
    coleccion_personas = [estudiante1, estudiante2, docente1, docente2, admin1, admin2]

    # Unico ciclo para recorrer la colección sin condicionales por tipo (Polimorfismo)
    for persona in coleccion_personas:
        persona.mostrar_informacion()
        persona.realizar_actividad_principal()
        print("-" * 55)

#Pruebas para la actividad 2:

    print("\n==================================================")
    print(" PRUEBAS DE LA ACTIVIDAD N°2 (GRUPOS Y EXCEPCIONES)")
    print("==================================================\n")

# Prueba: Demostrar que Persona no se puede instanciar directamente
    print("--- Prueba: Intentar instanciar la clase Persona directamente ---")
    try:
        _ = Persona("9999", "Prueba", "prueba@um.edu.co")
    except TypeError as e:
        print(f"[EXCEPCIÓN CAPTURADA] Persona es abstracta: {e}\n")

    # Creación de Grupos Académicos y Horarios
    horario1 = Horario("Lunes", "08:00", "10:00", "Lab 302")
    horario2 = Horario("Martes", "10:00", "12:00", "Aula 204")

    grupo1 = GrupoAcademico(
        "G01", asig_poo, docente1, capacidad_maxima=1, horario=horario1
    )
    grupo2 = GrupoAcademico(
        "G02", asig_constitucional, docente2, capacidad_maxima=2, horario=horario2
    )

    # Pruebas de Matrícula y Excepciones
    print("--- Pruebas de Matrícula ---")
    try:
        grupo1.matricular_estudiante(estudiante1)
    except (EstudianteYaMatriculadoException, GrupoCapacidadExcedidaException) as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    # Intentar matricular duplicado
    try:
        grupo1.matricular_estudiante(estudiante1)
    except EstudianteYaMatriculadoException as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    # Intentar superar capacidad máxima
    try:
        grupo1.matricular_estudiante(estudiante2)
    except GrupoCapacidadExcedidaException as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    print()

    # Pruebas de Retiro
    print("--- Pruebas de Retiro ---")
    try:
        grupo1.retirar_estudiante("EST-99")
    except EstudianteNoMatriculadoException as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    try:
        grupo1.retirar_estudiante("EST-01")
    except EstudianteNoMatriculadoException as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    print()

    # Pruebas de Búsqueda Inexistente
    print("--- Pruebas de Búsqueda de Asignaturas y Programas ---")
    try:
        buscar_asignatura("ASI-999", asignaturas)
    except AsignaturaNoEncontradaException as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    try:
        buscar_programa("PRG-999", programas)
    except ProgramaNoEncontradoException as e:
        print(f"[EXCEPCIÓN CAPTURADA] {e}")

    # Consulta de los dos grupos, con y sin estudiantes matriculados.
    grupo2.matricular_estudiante(estudiante2)
    print("\n--- Información de los grupos y sus estudiantes ---")
    grupo1.mostrar_informacion_grupo()
    grupo1.mostrar_estudiantes()
    grupo2.mostrar_informacion_grupo()
    grupo2.mostrar_estudiantes()

    print("\n--- Búsquedas de registros existentes ---")
    buscar_asignatura("ASI01", asignaturas).mostrar_informacion()
    buscar_programa("PRG01", programas).mostrar_informacion()
    print("\nFin de las pruebas de la Actividad 2.")


if __name__ == "__main__":
    main()