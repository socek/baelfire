class VisualizatorChooser(object):

    def __init__(self):
        self.visualizators = {}
        self.generate_visualizators()

    def add_visualizator(self, url, visualizator):
        self.visualizators[url] = visualizator

    def choose(self, url, report, *args, **kwargs):
        visualizator = self.visualizators.get(url, self.DEFAULT)
        return visualizator(url, report, *args, **kwargs)
