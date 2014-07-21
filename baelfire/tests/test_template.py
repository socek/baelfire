import os
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

    @property
    def paths(self):
        return self._paths


class TemplateTaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.recipe = MagicMock()
        self.recipe.recipe_paths = {}
        self.template = TemplateTaskExample()
        self.template._paths = {}
        self.template.assign_recipe(self.recipe)

    def test_generate_dependencies(self):
        """Should add FileChanged dependency for template file and this file.
        """
        self.template.recipe_paths['templates'] = '/main/templates'
        self.template.generate_dependencies()

        dependency = self.template.dependencies[0]
        self.assertEqual(
            ['/main/templates/template.jinja2'], dependency.filenames)

        dependency = self.template.dependencies[1]
        self.assertEqual([__file__], dependency.filenames)

    def test_jinja_when_new(self):
        """Should generate new jinja2 envoritment."""
        self.assertEqual(None, self.template._jinja)
        self.template.recipe_paths['templates'] = 'templates'

        env = self.template.jinja()

        self.assertEqual(self.template._jinja, env)
        self.assertEqual(Environment, type(env))

    def test_jinja_when_exists(self):
        """Should return jinja2 envoritment generated before."""
        self.template._jinja = MagicMock()

        env = self.template.jinja()

        self.assertEqual(self.template._jinja, env)

    def test_generate_data(self):
        """Should return dict with settings and paths from recipe. Paths is set
        to {} due the 'mock' of it."""
        data = self.template.generate_data()

        self.assertEqual(self.recipe.settings, data['settings'])
        self.assertEqual({}, data['paths'])

    def test_make(self):
        """Should generate template from given file."""
        try:
            self.template._paths = {}
            self.recipe.recipe_paths = {
                'templates': os.path.abspath(
                    os.path.join(os.getcwd(), 'testdir'))}
            test_path = self.template.recipe_paths['templates']
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
