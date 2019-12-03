#!/usr/bin/python3

from tkinter import * 
import os
from predict_AI import LINC_detector
from ui_components import buttonFrame, messageFrame, rightFrame

class WindowRunner(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.kill_prog = False              # Kill switch
        self.are_threads = None                # Check for any threads
        # Init window obj
        self.configure(background='white')
        #self.geometry('800x500')
        self.winfo_toplevel().title("LINC")

        RF = rightFrame(self)
        RF.grid(sticky="W", column=1, row=0, rowspan = 2)
        RF.grid_propagate(0)
        
        MF = messageFrame(self)
        MF.grid(sticky="W", column=0, row=0)
        MF.grid_propagate(0)
        
        BF = buttonFrame(self)
        BF.grid(sticky="W", column=0, row=1)
        BF.grid_propagate(0)

        self.graceful_exit() # Start checking exit

    def graceful_exit(self):
        if self.kill_prog: 
            if self.are_threads != None:
                if not self.are_threads.isAlive():
                    print(f"graceful: Thread Alive?: {self.are_threads.isAlive()}"
                            +" ...destroying now")
                    self.destroy()
                    return
            else:
                print("graceful:destroying now")
                self.destroy()
                return
        self.after(1, self.graceful_exit)


if __name__ == "__main__":
    # Set window
    WR = WindowRunner()
    # Make window persistent
    WR.mainloop()


