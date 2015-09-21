from mock import MagicMock

from ..parrented import parrented


class TestParrented(object):

    @property
    def parented(self):
        def method(self):
            return self
        return method

    def test_parrented_method_without_parent(self):
        """
        parrented should return own method if no parrent set.
        """
        obj = MagicMock()
        obj.parent = None
        method = parrented(self.parented)

        assert method(obj) == obj

    def test_parrented_method_with_parent(self):
        """
        parrented should return parent method if parrent is set.
        """
        parent = MagicMock()
        obj = MagicMock()
        obj.parent = parent
        method = parrented(self.parented)

        assert method(obj) == parent.method.return_value
        parent.method.assert_called_once_with(obj)

    def test_parrented_method_property(self):
        """
        parrented should return parent property.
        """
        parent = MagicMock()
        parent.method = 15
        obj = MagicMock()
        obj.parent = parent
        method = parrented(self.parented)

        assert method(obj) == parent.method
