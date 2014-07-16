import os
import sys
import shutil
from jinja2 import Environment

from mock import MagicMock
from soktest import TestCase

from baelfire.template import TemplateTask


class TemplateTaskExample(TemplateTask):

    def get_output_file(self):
        dirname = os.path.dirname(self.template_absolute_path())
        return os.path.join(dirname, 'myfile')

    def get_template_path(self):
        return 'template.jinja2'

    def generate_data(self):
        data = super().generate_data()
        data['mytest'] = 'success'
        return data


class TemplateTaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.recipe = MagicMock()
        self.template = TemplateTaskExample()
        self.template.assign_recipe(self.recipe)

    def test_module(self):
        """Should return mock module, because recipe is a MagicMock."""
        expected_module = sys.modules['mock']
        self.assertEqual(expected_module, self.template.module())

    def test_template_absolute_path(self):
        """Should return absolute path for a template."""
        self.add_mock_object(self.template, 'module')
        self.mocks['module'].return_value.__file__ = '/main/child'
        path = self.template.template_absolute_path()
        self.assertEqual('/main/templates/template.jinja2', path)

    def test_generate_dependencies(self):
        """Should add FileChanged dependency for template file and this file.
        """
        self.add_mock_object(self.template, 'module')
        self.mocks['module'].return_value.__file__ = '/main/child'

        self.template.generate_dependencies()

        dependency = self.template.dependencies[0]
        self.assertEqual(
            ['/main/templates/template.jinja2'], dependency.filenames)

        dependency = self.template.dependencies[1]
        self.assertEqual([__file__], dependency.filenames)

    def test_jinja_when_new(self):
        """Should generate new jinja2 envoritment."""
        self.assertEqual(None, self.template._jinja)

        env = self.template.jinja()

        self.assertEqual(self.template._jinja, env)
        self.assertEqual(Environment, type(env))

    def test_jinja_when_exists(self):
        """Should return jinja2 envoritment generated before."""
        self.template._jinja = MagicMock()

        env = self.template.jinja()

        self.assertEqual(self.template._jinja, env)

    def test_generate_data(self):
        """Should return dict with settings and paths from recipe."""
        data = self.template.generate_data()

        self.assertEqual(self.recipe.settings, data['settings'])
        self.assertEqual(self.recipe.paths, data['paths'])

    def test_make(self):
        """Should generate template from given file."""
        try:
            self.add_mock_object(
                self.template, 'module', return_value=sys.modules[__name__])
            self.template.templates_dir = 'testdir'
            test_path = os.path.dirname(self.template.template_absolute_path())
            os.mkdir(test_path)
            template = open(self.template.template_absolute_path(), 'w')
            template.write("This is sample {{mytest}} template.")
            template.close()

            self.template.make()

            _file = open(self.template.get_output_file(), 'r')
            generated_data = _file.read()
            _file.close()

            self.assertEqual(
                'This is sample success template.', generated_data)

        finally:
            shutil.rmtree(test_path, True)

    def test_generate_dependencies_when_check_template_is_false(self):
        """Should not add any dependency when check_template is setted to
        False."""
        self.template.check_template = False
        self.template.generate_dependencies()
        self.assertEqual([], self.template.dependencies)
