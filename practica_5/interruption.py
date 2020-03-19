
from DiagramaDeGant import*
from so import*
import log

class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

    def runNextProgram(self):
        #hay algo en lista de espera
        if not self.kernel.scheduler.isEmptyRQ() :
            #obtiene el sig
            nextPCB = self.kernel.scheduler.next()
            self.correrPrograma(nextPCB)

    def agregarAReadyQueue(self,pcb):
        pcb.changeStateTo(State.Ready)
        self.kernel.scheduler.add(pcb)
        log.logger.info("{prg_name} se ha agregado a la ReadyQueue".format(prg_name=pcb.path))



    def correrPrograma(self,pcb):
        self.kernel.dispatcher.load(pcb)
        pcb.changeStateTo(State.Running)
        self.kernel.pcbTable.setRunningPCB(pcb)
        log.logger.info("{prg_name} is now running".format(prg_name=pcb.path))


    def runOrSetReady(self,pcbAgregar):
        pcbRunning = self.kernel.pcbTable.runningPCB
        if self.kernel.pcbTable.runningPCB is None:
            self.correrPrograma(pcbAgregar)
        elif self.kernel.scheduler.mustExpropiate(pcbAgregar,pcbRunning):
             self.kernel.dispatcher.save(pcbRunning)
             self.agregarAReadyQueue(pcbRunning)
             self.correrPrograma(pcbAgregar)
        else:
            self.agregarAReadyQueue(pcbAgregar)

class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        killPCB = self.kernel.pcbTable.runningPCB
        self.kernel.dispatcher.save(killPCB)

        killPCB.changeStateTo(State.Terminated)

        self.kernel.pcbTable.setRunningPCB(None)

        self.kernel.memoryManager.freePageTable(killPCB.pid)

        log.logger.info("{prg_name} has been handled by ioDevice".format(prg_name=killPCB.path))

        self.runNextProgram()


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        inPCB = self.kernel.pcbTable.runningPCB
        self.kernel.dispatcher.save(inPCB)
        inPCB.changeStateTo(State.Waiting)
        self.kernel.pcbTable.setRunningPCB(None)
        self.kernel.ioDeviceController.runOperation(inPCB, operation)
        log.logger.info(self.kernel.ioDeviceController)
        log.logger.info("{prg_name} is being handled by ioDevice".format(prg_name=inPCB.path))
        self.runNextProgram()


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        outPCB = self.kernel.ioDeviceController.getFinishedPCB()
        log.logger.info(self.kernel.ioDeviceController)
        log.logger.info("{prg_name} is being handled by ioDevice".format(prg_name= outPCB.path))
        self.runOrSetReady(outPCB)


class TimeoutInterruptHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        timeoutPCB = self.kernel.pcbTable.runningPCB

        self.kernel.dispatcher.save(timeoutPCB)
        timeoutPCB.changeStateTo(Ready())
        self.kernel.scheduler.add(timeoutPCB)
        log.logger.info("{prg_name} has been timed out and added to ReadyQueue".format(prg_name=timeoutPCB.path))
        self.kernel.pcbTable.setRunningPCB(None)
        log.logger.info("Timer has been resetted")
        self.runNextProgram()

class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        dictNewParam = irq.parameters
        priority = dictNewParam['priority']
        path = dictNewParam['path']
        if path in self.kernel.fileSystem.availablePaths():
            self.agregarAlPCB(path,priority)

        else:
            log.logger.info("#  ERROR 002: failed to find a referenced program at    --> {r_path}".format(r_path=path))

    def agregarAlPCB(self,path,priority):
        # si la longitud de instrucciones es mas grande que la memoria libre
        if (len(self.kernel.fileSystem.read(path).instructions)) > self.kernel.memoryManager.getFreeMemory():
            log.logger.info("#  ERROR 001: not enough memory to load the required program at    --> {this_path}".format(
                this_path=path))
            # error no hay suficiente memoria para cargar
        else:

            nuevoPcb = self.kernel.pcbTable.newAndAdd( path, priority)
            self.kernel.loader.load(nuevoPcb)
            self.kernel.diagramaDeGant.addPCB(nuevoPcb)
            log.logger.info("Program at {prg_name} has been loaded".format(prg_name=path))
            self.runOrSetReady(nuevoPcb)

class DiagramaInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        tick = irq.parameters["TICK"]
        self.kernel.diagramaDeGant.collect(tick)