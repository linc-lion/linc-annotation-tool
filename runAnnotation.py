from threading import Event, Thread
import multiprocessing
from multiprocessing import Pool
import time
from predict_AI import LINC_detector
from ui_vocFileUtil import create_voc
import os


# Outside class to avoid pickle error
def run_anno_proc(data):
    # Code to run annotations with a process

    the_results = []
    proc_name = multiprocessing.current_process().name
    print(f'Spawned {proc_name}')

    # Model path need to load in each instance, slows down
    model_path = os.path.join(os.getcwd(), 'DeployModels', 'body_parts_1.pth')
    # Prime model for use
    LINC = LINC_detector(model_path)

    # Run images
    data = zip(data[0], data[1], data[2])
    for (image_path, name, threshold) in data:
        #print(f"IMAGE:{image_path}\nNAME: {name}\n Thresh: {threshold}\n")
        try:
            results, time_taken = LINC.detect([image_path], [name], threshold)
        except Exception as e:
            print(e)
            return
        time_taken += time_taken
        # Make marking annotation
        create_voc(results, image_path)
        the_results.append(results)
        #print(f"TIME_TAKEN:{time_taken}")

    return the_results, time_taken


def chunk_it(data, sections):
    # Split list into even as possible sub lists
    split_lists = []
    size, leftovers = divmod(len(data), sections)

    for i in range(sections):
        if leftovers != 0:
            end = size + 1
            leftovers -= 1
        else:
            end = size
        split_lists.append(data[i*size:(i*size)+end])

    return split_lists


# Main worker class
class LINCWorker():
    def __init__(self, *args, **kwargs):
        # !args takes lists of same size to run jobs on
        self.status = 0 # Jobs completion percentage
        self.run_time = 0
        self.data = []
        self.thread = None
        self.the_pool = None
        # Get aval cpus
        self.num_proc = multiprocessing.cpu_count()
        print(f'Processor count: {self.num_proc}')

        # Create Thread Event to tell when thread completes
        self.ready = Event()
        self.kill = Event()


    def __del__(self):
        print("Clean Up Thread")
        self.kill_all()


    def start(self):
        self.thread.start()


    def ready(self):
        return self.ready.isSet()


    def get_status(self):
        return self.status


    def get_data(self):
        return self.data


    def kill_all(self):
        # Check for process and kill
        if self.the_pool != None:
            print("Killing pool")
            self.the_pool.terminate()
        # Set kill flag for thread
        if self.thread != None:
            print(f"Kill_all:Thread Alive? {self.thread.isAlive()}")
            self.kill.set()


    def run_in_thread(self, func, args):
        # Create the thread and pass the target func, and args
        self.thread = Thread(target=func, args=args)


    def run_in_process(self, func, args):
        # Start and run the process pool.
        # Divide data into list based on cpu #
        self.the_pool = Pool(processes=self.num_proc)

        images = chunk_it(args[0], self.num_proc)       # Div data evenly between procs
        names = chunk_it(args[1], self.num_proc)
        threshold = chunk_it(args[2], self.num_proc)
        data = zip(images, names, threshold)
        total = self.num_proc                # Get len of data for status bar

        # imap_unordered returns as ready, iterable list.
        try:
            for i, (out_data, time) in enumerate(self.the_pool.imap_unordered(func, data)):
                self.run_time = time
                self.status = (i+1)/total
                #print(f"Appending{out_data}")
                self.data.append(out_data)
                if self.kill.is_set():               # Thread needs to return to stop
                    return
            self.the_pool.close()
        except Exception as e:
            print(e)
            self.the_pool.terminate()
            return
        self.ready.set() # Used to signal to the thread Event the thread is done


    def run_annotation_thread(self, *args):
        # Run annotation in thread
        self.thread = Thread(target=self.run_anno_thread, args=args)
        self.thread.start()
        return self.thread # Return the thread instance to be checked up on


    def run_anno_thread(self, *args):
        # Code to run annotations in thread
        try:
            # Prime model
            model_path = os.path.join(os.getcwd(), 'DeployModels', 'body_parts_1.pth')
            LINC = LINC_detector(model_path)
            image_paths, the_names, threshold = args

            total = len(args[0])                # Get len of data for status bar
            for i, (image_path, name) in enumerate(zip(image_paths, the_names)):
                if self.kill.is_set():
                    print("Thread Shutting down....")
                    return
                self.status = (i/total) if i != 0 else 0
                out_data, time_taken = LINC.detect([image_path], [name],
                                                threshold[0])
                self.run_time = time_taken
                self.data.append(out_data)
                # Make marking annotation
                create_voc(out_data, image_path)

            self.status = 1.00                  # Done 100%
            self.ready.set() # Used to signal to the thread Event the thread is done
        except Exception as e:
            print("Got Ex")
            self.kill.set()     # Send out flag to main context
            return


    def run_annotation_proc(self, *args, num_proc='one'):
        # Run annotation in process wrapped in thread
        if num_proc == 'full':
            self.num_proc = multiprocessing.cpu_count()
        elif num_proc == 'half':
            self.num_proc = int(multiprocessing.cpu_count()/2)
        elif num_proc == 'one':
            self.num_proc = 1
        print(f'Running on {self.num_proc} cpus')
        self.thread = Thread(target=self.run_in_process, args=(func, args))
        self.thread.start()


