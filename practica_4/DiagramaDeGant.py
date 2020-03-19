from hardware import *
from so import *
import log

class DiagramaDeGant():

    def __init__(self, pcbTable):
        ## tiene pcbTable pasado por parametro, ademas de una nueva lista vacia de pcb y otra de ticks
        self._pcbTable = pcbTable
        self._pcbs = []
        self._ticks = []

    def addPCB(self, pcb):
        self._pcbs.append([pcb.pid])
        for i in range(0, len(self._ticks)):
            self._pcbs[pcb.pcbId].append(" ")

    def collect(self, tick):
        self._ticks.append(tick)
        for pcb in self._pcbTable.allpcbs():
            self.addStatusToList(pcb)
        log.logger.info(tabulate(self._pcbs, self._ticks, tablefmt='fancy_grid'))

    def addStatusToList(self, pcb):
        pid = pcb.pid
        if pcb.state == "running":
            self._pcbs[pid].append("{PC}".format(PC= HARDWARE.cpu.pc))
        if pcb.state == "ready":
            self._pcbs[pid].append(".")
        if pcb.state == "waiting":
            self._pcbs[pid].append("I/O")
        if pcb.state == "terminated":
            self._pcbs[pid].append("#")
