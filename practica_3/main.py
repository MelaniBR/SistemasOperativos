from hardware import *
from so import *
import log


##
##  MAIN 
##
if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    ## Switch on computer
   

    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    kernel = Kernel()
    prg1 = Program("prg1.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4), ASM.IO(), ASM.CPU(1)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])
    prg4 = Program("test.exe", [ASM.CPU(1), ASM.IO(), ASM.CPU(1)])
    prg5 = Program("test.exe", [ASM.CPU(2)])

    #prg3 = Program("prg3.exe", [ASM.CPU(1)])

    # execute all programs "concurrently"
    #kernel.run(prg1)
    #kernel.run(prg2)
    #kernel.run(prg3)
    kernel.run(prg4)
    kernel.run(prg5)




    ##  create a program
    #prg = Program("test.exe", [ASM.CPU(2), ASM.IO(), ASM.CPU(3), ASM.IO(), ASM.CPU(3)])
    
    # execute the program
    #kernel.run(prg)
    HARDWARE.switchOn()




