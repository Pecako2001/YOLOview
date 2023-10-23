#Librarys
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, Button, Label, Text, filedialog, Scrollbar, Listbox, messagebox, ttk
from ttkthemes import ThemedTk, ThemedStyle
import threading, shutil, sys, os

#Local imports
from ultralytics import YOLO
from FrameGen import framegen
from NewFileAnnotate import newmodel
from Autoannotation import Autoannotation
from AnnotationViewer import AnnotationViewer
from createyaml import createdata
from ResultsPlot import resultsplot

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, str_):
        self.widget.insert(tkmain.END, str_)
        self.widget.see(tkmain.END)

    def flush(self):
        pass

class DatasetCreatorApp(ThemedTk):
    def __init__(self):
        super().__init__()
        style = ThemedStyle(self)
        #style.set_theme("arc")

        # Initialize required classes
        self.NewYolo = newmodel()
        self.frame = framegen()
        self.annotation = Autoannotation()
        self.data = createdata()
        self.trainingresults = resultsplot()

        # UI Elements
        self.width = 1420  
        self.height = 1090 
        self.title("Datasetcreator")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.create_layout()
        self.style_widgets()
    
        #Set some variables at startup
        self.video_path = None
        self.selected_item = ''
        self.file_map = {}
        # Redirecting standard output to the Text widget
        sys.stdout = self.TextRedirector(self.output_text)

    class TextRedirector:
        def __init__(self, widget):
            self.widget = widget

        def write(self, str_):
            self.widget.insert(tk.END, str_)
            self.widget.see(tk.END)

        def flush(self):
            pass

    def create_layout(self):
        # Setting up theming and styles
        style = ttk.Style()
        # Notebook styles
        style.configure('TNotebook', background='#5c5c5c', tabposition='n')
        style.configure('TNotebook.Tab', background='#7c7c7c', foreground='#0a0a0a', padding=(10, 5))
        style.map('TNotebook.Tab', background=[('selected', '#4c4c4c')], foreground=[('selected', 'gray')])
        # Button styles
        style.configure('TButton', background='#5c5c5c', foreground='#0a0a0a', borderwidth=1)
        style.map('TButton', background=[('active', '#7c7c7c')], foreground=[('active', 'gray')])
        style.map('TButton', background=[('disabled', '#ff9cac')], foreground=[('disabled', 'black')], relief=[('disabled', 'ridge')])
        # Label styles
        style.configure('TLabel', background='#5c5c5c', foreground='#0a0a0a')
        # Combobox styles
        style.configure('TCombobox', background='white', foreground='#5c5c5c')
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
        style.map('TCombobox', background=[('readonly', '#5c5c5c')], foreground=[('readonly', 'cyan')])
        # Create the notebook (tabs container)
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)
        # Create frames to hold content for each tab
        self.tab1_frame = ttk.Frame(notebook)
        self.tab2_frame = ttk.Frame(notebook)
        self.tab3_frame = ttk.Frame(notebook)
        self.tab4_frame = ttk.Frame(notebook)
        # Add frames to notebook as tabs
        notebook.add(self.tab1_frame, text="Generating dataset")
        notebook.add(self.tab2_frame, text="Model parameters")
        notebook.add(self.tab3_frame, text="Training data")

        #Define alls screens
        self.firstscreen()
        self.secondscreen()
        self.thirdscreen()
        
    def firstscreen(self):
        pady = 5
        padx = 5
        
        # First column: "Specify Video" and "Process Video"
        self.path_frame = tk.Frame(self.tab1_frame, padx=10, pady=10)
        self.path_frame.pack(pady=2)

        self.path_button = ttk.Button(self.path_frame, text="Ask for Video Path", command=self.select_video_path, width=30)
        self.path_button.pack(pady=2)

        self.path_label = ttk.Label(self.path_frame, text="", width=30)
        self.path_label.pack(pady=2)

        self.process_button = ttk.Button(self.path_frame, text="Process Video", command=self.process_video, width=30)
        self.process_button.pack(pady=2)
        self.process_button.config(state=tk.DISABLED)
        
        # Third column: model selection and file addition
        self.model_label = tk.Label(self.tab1_frame, text="Select a model")
        self.model_label.pack(pady=2)
        
        self.model_items = ['yolov8n-seg.pt','yolov8s-seg.pt','yolov8m-seg.pt','yolov8l-seg.pt','yolov8x-seg.pt']
        self.combobox = ttk.Combobox(self.tab1_frame, values=self.model_items)  
        self.combobox.pack(pady=2)
        self.combobox.bind("<<ComboboxSelected>>", self.on_select)
                    
        self.file_button = tk.Button(self.tab1_frame, text="Add File", command=self.add_file) 
        self.file_button.pack(pady=2)

        # Second column: "Annotate Data", "Annotation Viewer", "Generate Dataset", and "Train Model"
        self.action_frame = tk.Frame(self.tab1_frame, padx=10, pady=10)
        self.action_frame.pack(pady=10)

        self.annotate_button = ttk.Button(self.tab1_frame, text="Annotate new model", command=self.newmodel_data, width=30)
        self.annotate_button.pack(pady=2)

        self.annotate_button = ttk.Button(self.tab1_frame, text="Annotate data", command=self.annotate_data, width=30)
        self.annotate_button.pack(pady=2)

        self.viewer_button = ttk.Button(self.tab1_frame, text="Annotation viewer", command=self.annotation_viewer, width=30)
        self.viewer_button.pack(pady=2)

        self.generate_dataset_button = ttk.Button(self.tab1_frame, text="Generate Dataset", command=self.datacreation, width=30)
        self.generate_dataset_button.pack(pady=2)

        self.output_text = tk.Text(self.tab1_frame, wrap=tk.WORD, width=100, height=10)
        self.output_text.pack(pady=2)

    def secondscreen(self):
        parameter_labels = [
            ("Epochs", "100"),
            ("Patience", "50"),
            ("Batch", "16"),
            ("Image Size", "640"),
            ("Freeze", "none"),
            ("Initial Learning Rate (lr0)", "0.01"),
            ("Final Learning Rate (lrf)", "0.01"),
            ("Weight Decay", "0.0005"),
            ("Warmup Epochs", "3"),
            ("Box", "7.5"),
            ("Cls", "0.5"),
            ("Dfl", "1.5")
        ]

        self.labels = [] 
        self.entries = [] 

        for param_label, default_value in parameter_labels:
            # Create label
            label = tk.Label(self.tab2_frame, text=f"{param_label}:")
            label.pack(pady=2)
            self.labels.append(label)
            
            entry = tk.Entry(self.tab2_frame)
            entry.insert(0, default_value)
            entry.pack(pady=2)
            self.entries.append(entry)

        self.submit_button = tk.Button(self.tab2_frame, text="Submit", command=self.submit_values)
        self.submit_button.pack(pady=20)
        
    def thirdscreen(self):
        self.model_frame = tk.Frame(self.tab3_frame, padx=10, pady=10)
        self.model_frame.grid(row=0, column=2, sticky="nsew")

        self.train_model_button = ttk.Button(self.tab3_frame, text="Train Model", command=self.training_data, width=30)
        self.train_model_button.grid(row=1, column=0, padx=5, pady=5)

        self.train_model_button = ttk.Button(self.tab3_frame, text="Download last", command=self.last_download, width=30)
        self.train_model_button.grid(row=1, column=1, padx=5, pady=5)
        self.train_model_button = ttk.Button(self.tab3_frame, text="Download best", command=self.best_download, width=30)
        self.train_model_button.grid(row=1, column=2, padx=5, pady=5)
 
        # Initialize the canvas
        self.fig, _ = plt.subplots(2, 3, figsize=(14, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab3_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        
        self.update_plot()
  
    def submit_values(self):
        values = [entry.get() for entry in self.entries]  
        messagebox.showinfo("Values", "All values are set")

    def update_plot(self):
        try:
            os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
            if os.path.exists("./runs/segment/"):
                latest_folder = self.trainingresults.get_latest_training_folder("./runs/segment/")
                plot_path = os.path.join("./runs/segment/", latest_folder, "results.csv")
                
                if os.path.exists(plot_path):
                    data = pd.read_csv(plot_path, skipinitialspace=True)
                    data.columns = [col.strip() for col in data.columns]
                    
                    axs = self.fig.axes
                    axs[0].clear()
                    data.plot(x='epoch', y=['train/box_loss', 'val/box_loss'], ax=axs[0], legend=True, grid=True)
                    axs[1].clear()
                    data.plot(x='epoch', y=['train/seg_loss','val/seg_loss'], ax=axs[1], legend=True, grid=True)
                    axs[2].clear()
                    data.plot(x='epoch', y=['train/cls_loss','val/cls_loss'], ax=axs[2], legend=True, grid=True)
                    axs[3].clear()
                    data.plot(x='epoch', y=['train/dfl_loss','val/dfl_loss'], ax=axs[3], legend=True, grid=True)
                    axs[4].clear()
                    data.plot(x='epoch', y=['metrics/precision(B)'], ax=axs[4], legend=True, grid=True)
                    axs[5].clear()
                    data.plot(x='epoch', y=['lr/pg0', 'lr/pg1', 'lr/pg2'], ax=axs[5], legend=True, grid=True)
                    self.canvas.draw()
                else:
                    print(f"results.csv not found in {plot_path}")

        except Exception as e:
            print(f"Error in update_plot: {e}")

        self.tab3_frame.after(5000, self.update_plot)        

    def style_widgets(self):
        style_font = ("Arial", 16)

    def on_select(self, event):
        self.selected_item = self.combobox.get()
        if self.selected_item not in self.model_items:
            self.file_path = self.file_map[self.selected_item]
            self.selected_item = self.file_path
        self.custom_print(f"the selected file = {self.selected_item}")
        
    def add_file(self):
        filepath = filedialog.askopenfilename(title="Select a File")
        if filepath: 
            filename = os.path.basename(filepath)  
            self.model_items.append(filename)
            self.file_map[filename] = filepath
            self.combobox['values'] = self.model_items  # Update the combobox with new values

    def select_video_path(self):
        self.video_path = filedialog.askopenfilename(title="Select a video", filetypes=[("All files", "*.*")])
        self.filename_without_extension = os.path.splitext(os.path.basename(self.video_path))[0]
        if self.video_path:
            self.path_label.config(text=self.filename_without_extension)
            self.process_button.config(state=tk.NORMAL)

    def process_video(self):
        thread = threading.Thread(target=self.video_processing_logic)
        thread.start()

    def datacreation(self):
        folder_path = "dataset"
        if any(os.path.isfile(os.path.join(folder_path, f)) for f in os.listdir(folder_path)):
            self.custom_print("Creating dataset...")
            self.data.create()
        else:
            messagebox.showinfo("Error", "The folder is empty, annotate data first")

    def newmodel_data(self):
        thread = threading.Thread(target=self.annotate_new)
        thread.start()

    def annotate_data(self):
        thread = threading.Thread(target=self.annotate_data_logic)
        thread.start()
    
    def training_data(self):
        thread = threading.Thread(target=self.trainmodel)
        thread.start()

    def trainmodel(self):
        if self.selected_item == '':
            messagebox.showinfo("Error", "Please select model first, on first tab")
        else:
            os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
            self.custom_print("Starting Model training...")
            model = YOLO(self.selected_item)
            epochs = int(self.entries[0].get())
            patience = int(self.entries[1].get())
            batch = int(self.entries[2].get())
            imgsz = int(self.entries[3].get())
            freeze = None if self.entries[4].get().lower() == 'none' else int(self.entries[4].get())
            lr0 = float(self.entries[5].get())
            lrf = float(self.entries[6].get())
            weight_decay = float(self.entries[7].get())
            warmup_epochs = int(self.entries[8].get())
            box = float(self.entries[9].get())
            cls = float(self.entries[10].get())
            dfl = float(self.entries[11].get())
            
            self.results = model.train(
                data='trainset\data.yaml',
                epochs=epochs,
                patience=patience,
                batch=batch,
                imgsz=imgsz,
                freeze=freeze,
                lr0=lr0,
                lrf=lrf,
                weight_decay=weight_decay,
                warmup_epochs=warmup_epochs,
                box=box,
                cls=cls,
                dfl=dfl
            )
            messagebox.showinfo("Model training", "Model training done")

    def annotation_viewer(self):
        folder_path = "dataset"
        if any(os.path.isfile(os.path.join(folder_path, f)) for f in os.listdir(folder_path)):
            thread = threading.Thread(target=self.annotation_viewer_logic)
            thread.start()
        else:
            messagebox.showinfo("Error", "The folder is empty, annotate data first")

    def video_processing_logic(self):
        if self.video_path:
            self.custom_print(f"Creating frames from the video: {self.video_path}")
            self.frame.generator(self.video_path, self.filename_without_extension)
            self.custom_print("Frame generator done")
        else:
            self.custom_print("No video path specified.")

    def annotate_data_logic(self):
        detectionmodel = self.selected_item
        if self.selected_item == '':
            messagebox.showinfo("Error", "Please select model first")
        else:
            self.custom_print("Annotating data this can take a minute...")
            self.annotation.annotate(detectionmodel)
            self.custom_print(f"Data annotated and moved to dataset folder")

    def annotation_viewer_logic(self):
        self.custom_print("Processing all the images...")
        folder_path = 'dataset'  # Replace with your directory path
        viewer = AnnotationViewer(folder_path, parent=self)  
        self.custom_print("All the images have been processed and dataset has been created")

    def custom_print(self ,message):
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)

    def last_download(self):
        destination_path = filedialog.askdirectory()
        latest_folder = self.trainingresults.get_latest_training_folder("./runs/segment/")
        plot_path = os.path.join("./runs/segment/", latest_folder, "weights/last.pt")
        if os.path.isfile(plot_path): # Check if file exists at the plot path
            try:
                if destination_path:
                    shutil.copy2(plot_path, os.path.join(destination_path, "last.pt"))
                    messagebox.showinfo("Files copied", f"File copied to: {os.path.join(destination_path, 'last.pt')}")
            except Exception as e:
                messagebox.showinfo("Error", f"Error: {str(e)}")
        else:
            messagebox.showinfo("No file", f"No file found at: {plot_path}")

    def best_download(self):
        destination_path = filedialog.askdirectory()
        latest_folder = self.trainingresults.get_latest_training_folder("./runs/segment/")
        plot_path = os.path.join("./runs/segment/", latest_folder, "weights/best.pt")
        if os.path.isfile(plot_path): 
            try:
                if destination_path: 
                    shutil.copy2(plot_path, os.path.join(destination_path, "best.pt"))
                    messagebox.showinfo("Files copied", f"File copied to: {os.path.join(destination_path, 'best.pt')}")
            except Exception as e:
                messagebox.showinfo("Error", f"Error: {str(e)}")
        else:
            messagebox.showinfo("No file", f"No file found at: {plot_path}")

    def annotate_new(self):
        self.custom_print("Annotating new Yolo model...")
        self.NewYolo.annotation()
        self.custom_print("Annotation completed")

