from ultralytics.data.annotator import auto_annotate
import shutil
import os, io, sys
import logging


class Autoannotation:
    def annotate(self, detectionmodel):
        auto_annotate(data='data', det_model=detectionmodel, sam_model='sam_b.pt', output_dir='dataset')
        print(f"detection with model = {detectionmodel}")
        # Check if the source folder exists
        source_folder = 'data'
        if not os.path.exists(source_folder):
            print(f"Source folder '{source_folder}' does not exist.")
            return
        destination_folder = 'dataset'
        # Check if the destination folder exists, if not, create it
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Get all files in the source folder
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        
        # Move each file to the destination folder
        for file in files:
            shutil.move(os.path.join(source_folder, file), os.path.join(destination_folder, file))

        print(f"All files moved from '{source_folder}' to '{destination_folder}'.")
