# 1. Clase: Programa academico

class ProgramaAcademico:
    def __init__(self, codigo: str, nombre: str, facultad: str, numero_semestres: int):
        self._codigo = codigo
        self._nombre = nombre
        self._facultad = facultad
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


# 3. Clase base: Persona

class Persona:
    def __init__(self, identificacion: str, nombre: str, correo: str):
        self._identificacion = identificacion
        self._nombre = nombre
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
            print(f"[ERROR] Correo electrónico invalido para {self._nombre}. No puede estar vacio.")

    def mostrar_informacion(self):
        print(f"ID: {self._identificacion} | Nombre: {self._nombre} | Correo: {self._correo}")

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

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"   [Administrativo] Num Empleado: {self._numero_empleado} | Dependencia: {self._dependencia} | Cargo: {self._cargo} | Jornada: {self._jornada}")

    def realizar_actividad_principal(self):
        print(f"   -> {self.get_nombre()} se desempeña como {self._cargo} en la dependencia de {self._dependencia}.")

# Programa principal: (demostracion y pruebas de funcionamiento)

def main():
    print("==================================================")
    print("      SISTEMA DE GESTIÓN ACADEMICA - PRUEBAS     ")
    print("==================================================\n")

    # 1. Creación de programas académicos y asignaturas
    
    print("--- 1. Creación de Programas Académicos y Asignaturas ---")
    prog_sistemas = ProgramaAcademico("PRG01", "Ingenieria de Sistemas", "Ciencias e Ingenierias", 10)
    prog_derecho = ProgramaAcademico("PRG02", "Derecho", "Ciencias Juridicas", 10)

    prog_sistemas.mostrar_informacion()
    prog_derecho.mostrar_informacion()

    asig_poo = Asignatura("ASI01", "Programación Orientada a Objetos", 3, prog_sistemas)
    asig_constitucional = Asignatura("ASI02", "Derecho Constitucional", 4, prog_derecho)

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

if __name__ == "__main__":
    main()