from hardware import*
class Dispatcher():

    def __init__(self, memoryManager):
        self._memoryManager = memoryManager

    def save(self, pcb):
        pcb.setPc(HARDWARE.cpu.pc)
        HARDWARE.cpu.pc = -1


    def load(self, pcb):
        pageTablePCB = self._memoryManager.getPageTable(pcb.pid)
        HARDWARE.cpu.pc = pcb.pc
        HARDWARE.timer.reset()
        HARDWARE.mmu.resetTLB()
        for i in pageTablePCB.getPages():
            HARDWARE.mmu.setPageFrame(i, pageTablePCB.getFrame(i))
