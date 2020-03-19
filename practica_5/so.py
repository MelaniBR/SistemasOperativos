#!/usr/bin/env python

from hardware import*
import log


## emulates a compiled program
class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## now test if last instruction is EXIT
        ## if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


###///////////////////////////////////////////////////////////////////////////////////////////////////
###///////////////////////////////////////////////////////////////////////////////////////////////////









## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)
        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()

    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            ## pop(): extracts (deletes and return) the first element in queue
            pair = self._waiting_queue.pop(0)
            #print(pair)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)

    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)







##  PCB Y PCBTABLE


class PCB():
    ##Es un bloque o registro de datos que contiene diversa información relacionada con el proceso: Estado del proceso
    ##Identificador
    ##Registros del CPU
    ##Prioridad
    ##Estado de Entrada/Salida
    def __init__(self,path,priority):
        self._path = path
        self._pid = 0
        self._pc = 0
        self._state = State.New
        self._processPriority = priority
        self._age = 0
    @property
    def path(self):
        return self._path
#
    @property
    def priority(self):
        if self._age < 5:
            return self._processPriority
        elif self._age < 10 and self._processPriority > 1:
            return self._processPriority - 1
        elif self._age < 15 and self._processPriority > 2:
            return self._processPriority - 2
        elif self._age < 20 and self._processPriority > 3:
            return self._processPriority - 3
        else:
            return 1
    def setPriority(self, priority):
        self._processPriority = priority

    def getAge(self):
        return self._age

    def setAge(self, value):
        self._age = value

    def agePCB(self):
        if self._state == State.Running or self._state == State.Waiting :
            pass
        else:
            self.setAge(self._age + 1)
            log.logger.info("{prg_name} has been aged to age {prg_age}".format(prg_name=self._path, prg_age=self._age))

    @property
    def pid(self):
       return self._pid
#
    # @pid.setter
    def setPid(self, pid):
        self._pid = pid
#
    @property
    def pc(self):
        return self._pc
#
    # @pc.setter
    def setPc(self, pc):
        self._pc = pc
#
    @property
    def state(self):
        return self._state
#
    # @state.setter tiraba error en el NEW
    def changeStateTo(self, state):
        self._state = state


class PCBTable():
    def __init__(self):
        self._PCBTable = dict()
        self._runningPCB = None
        self._PIDCounter = 0

    def get(self, pid):
        return self._PCBTable[pid]

    def add(self, pcb):
        pcb.setPid(self._PIDCounter)
        self._PCBTable[self._PIDCounter] = pcb
        self.getNewPID()

    def remove(self, pid):
        del self._PCBTable[pid]

    @property
    def runningPCB(self):
        return self._runningPCB

    # @runningPCB.setter
    def setRunningPCB(self, pcb):
        self._runningPCB = pcb

    def getNewPID(self):
        self._PIDCounter += 1
    def newAndAdd(self,path, prioridad):
        pcb = PCB(path, prioridad)
        self.add(pcb)
        return pcb
    def allpcbs(self):
        return self._PCBTable.values()



## ESTADO
class State():

        New = "new"
        Running = "running"
        Ready = "ready"
        Waiting = "waiting"
        Terminated = "terminated"



