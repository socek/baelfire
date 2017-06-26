from mock import MagicMock

from baelfire.dependencies.dependency import AlwaysTrue
from baelfire.dependencies.dependency import Dependency
from baelfire.dependencies.dependency import AlwaysFalse


class TestAlwaysTrue(object):

    def test_should_build(self):
        """
        AlwaysTrue.should_rebuild should always return True.
        """
        assert AlwaysTrue().should_build() is True


class TestAlwaysFalse(object):

    def test_should_build(self):
        """
        AlwaysFalse.should_rebuild should always return False.
        """
        assert AlwaysFalse().should_build() is False


class TestDependency(object):

    def test_settings(self):
        """
        .settings should return parent settings.
        """
        parent = MagicMock()
        dependency = Dependency()
        dependency.set_parent(parent)

        assert dependency.settings is parent.settings
