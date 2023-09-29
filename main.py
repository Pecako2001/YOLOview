import tkinter as tk
from tkinter import simpledialog, Button, Label, Text
import threading
import sys
import os
from ultralytics import YOLO
from FrameGen import framegen
from NewFileAnnotate import newmodel
from Autoannotation import Autoannotation
from AnnotationViewer import AnnotationViewer
from createyaml import createdata

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, str_):
        self.widget.insert(tkmain.END, str_)
        self.widget.see(tkmain.END)

    def flush(self):
        pass


class DatasetCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        #Choose base model
        self.model = YOLO('yolov8n-seg.pt')  # load a pretrained model (recommended for training)
        # Initialize required classes
        self.NewYolo = newmodel()
        self.frame = framegen()
        self.annotation = Autoannotation()
        self.data = createdata()

        # UI Elements
        self.title("Datasetcreator")
        self.geometry("700x700")
        self.style_widgets()
        self.create_layout()

        self.video_path = None

        # Redirect standard output to the Text widget
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
        # First column: "Specify Video" and "Process Video"
        self.path_frame = tk.Frame(self, padx=10, pady=10)
        self.path_frame.grid(row=0, column=0, sticky="nsew")

        self.path_button = Button(self.path_frame, text="Ask for Video Path", command=self.ask_video_path, width=30, height=5)
        self.path_button.grid(row=0, column=0, padx=5, pady=5)

        self.path_label = Label(self.path_frame, text="", width=30, height=10)
        self.path_label.grid(row=1, column=0, padx=5, pady=5)

        self.process_button = Button(self.path_frame, text="Process Video", command=self.process_video, width=30, height=5)
        self.process_button.grid(row=2, column=0, padx=5, pady=5)

        # Second column: "Annotate Data", "Annotation Viewer", "Generate Dataset", and "Train Model"
        self.action_frame = tk.Frame(self, padx=10, pady=10)
        self.action_frame.grid(row=0, column=1, sticky="nsew")

        self.annotate_button = Button(self.action_frame, text="Annotate data", command=self.annotate_data, width=30, height=5)
        self.annotate_button.grid(row=0, column=0, padx=5, pady=5)

        self.viewer_button = Button(self.action_frame, text="Annotation viewer", command=self.annotation_viewer, width=30, height=5)
        self.viewer_button.grid(row=1, column=0, padx=5, pady=5)

        # You'll need to define the logic and function for these two new actions.
        self.generate_dataset_button = Button(self.action_frame, text="Generate Dataset", command=self.datacreation, width=30, height=5)
        self.generate_dataset_button.grid(row=2, column=0, padx=5, pady=5)

        self.train_model_button = Button(self.action_frame, text="Train Model", command=self.trainmodel, width=30, height=5)
        self.train_model_button.grid(row=3, column=0, padx=5, pady=5)

        self.output_text = Text(self, wrap=tk.WORD, width=80, height=10)
        self.output_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def style_widgets(self):
        # Add some font and padding styling
        style_font = ("Arial", 12)
        
        Button(self, font=style_font, padx=5, pady=5)
        Label(self, font=style_font, padx=5, pady=5)
        Text(self, font=style_font, wrap=tk.WORD, padx=10, pady=10)

    def ask_video_path(self):
        self.video_path = simpledialog.askstring("Input", "Enter the video path:")
        if self.video_path:
            self.path_label.config(text=self.video_path)

    def process_video(self):
        # Create a thread to run the video processing code
        thread = threading.Thread(target=self.video_processing_logic)
        thread.start()

    def datacreation(self):
        self.custom_print("Creating dataset")
        self.data.create()

    def trainmodel(self):
        self.results = self.model.train(data="./trainset/data.yaml", epochs=1000, show=True)

    def annotate_data(self):
        thread = threading.Thread(target=self.annotate_data_logic)
        thread.start()

    def annotation_viewer(self):
        # Create a thread to run the video processing code
        thread = threading.Thread(target=self.annotation_viewer_logic)
        thread.start()

    def video_processing_logic(self):
        if self.video_path:
            # Replace the print function with the custom_print function
            self.custom_print(f"Creating frames from the video: {self.video_path}")
            self.frame.generator(self.video_path)
            self.custom_print("Frame generator done")
        else:
            self.custom_print("No video path specified.")

    def annotate_data_logic(self):
        self.custom_print("Annotating data this can take a minute...")
        detectionmodel = 'yolov8n-seg.pt'
        #detectionmodel = simpledialog.askstring("Input", "Enter the detection model with .pt:")
        self.annotation.annotate(detectionmodel)
        self.custom_print(f"Data annotated and moved to dataset folder")

    def annotation_viewer_logic(self):
        self.custom_print("Processing all the images...")
        folder_path = 'dataset'  # Replace with your directory path
        viewer = AnnotationViewer(folder_path, parent=self)  # Changed to self here
        self.custom_print("All the images have been processed and dataset has been created")


    def custom_print(self ,message):
        # Append message to the Text widget and scroll to the end
        self.output_text.insert(tk.END, message + '\n')
        self.output_text.see(tk.END)


if __name__ == '__main__':
    app = DatasetCreatorApp()
    app.mainloop()
