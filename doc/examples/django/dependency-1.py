from os import walk
from os.path import getmtime
from os.path import join

from baelfire.dependencies import FileChanged


class MigrationsChanged(FileChanged):

    migrations_dirname = 'migrations'

    def _map_mtime(self, root):
        """
        convert filename into full path with mtime
        """
        def make(file):
            path = join(root, file)
            mtime = getmtime(path)
            return path, mtime
        return make

    @property
    def path(self):
        # list of files to check
        checkfiles = []

        for root, dirs, files in walk(self.paths.get('src')):
            # check only paths ending with "migrations"
            if root.endswith(self.migrations_dirname):
                # filter for only  '.py' files
                files = filter(lambda file: file.endswith('.py'), files)

                checkfiles += list(map(self._map_mtime(root), files))

        # get the newest file, and return its full path, so the output_file will be compared only to one file
        return max(checkfiles, key=lambda obj: obj[1])[0]
