import pandas as pd
import matplotlib.pyplot as plt
import time, os

class resultsplot():
    def show(self, latest_folder):
        if latest_folder:
            plot_path = os.path.join("./runs/segment/", latest_folder,"results.csv")
        # Load the CSV file into a DataFrame, considering the spaces
            data = pd.read_csv(plot_path, skipinitialspace=True)
            os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
            # Strip column names of spaces
            data.columns = [col.strip() for col in data.columns]

            # Create a figure with 2x2 subplots (adjust as needed)
            fig, axs = plt.subplots(2, 3, figsize=(14, 10))

            # Plot different metrics on separate subplots
            data.plot(x='epoch', y=['train/box_loss', 'val/box_loss'], ax=axs[0, 0], legend=True, grid=True)
            axs[0, 0].set_title('Box Loss over Epochs')
            axs[0, 0].set_ylabel('Box Loss Value')

            data.plot(x='epoch', y=['train/seg_loss','val/seg_loss'], ax=axs[0, 1], legend=True, grid=True)
            axs[0, 1].set_title('Segmentation Loss over Epochs')
            axs[0, 1].set_ylabel('Segmentation Loss Value')

            data.plot(x='epoch', y=['train/cls_loss','val/cls_loss'], ax=axs[1, 0], legend=True, grid=True)
            axs[1, 0].set_title('Classification Loss over Epochs')
            axs[1, 0].set_ylabel('Classification Loss Value')

            data.plot(x='epoch', y=['train/dfl_loss','val/dfl_loss'], ax=axs[1, 1], legend=True, grid=True)
            axs[1, 1].set_title('DFL Loss over Epochs')
            axs[1, 1].set_ylabel('DFL Loss Value')

            data.plot(x='epoch', y=['metrics/precision(B)'], ax=axs[0, 2], legend=True, grid=True)
            axs[0, 2].set_title('Metrics/precesion')
            axs[0, 2].set_ylabel('Precision Value')

            data.plot(x='epoch', y=['lr/pg0', 'lr/pg1', 'lr/pg2'], ax=axs[1, 2], legend=True, grid=True)
            axs[1, 2].set_title('Learning Rate per Epoch')
            axs[1, 2].set_ylabel('Learning Rate')

            plt.tight_layout()
            #plt.show()
        else:
            print("Info", "No training data found!")
    
    def get_latest_training_folder(self, base_path):
        # Get all subdirectories in the base path
        subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        # Filter out directories that don't start with "train"
        train_dirs = [d for d in subdirs if d.startswith('train')]
        
        # Sort directories by number
        def sort_key(x):
            try:
                return int(x[5:])  # Convert the string after 'train' to integer
            except ValueError:  # Handle non-integer values
                return -1  # Put them at the beginning of the list
        
        sorted_train_dirs = sorted(train_dirs, key=sort_key)
        
        # Return the last one (highest number)
        return sorted_train_dirs[-1] if sorted_train_dirs else None
