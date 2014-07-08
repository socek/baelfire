===========
2. Tutorial
===========

2.1 Idea
========
Baelfire is design for making makefile more configurable and have more power.
To achive that, the "makefile" was splitted into 3 parts: recipe, task and
dependency. Recipe is for gathering tasks, other recipes and configuration.
Task is for checking depenency and running. Dependency check what is needed (for
example "was thie file changed since last run").

2.2 Recipe
==========
Minimal Recipe package should containt Recipe class with gather_recipes method,
like this:
>>>
    class ProjectRecipe(Recipe):
        def gather_recipes(self):
            self.add_task(ProjectTask)

I've omited imports, to simplify example. ProjectTask is subclass of Task.
Probably second most used feature is making settings and paths.

>>>
    class ProjectRecipe(Recipe):
        def create_settings(self):
            self.paths['virtualenv_path'] = ['home', 'user', 'venv']
            self.settings['mysettings'] = 'mysetting value'

        def gather_recipes(self):
            self.add_task(ProjectTask)

We have two objects paths and settings. Thoes objects are just smarter dicts and
we can use them in the Task class.
