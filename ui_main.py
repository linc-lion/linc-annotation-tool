#!/usr/bin/python3

from tkinter import * 
import os
from predict_AI import LINC_detector
from ui_components import buttonFrame, messageFrame, staticFrame

# Model path
model_path = os.path.join('DeployModels', 'body_parts_1.pth')
# Prime model for use
LINC = LINC_detector(model_path)


class WindowRunner(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Init window obj
        self.configure(background='white')
        #self.geometry('800x500')
        
        SF = staticFrame(self)
        SF.grid(sticky="W", column=1, row=0, rowspan = 2)
        SF.grid_propagate(0)
        
        MF = messageFrame(self)
        MF.grid(sticky="W", column=0, row=0)
        MF.grid_propagate(0)
        
        BF = buttonFrame(self,LINC)
        BF.grid(sticky="W", column=0, row=1)
        BF.grid_propagate(0)

if __name__ == "__main__":
    #tk = Tk()
    # Set window
    WR = WindowRunner()  
    # Make window persistent
    WR.mainloop()


