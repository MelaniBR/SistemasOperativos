import log
class FileSystem():
##es el componente del sistema operativo encargado de administrar y facilitar el
# uso de las memorias periféricas, ya sean secundarias o terciarias.

    def __init__(self):
        self._dictPathProgram = {}
    def write(self, path, prg):
        self._dictPathProgram[path] = prg
        log.logger.info("{this_path} has a new referenced program".format(this_path=path))
    def read(self, path):
        return self._dictPathProgram[path]
    def availablePaths(self): #extra, para la consola
        return self._dictPathProgram.keys()