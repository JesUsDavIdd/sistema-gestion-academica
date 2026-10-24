"""Pruebas AC2 sin modificar el archivo evaluado.
Uso: python test_actividad_ac2.py ruta/ActividadUni.py
Incluye pruebas funcionales, de integración y comprobaciones estructurales.
"""
import ast
import contextlib
import importlib.util
import inspect
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest

SOURCE = Path(sys.argv.pop(1)) if len(sys.argv) > 1 and sys.argv[1].lower().endswith('.py') else Path(__file__).with_name('ActividadUni.py')
TREE = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
spec = importlib.util.spec_from_file_location('actividad_ac2', SOURCE)
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()) as import_output:
    spec.loader.exec_module(m)


def capture(function, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class RequisitosAC2(unittest.TestCase):
    def setUp(self):
        self.programa = m.ProgramaAcademico('P1', 'Sistemas', 'Ingenieria', 10)
        self.asignatura = m.Asignatura('A1', 'POO', 3, self.programa)
        self.docente = m.Docente('D1', 'Eva', 'eva@uni.edu', 'EMP1', 'Ingenieria', 'Catedra', 12)
        self.estudiante = m.Estudiante('E1', 'Ana', 'ana@uni.edu', 'EST1', self.programa, 2, 4.5)
        self.otro = m.Estudiante('E2', 'Luis', 'luis@uni.edu', 'EST2', self.programa, 3, 4.2)
        self.admin = m.Administrativo('N1', 'Leo', 'leo@uni.edu', 'EMP2', 'Admisiones', 'Analista', 'Diurna')
        self.horario = m.Horario('Lunes', '08:00', '10:00', '302')
        self.grupo = m.GrupoAcademico('G1', self.asignatura, self.docente, 1, self.horario)

    def enroll(self, student=None, group=None):
        return capture((group or self.grupo).matricular_estudiante, student or self.estudiante)

    def test_busqueda_asignatura_existente_devuelve_mismo_objeto(self):
        self.assertIs(m.buscar_asignatura('A1', [self.asignatura]), self.asignatura)

    def test_busqueda_programa_existente_devuelve_mismo_objeto(self):
        self.assertIs(m.buscar_programa('P1', [self.programa]), self.programa)

    def test_busqueda_asignatura_ausente_no_modifica_registros(self):
        registros = [self.asignatura]
        with self.assertRaises(m.AsignaturaNoEncontradaException) as caught:
            m.buscar_asignatura('A99', registros)
        self.assertIn('A99', str(caught.exception))
        self.assertEqual(registros, [self.asignatura])

    def test_busqueda_programa_ausente_no_modifica_registros(self):
        registros = [self.programa]
        with self.assertRaises(m.ProgramaNoEncontradoException) as caught:
            m.buscar_programa('P99', registros)
        self.assertIn('P99', str(caught.exception))
        self.assertEqual(registros, [self.programa])

    def test_busquedas_con_registros_vacios(self):
        with self.assertRaises(m.AsignaturaNoEncontradaException):
            m.buscar_asignatura('A1', [])
        with self.assertRaises(m.ProgramaNoEncontradoException):
            m.buscar_programa('P1', [])

    def test_importacion_no_ejecuta_main(self):
        self.assertEqual(import_output.getvalue(), '')

    def test_persona_abstracta_no_instanciable(self):
        self.assertTrue(inspect.isabstract(m.Persona))
        self.assertIn('realizar_actividad_principal', m.Persona.__abstractmethods__)
        with self.assertRaises(TypeError):
            m.Persona('X', 'Prueba', 'prueba@uni.edu')

    def test_subclase_sin_actividad_permanece_abstracta(self):
        class SinActividad(m.Persona):
            pass
        with self.assertRaises(TypeError):
            SinActividad('X', 'Prueba', 'prueba@uni.edu')

    def test_subclases_concretas_y_comportamientos_polimorficos(self):
        cases = [(self.estudiante, ('Ana', 'Sistemas', '2')),
                 (self.docente, ('Eva', 'Ingenieria')),
                 (self.admin, ('Leo', 'Analista', 'Admisiones'))]
        outputs = []
        for person, expected in cases:
            with self.subTest(clase=type(person).__name__):
                self.assertIsInstance(person, m.Persona)
                self.assertFalse(inspect.isabstract(type(person)))
                self.assertIn('realizar_actividad_principal', type(person).__dict__)
                _, output = capture(person.realizar_actividad_principal)
                outputs.append(output)
                for text in expected:
                    self.assertIn(text, output)
        self.assertEqual(len(set(outputs)), 3)

    def test_informacion_general_y_especializada(self):
        for person, particular in ((self.estudiante, 'EST1'), (self.docente, 'EMP1'), (self.admin, 'Admisiones')):
            _, output = capture(person.mostrar_informacion)
            for text in (person.get_identificacion(), person.get_nombre(), person.get_correo(), particular):
                self.assertIn(text, output)

    def test_grupo_relaciona_objetos_y_registra_datos(self):
        self.assertIs(self.grupo._asignatura, self.asignatura)
        self.assertIs(self.grupo._docente, self.docente)
        self.assertIs(self.grupo._horario, self.horario)
        self.assertEqual(self.grupo._codigo_grupo, 'G1')
        self.assertEqual(self.grupo._capacidad_maxima, 1)
        self.assertEqual(self.grupo._estudiantes_matriculados, [])

    def test_horario_informa_cuatro_datos(self):
        returned, printed = capture(self.horario.mostrar_informacion)
        output = printed + (returned if isinstance(returned, str) else '')
        for text in ('Lunes', '08:00', '10:00', '302'):
            self.assertIn(text, output)

    def test_grupo_informa_relaciones_horario_y_cupo(self):
        _, output = capture(self.grupo.mostrar_informacion_grupo)
        for text in ('G1', 'POO', 'Eva', '0/1', 'Lunes', '08:00', '10:00', '302'):
            self.assertIn(text, output)

    def test_dos_grupos_de_asignatura_con_matriculas_independientes(self):
        otro_grupo = m.GrupoAcademico('G2', self.asignatura, self.docente, 2, self.horario)
        self.enroll()
        self.enroll(self.otro, otro_grupo)
        self.assertIsNot(self.grupo._estudiantes_matriculados, otro_grupo._estudiantes_matriculados)
        self.assertEqual(self.grupo._estudiantes_matriculados, [self.estudiante])
        self.assertEqual(otro_grupo._estudiantes_matriculados, [self.otro])

    def test_primera_matricula_exitosa(self):
        self.enroll()
        self.assertEqual(self.grupo._estudiantes_matriculados, [self.estudiante])

    def test_matricular_dos_estudiantes_dentro_de_capacidad(self):
        grupo = m.GrupoAcademico('G2', self.asignatura, self.docente, 2, self.horario)
        self.enroll(self.estudiante, grupo)
        self.enroll(self.otro, grupo)
        self.assertEqual(grupo._estudiantes_matriculados, [self.estudiante, self.otro])

    def test_duplicado_lanza_excepcion_y_conserva_matricula(self):
        self.enroll()
        with self.assertRaises(m.EstudianteYaMatriculadoException):
            self.enroll()
        self.assertEqual(self.grupo._estudiantes_matriculados, [self.estudiante])

    def test_duplicado_por_codigo_en_otro_objeto(self):
        duplicado = m.Estudiante('E3', 'Ana copia', 'otra@uni.edu', 'EST1', self.programa, 2, 4.5)
        self.enroll()
        with self.assertRaises(m.EstudianteYaMatriculadoException):
            self.enroll(duplicado)
        self.assertEqual(len(self.grupo._estudiantes_matriculados), 1)

    def test_capacidad_excedida_lanza_excepcion_y_conserva_lista(self):
        self.enroll()
        with self.assertRaises(m.GrupoCapacidadExcedidaException):
            self.enroll(self.otro)
        self.assertEqual(self.grupo._estudiantes_matriculados, [self.estudiante])

    def test_retirar_estudiante_matriculado(self):
        self.enroll()
        capture(self.grupo.retirar_estudiante, 'EST1')
        self.assertEqual(self.grupo._estudiantes_matriculados, [])

    def test_retiro_inexistente_en_grupo_vacio(self):
        with self.assertRaises(m.EstudianteNoMatriculadoException):
            capture(self.grupo.retirar_estudiante, 'EST99')

    def test_retiro_inexistente_en_grupo_ocupado(self):
        self.enroll()
        with self.assertRaises(m.EstudianteNoMatriculadoException):
            capture(self.grupo.retirar_estudiante, 'EST99')
        self.assertEqual(self.grupo._estudiantes_matriculados, [self.estudiante])

    def test_retiro_libera_cupo(self):
        self.enroll()
        capture(self.grupo.retirar_estudiante, 'EST1')
        self.enroll(self.otro)
        self.assertEqual(self.grupo._estudiantes_matriculados, [self.otro])

    def test_consulta_grupo_vacio(self):
        _, output = capture(self.grupo.mostrar_estudiantes)
        self.assertIn('G1', output)
        self.assertIn('POO', output)
        self.assertTrue(output.strip())

    def test_consulta_grupo_con_estudiantes(self):
        self.enroll()
        _, output = capture(self.grupo.mostrar_estudiantes)
        self.assertIn('Ana', output)
        self.assertIn('EST1', output)

    def test_cinco_excepciones_propias_con_mensajes(self):
        names = ('EstudianteYaMatriculadoException', 'GrupoCapacidadExcedidaException',
                 'EstudianteNoMatriculadoException', 'AsignaturaNoEncontradaException', 'ProgramaNoEncontradoException')
        classes = [getattr(m, name) for name in names]
        self.assertEqual(len(set(classes)), 5)
        for cls in classes:
            self.assertTrue(issubclass(cls, Exception))
            self.assertTrue(str(cls()).strip())

    def assert_search_raises(self, exception_name):
        found = []
        for function in ast.walk(TREE):
            if not isinstance(function, ast.FunctionDef) or function.name == 'main':
                continue
            for node in ast.walk(function):
                if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call):
                    if isinstance(node.exc.func, ast.Name) and node.exc.func.id == exception_name:
                        found.append(function.name)
        self.assertTrue(found, f'{exception_name}: falta una busqueda real que detecte la situacion y lance la excepcion desde su metodo; raise manual en main() no basta')

    def test_busqueda_asignatura_inexistente_desde_metodo(self):
        self.assert_search_raises('AsignaturaNoEncontradaException')

    def test_busqueda_programa_inexistente_desde_metodo(self):
        self.assert_search_raises('ProgramaNoEncontradoException')

    def test_main_preve_captura_de_cinco_excepciones(self):
        main = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        handled = {n.type.id for n in ast.walk(main) if isinstance(n, ast.ExceptHandler) and isinstance(n.type, ast.Name)}
        expected = {'EstudianteYaMatriculadoException', 'GrupoCapacidadExcedidaException',
                    'EstudianteNoMatriculadoException', 'AsignaturaNoEncontradaException', 'ProgramaNoEncontradoException'}
        self.assertTrue(expected <= handled)

    def test_ejecucion_directa_inicia_demostracion(self):
        env = dict(os.environ, PYTHONIOENCODING='utf-8')
        result = subprocess.run([sys.executable, '-B', str(SOURCE)], capture_output=True, text=True, encoding='utf-8', timeout=10, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip(), 'El archivo termina sin ejecutar main(): la llamada inicial esta dentro de la propia funcion')
        self.assertIn('GRUPOS Y EXCEPCIONES', result.stdout)

    def test_main_no_se_llama_recursivamente(self):
        main = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        calls = [n for n in ast.walk(main) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'main']
        self.assertFalse(calls, 'La proteccion __name__ == __main__ debe estar al nivel del modulo, fuera de main()')

    def test_main_continua_hasta_final_tras_excepciones(self):
        try:
            _, output = capture(m.main)
        except Exception as error:
            self.fail(f'main() se interrumpe con {type(error).__name__}: {error}')
        self.assertIn('La asignatura con', output)
        self.assertIn('PRG-999', output)
        self.assertEqual(output.count('[EXCEPCIÓN CAPTURADA]'), 6)
        self.assertIn('Fin de las pruebas de la Actividad 2.', output)
        self.assertNotIn('Error:', output)


class ComprobacionesAdicionales(unittest.TestCase):
    def test_regresion_ac1_metodos_estudiante(self):
        fields = ('codigo_estudiantil', 'programa', 'semestre', 'promedio_acumulado')
        missing = [prefix + field for prefix in ('get_', 'set_') for field in fields if not callable(getattr(m.Estudiante, prefix + field, None))]
        self.assertEqual(missing, [], f'Metodos publicos de AC1 perdidos: {missing}')

    def test_regresion_ac1_metodos_docente(self):
        fields = ('numero_empleado', 'facultad', 'tipo_contratacion', 'horas_semanales')
        missing = [prefix + field for prefix in ('get_', 'set_') for field in fields if not callable(getattr(m.Docente, prefix + field, None))]
        self.assertEqual(missing, [], f'Metodos publicos de AC1 perdidos: {missing}')

    def test_demostracion_consulta_grupos_y_estudiantes(self):
        main = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        called = {n.func.attr for n in ast.walk(main) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        self.assertTrue({'mostrar_informacion_grupo', 'mostrar_estudiantes'} <= called,
                        'Los metodos existen pero main() no demuestra la consulta de grupos y matriculados')


if __name__ == '__main__':
    unittest.main(verbosity=2)