if __name__ == '__main__':


    # Make data can be any list of data, if not two change zip above
    the_images = [r"C:\Users\stullwindows\Desktop\LincAnnotation\linc-annotation-tool-master\TestImages\lion_fam.jpg"]
        #'AnnotationTool/InImages/LINCImages/0_03_30_1980__ANP_F2_2009_Oct_22_BR.JPG',
        #'AnnotationTool/InImages/LINCImages/2_03_30_1980__ANP_F2_2009_Aug_15_BL.JPG',
        #'AnnotationTool/InImages/LINCImages/3_03_30_1980__ANP_F2_2009_Aug_15_P.JPG',
        #'AnnotationTool/InImages/LINCImages/4_03_30_1980__ANP_F2_2009_Aug_14_L.JPG',
        #'AnnotationTool/InImages/LINCImages/1_03_30_1980__0_34___test34_.JPG']

    the_names = ["lion_fam.jpg"]
        #'0_03_30_1980__ANP_F2_2009_Oct_22_BR.JPG',
        #'1_03_30_1980__0_34___test34_.JPG',
        #'2_03_30_1980__ANP_F2_2009_Aug_15_BL.JPG',
        #'3_03_30_1980__ANP_F2_2009_Aug_15_P.JPG',
        #'4_03_30_1980__ANP_F2_2009_Aug_14_L.JPG']
    the_images = []
    the_names = []
    for the_dir, sub_dir, files in os.walk('TestImages'):
        for the_file in files:
            the_images.append(os.path.join(the_dir, the_file))
            the_names.append(the_file)
    print(the_images, the_names)
    the_thresh_proc = [.8 for i in range(len(the_names))]
    the_thresh_thread = 0.8
    args = (the_images, the_names, the_thresh_proc)

    # Start run
    LW = LINCWorker()

    #LW.run_annotation_proc(the_images, the_names, the_thresh_proc,
    #                         num_proc='half')
    LW.run_annotation_thread(the_images, the_names, the_thresh_proc)
    # Time out to break loop "debug"
    then = time.time()
    while True:
        now = (time.time() - then) # Just safety measure
        time.sleep(1)
        # Show percent done using status global
        #print(f"waiting, {LW.status} percent done")
        if LW.run_time != None:
            print(LW.run_time)

        if LW.ready.isSet():
            print(LW.get_data())
            print(f"toc:{now}")
            break
        if now > 1500:
            print("timeout")
            LW.kill_all()
            break
        if LW.kill.is_set():
            print("Killing")
            LW.kill_all()
            break

    print("exit")
    print(now)
