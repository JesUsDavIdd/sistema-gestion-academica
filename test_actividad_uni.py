"""Pruebas contra el enunciado. No modifica el archivo evaluado.

Ejecutar: python test_actividad_uni.py [ruta/ActividadUni.py]
Los accesores siguen get_/set_, la convención del código recibido.
Los casos de construcción inválida son comprobaciones de robustez adicionales.
"""
import ast
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else Path('C:/Users/becer/Downloads/ActividadUni.py')
spec = importlib.util.spec_from_file_location('actividad_evaluada', SOURCE)
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()) as import_output:
    spec.loader.exec_module(m)


def capture(function, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class Requisitos(unittest.TestCase):
    def setUp(self):
        self.programa = m.ProgramaAcademico('P1', 'Sistemas', 'Ingenieria', 10)
        self.asignatura = m.Asignatura('A1', 'POO', 3, self.programa)
        self.persona = m.Persona('101', 'Ana', 'ana@uni.edu')
        self.estudiante = m.Estudiante('102', 'Luis', 'luis@uni.edu', 'E1', self.programa, 2, 4.5)
        self.docente = m.Docente('103', 'Eva', 'eva@uni.edu', 'D1', 'Ingenieria', 'Catedra', 12)
        self.administrativo = m.Administrativo('104', 'Leo', 'leo@uni.edu', 'N1', 'Admisiones', 'Analista', 'Diurna')

    def test_importacion_sin_ejecutar_main(self):
        self.assertEqual(import_output.getvalue(), '')

    def test_constructores_inicializan_todos_los_datos(self):
        expected = {
            'programa': dict(codigo='P1', nombre='Sistemas', facultad='Ingenieria', numero_semestres=10),
            'asignatura': dict(codigo='A1', nombre='POO', numero_creditos=3, programa_academico=self.programa),
            'persona': dict(identificacion='101', nombre='Ana', correo='ana@uni.edu'),
            'estudiante': dict(identificacion='102', nombre='Luis', correo='luis@uni.edu', codigo_estudiantil='E1', programa=self.programa, semestre=2, promedio_acumulado=4.5),
            'docente': dict(identificacion='103', nombre='Eva', correo='eva@uni.edu', numero_empleado='D1', facultad='Ingenieria', tipo_contratacion='Catedra', horas_semanales=12),
            'administrativo': dict(identificacion='104', nombre='Leo', correo='leo@uni.edu', numero_empleado='N1', dependencia='Admisiones', cargo='Analista', jornada='Diurna'),
        }
        for name, fields in expected.items():
            obj = getattr(self, name)
            for field, value in fields.items():
                with self.subTest(clase=type(obj).__name__, atributo=field):
                    self.assertEqual(getattr(obj, '_' + field), value)

    def test_herencia_y_sobrescritura(self):
        for cls in (m.Estudiante, m.Docente, m.Administrativo):
            with self.subTest(clase=cls.__name__):
                self.assertTrue(issubclass(cls, m.Persona))
                for method in ('mostrar_informacion', 'realizar_actividad_principal'):
                    self.assertIn(method, cls.__dict__)
                    self.assertIsNot(getattr(cls, method), getattr(m.Persona, method))
                for method in ('get_identificacion', 'set_identificacion', 'get_nombre', 'set_nombre', 'get_correo', 'set_correo'):
                    self.assertIs(getattr(cls, method), getattr(m.Persona, method))

    def test_main_demuestra_los_siete_puntos_minimos(self):
        originals = {name: getattr(m, name) for name in ('ProgramaAcademico', 'Asignatura', 'Estudiante', 'Docente', 'Administrativo')}
        created = {name: [] for name in originals}
        events = []

        def factory(name):
            def create(*args, **kwargs):
                obj = originals[name](*args, **kwargs)
                created[name].append(obj)
                for method in ('mostrar_informacion', 'realizar_actividad_principal'):
                    if hasattr(obj, method):
                        original = getattr(obj, method)
                        def record(original=original, obj=obj, method=method):
                            events.append((obj, method))
                            return original()
                        setattr(obj, method, record)
                return obj
            return create

        with contextlib.ExitStack() as stack:
            for name in originals:
                stack.enter_context(patch.object(m, name, factory(name)))
            _, output = capture(m.main)
        self.assertGreaterEqual(len(created['ProgramaAcademico']), 1)
        self.assertGreaterEqual(len(created['Asignatura']), 1)
        people = []
        for name in ('Estudiante', 'Docente', 'Administrativo'):
            self.assertGreaterEqual(len(created[name]), 2)
            people.extend(created[name])
        people_events = [(obj, method) for obj, method in events if isinstance(obj, m.Persona)]
        self.assertEqual(people_events, [(obj, method) for obj in people for method in ('mostrar_informacion', 'realizar_actividad_principal')])
        self.assertEqual(output.count('[ERROR]'), 3)
        self.assertEqual(created['Estudiante'][0].get_correo(), 'carlos.gomez_actualizado@um.edu.co')
        self.assertEqual(created['ProgramaAcademico'][0].get_numero_semestres(), 10)
        self.assertEqual(created['Asignatura'][0].get_numero_creditos(), 3)

    def test_main_un_ciclo_sin_condicionales_por_tipo(self):
        tree = ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
        loops = [node for node in ast.walk(main) if isinstance(node, (ast.For, ast.While))]
        self.assertEqual(len(loops), 1)
        loop = loops[0]
        self.assertIsInstance(loop, ast.For)
        self.assertFalse(any(isinstance(node, (ast.If, ast.IfExp, ast.Match)) for node in ast.walk(loop)))
        calls = [node for node in ast.walk(loop) if isinstance(node, ast.Call)]
        self.assertFalse(any(isinstance(node.func, ast.Name) and node.func.id in ('type', 'isinstance') for node in calls))
        for method in ('mostrar_informacion', 'realizar_actividad_principal'):
            matches = [call for call in calls if isinstance(call.func, ast.Attribute) and call.func.attr == method]
            self.assertEqual(len(matches), 1)
            self.assertIsInstance(matches[0].func.value, ast.Name)
            self.assertEqual(matches[0].func.value.id, loop.target.id)


def accessor_case(object_name, field, new_value):
    def test(self):
        obj = getattr(self, object_name)
        getter = getattr(obj, 'get_' + field, None)
        setter = getattr(obj, 'set_' + field, None)
        self.assertTrue(callable(getter), f'{type(obj).__name__}: falta método de consulta para {field}')
        self.assertTrue(callable(setter), f'{type(obj).__name__}: falta método de modificación para {field}')
        self.assertEqual(getter(), getattr(obj, '_' + field))
        value = m.ProgramaAcademico('P2', 'Derecho', 'Juridica', 8) if new_value == '__programa__' else new_value
        setter(value)
        self.assertEqual(getter(), value)
    return test


for object_name, fields in {
    'persona': dict(identificacion='999', nombre='Bea', correo='bea@uni.edu'),
    'programa': dict(codigo='P2', nombre='Derecho', facultad='Juridica', numero_semestres=1),
    'asignatura': dict(codigo='A2', nombre='Calculo', numero_creditos=1, programa_academico='__programa__'),
    'estudiante': dict(codigo_estudiantil='E2', programa='__programa__', semestre=3, promedio_acumulado=4.7),
    'docente': dict(numero_empleado='D2', facultad='Ciencias', tipo_contratacion='Completo', horas_semanales=40),
    'administrativo': dict(numero_empleado='N2', dependencia='Biblioteca', cargo='Coordinador', jornada='Nocturna'),
}.items():
    for field, value in fields.items():
        setattr(Requisitos, f'test_accesores_{object_name}_{field}', accessor_case(object_name, field, value))


def rejection_case(object_name, field, invalid_values):
    def test(self):
        obj = getattr(self, object_name)
        getter, setter = getattr(obj, 'get_' + field), getattr(obj, 'set_' + field)
        previous = getter()
        for value in invalid_values:
            with self.subTest(valor=repr(value)):
                _, output = capture(setter, value)
                self.assertEqual(getter(), previous, 'La modificación inválida debe conservar el valor anterior')
                self.assertTrue(output.strip(), 'Debe informar al usuario del rechazo')
    return test


for object_name, field, invalid in (
    ('persona', 'correo', ('', '   ', '\t\n')),
    ('programa', 'numero_semestres', (0, -1)),
    ('asignatura', 'numero_creditos', (0, -1)),
):
    setattr(Requisitos, f'test_rechazo_{field}', rejection_case(object_name, field, invalid))


def output_case(object_name, method, expected):
    def test(self):
        _, output = capture(getattr(getattr(self, object_name), method))
        for text in expected:
            with self.subTest(dato=text):
                self.assertIn(text, output)
    return test


for name, expected in {
    'persona': ('101', 'Ana', 'ana@uni.edu'),
    'programa': ('P1', 'Sistemas', 'Ingenieria', 'Semestres: 10'),
    'asignatura': ('A1', 'POO', 'Creditos: 3', 'Sistemas'),
    'estudiante': ('102', 'Luis', 'luis@uni.edu', 'E1', 'Sistemas', 'Semestre: 2', 'Promedio: 4.5'),
    'docente': ('103', 'Eva', 'eva@uni.edu', 'D1', 'Ingenieria', 'Catedra', 'Horas/Semana: 12'),
    'administrativo': ('104', 'Leo', 'leo@uni.edu', 'N1', 'Admisiones', 'Analista', 'Diurna'),
}.items():
    setattr(Requisitos, f'test_informacion_{name}', output_case(name, 'mostrar_informacion', expected))
for name, expected in {
    'estudiante': ('Luis', 'semestre 2', 'Sistemas'),
    'docente': ('Eva', 'orienta clases', 'Ingenieria'),
    'administrativo': ('Leo', 'Analista', 'Admisiones'),
}.items():
    setattr(Requisitos, f'test_actividad_{name}', output_case(name, 'realizar_actividad_principal', expected))


class RobustezAdicional(unittest.TestCase):
    """El enunciado no prescribe el mecanismo de rechazo del constructor.

    Se acepta ValueError. Si retorna un objeto, sus métodos deben funcionar
    y sus datos deben respetar las mismas restricciones.
    """
    def check_constructor(self, factory, getter, valid):
        try:
            obj, _ = capture(factory)
        except ValueError:
            return
        try:
            value = getattr(obj, getter)()
            capture(obj.mostrar_informacion)
        except AttributeError as error:
            self.fail(f'Constructor devuelve objeto incompleto: {error}')
        self.assertTrue(valid(value), 'Constructor devuelve un objeto con valor inválido')

    def test_constructor_correo_vacio(self):
        self.check_constructor(lambda: m.Persona('1', 'Ana', ''), 'get_correo', lambda x: bool(x.strip()))

    def test_constructor_semestres_cero(self):
        self.check_constructor(lambda: m.ProgramaAcademico('P', 'Sistemas', 'Ingenieria', 0), 'get_numero_semestres', lambda x: x > 0)

    def test_constructor_creditos_cero(self):
        programa = m.ProgramaAcademico('P', 'Sistemas', 'Ingenieria', 10)
        self.check_constructor(lambda: m.Asignatura('A', 'POO', 0, programa), 'get_numero_creditos', lambda x: x > 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
