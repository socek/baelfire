from mock import MagicMock
from soktest import TestCase

from baelfire.template import TemplateTask


class TemplateTaskExample(TemplateTask):

    def get_template_path(self):
        return 'template.jinja2'


class TemplateTaskTest(TestCase):

    def setUp(self):
        super().setUp()
        self.recipe = MagicMock()
        self.template = TemplateTaskExample()
        self.template.assign_recipe(self.recipe)

    def test_simple(self):
        self.template.get_env()
