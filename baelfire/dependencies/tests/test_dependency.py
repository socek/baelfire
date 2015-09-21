from mock import MagicMock

from ..dependency import AlwaysRebuild
from ..dependency import Dependency
from ..dependency import NoRebuild


class TestAlwaysRebuild(object):

    def test_should_build(self):
        """
        AlwaysRebuild.should_rebuild should always return True.
        """
        assert AlwaysRebuild().should_build() is True


class TestNoRebuild(object):

    def test_should_build(self):
        """
        NoRebuild.should_rebuild should always return False.
        """
        assert NoRebuild().should_build() is False


class TestDependency(object):

    def test_settings(self):
        """
        .settings should return parent settings.
        """
        parent = MagicMock()
        dependency = Dependency()
        dependency.set_parent(parent)

        assert dependency.settings is parent.settings
