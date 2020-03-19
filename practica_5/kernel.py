# emulates the core of an Operative System
from interruption import*
from memoryManager import*
from so import*
from dispatcher import*
from loader import*
from fileSystem import*
from DiagramaDeGant import*

class Kernel():

    def __init__(self, scheduler):
        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)
        self._memoryManager = MemoryManager()
        self._fileSystem = FileSystem()
        self._scheduler = scheduler
        self._dispatcher = Dispatcher(self._memoryManager)
        self._loader = Loader(self._memoryManager, self._fileSystem)
        self._pcbTable = PCBTable()
        self._diagramaDeGant = DiagramaDeGant(self._pcbTable)

        ## setup interruption handlers
        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        timeoutHandler = TimeoutInterruptHandler(self)
        HARDWARE.interruptVector.register(TIMEOUT_INTERRUPTION_TYPE, timeoutHandler)

        diagramaHandler = DiagramaInterruptionHandler(self)
        HARDWARE.interruptVector.register(DIAGRAMA_INTERRUPTION_TYPE, diagramaHandler)





    @property
    def memoryManager(self):
        return self._memoryManager
    @property
    def fileSystem(self):
        return self._fileSystem
    @property
    def ioDeviceController(self):
        return self._ioDeviceController
    @property
    def scheduler(self):
        return self._scheduler
    @property
    def dispatcher(self):
        return self._dispatcher
    @property
    def loader(self):
        return self._loader
    @property
    def pcbTable(self):
        return self._pcbTable

    @property
    def diagramaDeGant(self):
        return self._diagramaDeGant





    ## emulates a "system call" for programs execution
    def run(self, path, priority):
        dictNewParam = {'path': path, 'priority': priority} ## nuevo diccionario con el nombre y prioridad
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, dictNewParam) ## Crea interrupciones (en este caso recibe un new)
        HARDWARE.interruptVector.handle(newIRQ) ## guarda el tipo de interrupción y la interrupción

    def __repr__(self):
        return "Kernel "