from hardware import*
from pageTable import*
class Loader():

    def __init__(self,memoryManeger,fileSystem):
        self._fileSystem = fileSystem
        self._frameSize = HARDWARE.mmu.frameSize
        self._memoryManager = memoryManeger

    def load(self, pcb):
        program = self._fileSystem.read(pcb.path)
        framedInstructions = self.splitInstructions(program.instructions) # lo divide para que entre en el marco

        availableFrames = self._memoryManager.allocFrames(len(framedInstructions)) ## longitud de los marcos libres l
        log.logger.info("The program at {prg_path} is going to use the next frames: {frame_list}".format(prg_path=pcb.path,frame_list=availableFrames ))

        newPageTable = PageTable() # Creamos la PageTable del proceso y lo guarda en memoria

        for n in range(0, len(availableFrames)):
            newPageTable.addPF(n, availableFrames[n])

        self._memoryManager.putPageTable(pcb.pid, newPageTable)
        self.loadPages(framedInstructions, availableFrames)
        log.logger.info(HARDWARE.memory)  ## Tira el cuadro en consola

    def loadPages(self, instructions, listFrames):

        for n in range(0, len(instructions)):
            frameID = listFrames[n]
            self.loadPage(instructions[n], frameID)

    def loadPage(self, pageInstructions, frameID):
        frameBaseDir = frameID * self._frameSize
        for index in range(0, len(pageInstructions)):
            HARDWARE.memory.write(frameBaseDir + index, pageInstructions[index])

    def splitInstructions(self, instructions):
        ##Recibe una lista de instrucciones y las divide pror la cantidad de marcos
        return list(chunks(instructions, self._frameSize))

    ## FUNCIONES AUXILIARES UNIVERSALES
def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]