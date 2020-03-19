from hardware import*
class MemoryManager:

    def __init__(self):
        self._frameSize = HARDWARE.mmu.frameSize
        self._freeFrames = []  # todos los frames(marcos) libres
        self._dictPageTables = {}
        self.initFreeFrames()
        log.logger.info("{prg_name} marcos que tengo  ".format(prg_name=(len(self._freeFrames))))

    def initFreeFrames(self):
        ## inicia los marcos libres
         for i in range(0, ((HARDWARE.memory.size // self._frameSize) - 1)):

             self._freeFrames.append(i)

    def allocFrames(self, n):
        ## Una lista de todos los marcos libres
        retf = []
        for i in range(0, n):
            nextFrame = self._freeFrames.pop(0)
            retf.append(nextFrame)
        return retf

    def putPageTable(self, pid, pageTable):
        ## Realiza una pagina
        self._dictPageTables[pid] = pageTable

    def getPageTable(self, pid):
        ## retorna una pagina con el pid indicado en el parametro
        return self._dictPageTables[pid]


    def freePageTable(self, pid):
           # Retorna una nueva lista de frames libres eliminando el que con tiene el pid pasado por parametro
        framesToFree = self._dictPageTables.pop(pid).getFrames() # la lista con los marcos que quedan libres
        for frame in framesToFree:
            self._freeFrames.append(frame)  ## agrega los libres a freeFrames
        log.logger.info("{prg_name} Se elimino memoria {prg_dir}  ".format(prg_name=(len(self._freeFrames)),prg_dir= pid ))
        return True

    def getFreeMemory(self):
        return (len(self._freeFrames)) * self._frameSize