import tkinter.filedialog
import threading
import winsound, sys
import spectogram

from tkinter import *
from recorder import Recorder
from plot import  Plot
from neural_network import NeuralNetwork
from image_transform import ImageTransform
from display_output import  Display


class Gui:

    timer = None

    def __init__(self, root):
        self.l_selected_file_name_var = StringVar()      # variable for label dynamic text
        self.l_timer_var = StringVar()
        self.t_result_str_var = StringVar()


        self.selected_file_name = ""                     # variable for storaging global selected file name
        self.counter = 0                                 # clock counter

        self.b_waveform = []                             # declaring plot buttons
        self.b_fft = []
        self.l_status = []
        self.full_file_path = []

        self.radioIntVar = []                            # 2D or more dimensions plot

        self.menu_bar = Menu(root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.ds_menu = Menu(self.menu_bar, tearoff=0)
        self.nn_menu = Menu(self.menu_bar, tearoff=0)

        self.frame_record = ""
        self.frame_record1 = ""
        self.frame_record2 = ""
        self.frame_record3 = ""

        self.root = root
        self.create_window(root)
        self.create_record(root)
        self.create_result(root)
        self.create_menu_bar(root)

        self.create_presentation(root)             #izbacen preview iz gui-a

        self.disp = ""


        self.root.config(menu=self.menu_bar)
        self.root.mainloop()


    def handleRadioSel(self):
        if(self.radioIntVar.get() == 1):
            self.b_spectrogram['state'] = 'active'
        elif(self.radioIntVar.get() == 2):
            self.b_spectrogram['state'] = 'disabled'

    def open_audio_file(self):
        sys.stdout.write("Searching for file...")
        options = {}
        options['filetypes'] = [('WAV audio files', '.wav')]
        self.full_file_path = tkinter.filedialog.askopenfilename(**options)
        splitted_path = self.full_file_path.split('/')
        file_name = splitted_path[len(splitted_path)-1]
        self.selected_file_name = file_name         #global var, selected file_name
        self.l_selected_file_name_var.set("[Selected file name]: " + self.selected_file_name)

        self.b_fft['state'] = 'active'         # enable plot buttons
        self.b_waveform['state'] = 'active'
        self.b_spectrogram['state'] = 'active'

        print ("\n[Selected file name:] " + file_name)

    def create_menu_bar(self, root):
        self.file_menu.add_command(label = "Open audio file", command = self.open_audio_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.ds_menu.add_command(label = "Generate graphics", command = lambda: spectogram.create_data_set_graphs())
        self.ds_menu.add_command(label = "Graphics augmentation", command = lambda: ImageTransform.gen_dataset_augmens())
        self.menu_bar.add_cascade(label = "Data-Set", menu=self.ds_menu)

        self.nn_menu.add_command(label = "Train", command = lambda: NeuralNetwork.create_and_train_nn())
        self.nn_menu.add_command(label = "Load last model weights", command=lambda : NeuralNetwork.load_model_weights())
        self.menu_bar.add_cascade(label = "Neural Network", menu=self.nn_menu)


    def create_window(self, root):
        root.title("Sound Recognition - Soft Computing")
        root.geometry("550x580")
        root.resizable(height=FALSE, width=FALSE)

    def create_record(self, root):
        self.frame_record = Frame(root)
        self.frame_record.pack(side=TOP, fill=BOTH, pady=(0,5))
        self.frame_record1 = Frame(self.frame_record)
        self.frame_record1.pack(side=TOP, fill=BOTH, pady=(0,10))
        self.frame_record2 = Frame(self.frame_record)                    #12 between 1 and 2
        self.frame_record2.pack(side=TOP, fill=BOTH, pady=(0,10))
        self.frame_record3 = Frame(self.frame_record)
        self.frame_record3.pack(side=BOTTOM, fill=NONE)

        l_caption = Label(self.frame_record1, text="Record sound:")
        l_caption.pack(side=LEFT)
        b_help = Button(self.frame_record1, text="info", width=3, height=1)
        b_help.pack(side=RIGHT)

        self.l_selected_file_name_var = StringVar()
        self.l_selected_file_name_var.set("[Selected file name:] none")

        l_selected_file_name = Label(self.frame_record2, textvariable = self.l_selected_file_name_var, width = 30, height = 1, anchor = 'w')
        l_selected_file_name.pack(side = LEFT)

        self.b_waveform = Button(self.frame_record2, text = "WaveForm", width = 8, height = 1, command = lambda : Plot.plot_audio(self.full_file_path, "raw", self.radioIntVar))
        self.b_waveform.pack(side = RIGHT)
        self.b_waveform['state'] = 'disabled'

        self.b_fft = Button(self.frame_record2, text = "FFT", width = 8, height = 1, command = lambda : Plot.plot_audio(self.full_file_path, "fft", self.radioIntVar))
        self.b_fft.pack(side = RIGHT, padx = 3)
        self.b_fft['state'] = 'disabled'

        self.b_spectrogram = Button(self.frame_record2, text = "Spectrogram", width = 10, height = 1, command = lambda : Plot.plot_audio(self.full_file_path, "spectrogram", self.radioIntVar))
        self.b_spectrogram.pack(side = RIGHT, padx = 3)
        self.b_spectrogram['state'] = 'disabled'

        self.radioIntVar = IntVar()
        R1 = Radiobutton(self.frame_record2, text="2D", variable=self.radioIntVar, value=1, command= lambda: self.handleRadioSel())
        R1.pack( side = RIGHT)
        self.radioIntVar.set(1)     # init 2D as default

        R2 = Radiobutton(self.frame_record2, text="3D", variable=self.radioIntVar, value=2, command= lambda: self.handleRadioSel())
        R2.pack( side = RIGHT)


        global b_start
        global l_time
        b_start = Button(self.frame_record3, text='Record', width=12, height=2, command=lambda: self.main_button_click())
        b_start.pack(pady=10, padx=15, side=LEFT)

        self.l_timer_var.set('00:00')
        l_time = Label(self.frame_record3, height=1, width=5, state='disabled', bg='white', textvariable=self.l_timer_var, foreground='black')
        l_time.pack(pady=10, padx=(10,0), side=LEFT)
        l_status = Label(self.frame_record3, text="...recording", foreground='red')
        l_status.pack(pady=10, padx=(5,10), side=LEFT)
        b_reset = Button(self.frame_record3, text='Reset', padx=2, command=self.reset_button_click())
        b_reset.pack(pady=10, padx=20, side=LEFT)

    def create_presentation(self, root):
        self.disp = Display(self.frame_record)
        self.disp.pack()

        print ("==================INSTRUCTIONS===================")
        print ("1. Load Convolution2D Neural Network weights model...")
        print ("2. Hit *Record* button and wait 1 sec after Beep signal, then start whistling...")
        print ("3. Hit *Recognize* button and check the results...")
        print ("================================================\n")

    def create_result(self, root):
        frame_result = Frame(root)
        frame_result.pack(fill=BOTH)

        l_result = Label(frame_result, text="Recognized sound:")
        l_result.pack(pady=10, padx=5, side=LEFT)

        self.t_result_str_var.set("Output is in console..")

        t_result = Label(frame_result, height=1, width=20, textvariable=self.t_result_str_var, bg="white")
        t_result.pack(pady=10, padx=5, side=LEFT)

        b_predict = Button(frame_result, text='Recognize', command= lambda: NeuralNetwork.predict_results())
        b_predict.pack(pady=10, padx=5, side=LEFT)

        b_details = Button(frame_result, text='Details')
        b_details.pack(pady=10, padx=5, side=RIGHT)

    def tick_timer(self):
        timer = threading.Timer(1, self.tick_timer)
        timer.start()
        self.counter += 1
        if self.counter > 9:
            self.l_timer_var.set('00:' + str(self.counter))
        else:

            self.l_timer_var.set('00:0' + str(self.counter))

        if self.counter > 3:                                    # 3 secs for duration of recording
            timer.cancel()
            self.play_beep()
            self.counter = 0
            self.l_timer_var.set('00:00')
            return

        print ("tick..." + str(self.counter))

    def main_button_click(self):
        self.play_beep()
        self.tick_timer()
        Recorder.start_recording()
        self.full_file_path = "test.wav"
        self.l_selected_file_name_var.set("[Selected file name]: " + "test.wav")
        self.b_spectrogram['state'] = 'active'

    def reset_button_click(self):
        b_start["text"] = "Record"

    def play_beep(self):
        winsound.PlaySound("beep.wav", winsound.SND_ALIAS)

