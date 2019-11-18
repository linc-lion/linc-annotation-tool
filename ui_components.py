from tkinter import * 
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import time
import os
from predict_AI import LINC_detector
from ui_vocFileUtil import create_voc
from ui_fileManager import transfer_files, get_image_files


# Static components
class staticFrame(Frame):
    def __init__(self, root):
        Frame.__init__(self, root, width=310, height=500)
        self.configure(bg='white')
        # Make components
        self.img_label = self.load_logo()
        self.info = self.info_label()        
        self.place_components()


    def place_components(self):
        # Place widgets
        self.img_label.grid(sticky='E', column=0, rowspan=1, row=0)
        self.info.grid(sticky='W', column=0, rowspan=1, row=2)


    def load_logo(self):
        # Load static logo
        image = Image.open("logo.png")
        image.thumbnail((300,300), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(image)
        img_label = Label(self, image=render, bg="white")
        img_label.image = render
        return img_label


    def info_label(self):
        # Static info directions
        info = Text(self, width=37,
                height=60, relief=FLAT, 
                highlightthickness=0, wrap='word') 
        info.tag_configure('tag-left',justify='left')
        info.insert(END,
        "1. Enter the date of the sighting, "+ 
        "in the format dd_mm_yyyy using "+ 
        "underscores.\n\n"+ 
        "2. Select the directory with lion images"+ 
        "and then click transfer to copy files with"+
        "clean file names to new sub director.\n\n"+
        "3. Use the annotation button"+
        "to start the auto-annotationer."+ 
        "Threshold level is the confidence threshold, " +
        "lower=less confident results are returned.",'tag-left') 
        info.configure(state=DISABLED, bg='white')
        return info


class messageFrame(Frame):
    # Used to display messages
    def __init__(self, root):
        Frame.__init__(self, root, width=500, height=300)
        self.root = root
        self.green = '#1fc401'
        self.configure(bg='white')
        self.root.messages = self.make_message_space()
        self.place_components()


    def place_components(self):
        the_row = 0
        # [0] ir root message
        self.root.messages[0].grid(sticky='W', column=0, 
                                row=the_row+0, columnspan=1)
        for i, mes in enumerate(self.root.messages):
            mes.grid(sticky='W', column=0,row=(the_row+i+1), 
                    columnspan=1)


    def make_message_space(self):
        the_width = 50
        the_width_2 = 60
        messages = [Label(self, bg="black",
                                relief=FLAT,font=("Courier","12", "bold"), 
                                highlightthickness=0, anchor="w", 
                                width=the_width)]
        # Default message
        messages[0].configure(text='Welcome....',fg=self.green) 
        # Message steps
        for i in range(1, 4):
            messages.append(Label(self, bg="white", relief=FLAT, 
                                font=("Courier",10),
                                anchor="w", highlightthickness=0, 
                                width=the_width_2))
        return messages
    

class buttonFrame(Frame):
    # Implements main buttons and flow
    def __init__(self, root, model):
        Frame.__init__(self, root, width=500, height=250)
        self.configure(bg='white')
        # Vars
        self.image_directory = None
        self.new_path = 'LINCImages'    # Sub directory name to be created
        self.new_path_abs = None        # Absolute path to new dir
        self.root = root                # Root window container
        self.green = '#1fc401'
        self.the_date = None
        self.LINC = model
        self.threshold = .8
        # Make buttons
        self.buttons, self.button_labels = self.make_buttons()
        self.status_bar = self.make_status_bar()
        self.date_box, self.date_button = self.make_date()
        # Place components
        self.place_components()
    

    def place_components(self):
        # Place in window
        off_col = 0
        current_row = 0
        # Date button
        self.date_button.grid(sticky='W', column=(0+off_col), row=current_row)
        self.date_box.grid(sticky='W', column=1, row=current_row, padx=100)
        current_row += 1 # Inc row
        
        # Main buttons
        for i, (button, b_label) in enumerate(zip(self.buttons, self.button_labels)):
            button.grid(sticky='W', column=(0+off_col), row=current_row)
            b_label.grid(sticky='W', column=(1+off_col), row=current_row)
            current_row += 1    # Inc row

        # Place status bar
        self.status_bar.grid(sticky='W', column=0, row=current_row, 
                            columnspan=2, pady=0, padx=0)


    def make_date(self):
        color = "#053bfc"
        color_a = "#fc6602"
        color_f = 'white'
        the_width = 20
        # Make date button
        date_b = Button(self, text="Submit Date", command=self.get_date, 
                        width=the_width, activebackground=color_a,
                        bg=color, fg=color_f)

        date_box = Entry(self, width=11)
        date_box.insert(END,"mm_dd_yyyy")

        self.date_box = date_box
        return date_box, date_b


    def make_buttons(self):
        # Make buttons
        # Print label to window
        the_width = 20
        the_width_l = 30
        color = "#054bfc"
        color_a = "#fc6602"     # Active color
        color_l = 'white'       # Label color
        color_f = 'white'       # Foreground color
        button = list(range(4))
        button_labels = list(range(4))
        
        
        # Select Directory
        button_labels[0] = Label (self, text="Choose Lion Images Directory", 
                        font=("Arial Bold", 10), bg=color_l, width=the_width_l)
        button[0] = Button(self, text="Select Dir", 
                        command=self.find_image_dir, 
                        width=the_width, activebackground=color_a,
                        bg=color, fg=color_f)
            
        # Clean file names
        button_labels[1] = Label (self, text= "Copy images to new directory", 
                        font=("Arial Bold", 10), bg=color_l, width=the_width_l)
        button[1] = Button(self, text="Transfer Files", 
                        command=self.transfer, 
                        width=the_width, activebackground=color_a,
                        bg=color, fg=color_f)
        
        # Run annotation
        button_labels[2] = Label (self, text= "Run auto-annotations", 
                        font=("Arial Bold", 10), bg=color_l, width=the_width_l)
        button[2] = Button(self, text="Annotate", 
                        command=self.get_thresh_input,# Ask user for threshold
                        width=the_width, activebackground=color_a,
                        bg=color, fg=color_f)

        # Launch Image Label
        button_labels[3] = Label (self, text= "Check annotations", 
                        font=("Arial Bold", 10), bg=color_l, width=the_width_l)
        button[3] = Button(self, text="Verify", 
                        command=self.run_image_lb, 
                        width=the_width, activebackground=color_a,
                        bg=color, fg=color_f)
        return button, button_labels
 

    def make_status_bar(self):
        status = Canvas(self, width=500, height=80,
                bg="white",relief=FLAT, highlightthickness=0)
        return status
  

    # Callbacks 
    def get_date(self):
        the_date = self.date_box.get() 
        good_date = re.search( r'^[0-1][0-9]_[0-3][0-9]_[1-2][0-9]{3}$', 
                            the_date, re.I)
        if good_date:
            self.root.messages[0].config(text=f'You entered {the_date}',
                                    fg=self.green)
            self.root.messages[1].config(text=f"Date: {the_date}")
            self.the_date = the_date #store date
        else:
            self.root.messages[0].config(text='Please type date in form mm_dd_yyyy',
                                    fg='red')


    def find_image_dir(self):
        # Directory selector
        image_directory = filedialog.askdirectory()
        print(image_directory)
        path,file_name = os.path.split(image_directory) 
        # Print label to window
        self.root.messages[2].configure(text=image_directory)
        self.button_labels[0].configure(bg="#00cc00")
        self.root.messages[0].config(text=f"You selected: {file_name}",
                                fg = self.green)
        self.image_directory = image_directory  # Pass to root 
        

    def transfer(self):
        # Clean and copy files
        if self.the_date == None:
            self.root.messages[0].config(text='Please type date in form mm_dd_yyyy',
                                    fg='red')
        elif not self.image_directory:
            self.root.messages[0].config(text='Please select an image directory',
                                    fg='red')
        else:
            self.root.messages[0].config(text='Complete please check file names',
                                    fg=self.green)
            self.root.messages[3].config(
                    text=f'New sub-directory created: {self.new_path} ')
            transfer_files(self.image_directory, self.the_date, self.new_path)
            self.button_labels[1].configure(bg="#00cc00")


    def run_status_bar(self, total, current, time_taken):
            current +=1 
            if time_taken != None:
                com_time = (total-current)*time_taken
                self.root.messages[0].configure(text=f'Estimated time {com_time:.2f}(sec)')
            print(f"Current{current}, Total:{total}")
            diff = current/total 
            self.status_bar.update()    # Forces update of widget
            if diff > .17:
                self.status_bar.create_rectangle(0, 25, 50, 75, fill="red")
            if diff > .34:
                self.status_bar.create_rectangle(50, 25, 100, 75, fill="orange")
            if diff > .54:
                self.status_bar.create_rectangle(100, 25, 150, 75, fill="yellow")
            if diff > .71:
                self.status_bar.create_rectangle(150, 25, 200, 75, fill="purple")
            if diff > .81:
                self.status_bar.create_rectangle(200, 25, 300, 75, fill="blue")
            if diff > .90:
                self.status_bar.create_rectangle(300, 25, 450, 75, fill="green")
                self.root.messages[0].config(text='DONE!', fg=self.green)

    
    def get_thresh_input(self):
        self.top_box = Toplevel(width=200)
        self.top_box.title("OPTIONAL - set annotation threshhold")
        m = Message(self.top_box,text = "Set threshold 1-9, or use default(8),"+
                                " then press Enter to run auto-annotator")
        b = Button(self.top_box, text="Enter",command=lambda:    # Run annotations
                    self.set_spin(spin), width=10)
        spin = Spinbox(self.top_box, from_=0, to=10, textvariable = 8)
        m.pack()
        spin.pack()         # Pack in widgets
        b.pack()


    def set_spin(self,spin):        
        # Call back for pop-up
        self.threshold = (float(spin.get())*.1)
        self.top_box.destroy()
        self.check_annotation()     # Run Annotation


    def check_annotation(self):
        time_taken = None
        self.root.messages[0].configure(text=f'Threshold set:{self.threshold:.2f}'
                                        + ', starting annotation..',fg=self.green)
        if self.image_directory != None:
            new_path_abs = os.path.join(self.image_directory, self.new_path)
            the_images, the_names = get_image_files(new_path_abs)
            total = len(the_images)
            print(f"threshold: {self.threshold}") 
            for i, (image_path, name) in enumerate(zip(the_images,the_names)):
                print(f"IMAGE:{image_path}\nNAME: {name}\n")
                self.run_status_bar(total, i, time_taken)
                results, time_taken = self.LINC.detect([image_path], [name],
                                                            self.threshold)
                # Make marking annotation
                create_voc(results, image_path)
            # Color status bar
            self.button_labels[2].configure(bg="#00cc00")
            self.root.messages[3].configure(text= "Please verify annotations/add marking tags")
        
        else:
            self.root.messages[0].config(text='Please transfer files first',
            fg='red')
        self.new_path_abs = new_path_abs


    def run_image_lb(self):
        # Launch image label
        the_path = os.path.join('labelImg', 'labelImg.py')
        print(f'IMAGE PATH:{self.new_path_abs}')
        if (self.new_path_abs != None) and os.path.isdir(self.new_path_abs):
            subprocess.call(["python3", the_path, self.new_path_abs])
            self.button_labels[3].configure(bg="#00cc00")
        else:
            self.root.messages[0].configure(text="Bad path: Select Directory again", 
                                            fg='red')
 
