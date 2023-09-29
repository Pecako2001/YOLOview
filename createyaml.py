import os
import shutil
import random

class createdata():
    def create(self):
        # Paths
        base_dir = 'dataset'  # update this path to your dataset
        output_dir = 'trainset'
        image_files = [f for f in os.listdir(base_dir) if f.endswith('.jpg') or f.endswith('.png')]

        # Shuffle the dataset
        random.shuffle(image_files)

        # Split ratios
        train_ratio, val_ratio = 0.8, 0.1
        train_len = int(len(image_files) * train_ratio)
        val_len = int(len(image_files) * val_ratio)

        # Divide the dataset
        train_files = image_files[:train_len]
        val_files = image_files[train_len:train_len + val_len]
        test_files = image_files[train_len + val_len:]

        # Create output directories
        for folder in ['images/train/images', 'images/val', 'images/test', 'labels/train', 'labels/val', 'labels/test']:
            os.makedirs(os.path.join(output_dir, folder), exist_ok=True)

        # Move the image files to images folder and label files to labels folder
        for file_list, img_folder, label_folder in zip([train_files, val_files, test_files], 
                                                    ['images/train', 'images/val', 'images/test'],
                                                    ['labels/train', 'labels/val', 'labels/test']):
            for filename in file_list:
                shutil.move(os.path.join(base_dir, filename), os.path.join(output_dir, img_folder, filename))
                txt_file = filename.rsplit('.', 1)[0] + '.txt'
                shutil.move(os.path.join(base_dir, txt_file), os.path.join(output_dir, label_folder, txt_file))
        base_directory = os.path.dirname(os.path.abspath(__file__))  # this gets the directory of the current Python script
        test_directory = os.path.join(base_directory, 'trainset/test/images')
        train_directory = os.path.join(base_directory, 'trainset/train/images')
        val_directory = os.path.join(base_directory, 'trainset/valid/images')
        
        # Generate data.yaml
        yaml_content = '''\
        names:
         -  Bag
        nc: 1
        train: {train_directory}  # train images (relative to 'path') {train_count} images
        val: {val_directory}  # val images (relative to 'path') {val_count} images
        test:  {test_directory} # test images {test_count} (optional)
        '''

        with open(os.path.join(output_dir, 'data.yaml'), 'w') as yaml_file:
            yaml_file.write(yaml_content.format(train_count=len(train_files), val_count=len(val_files), test_count=len(test_files), train_directory=train_directory, val_directory=val_directory, test_directory=test_directory))

        print("'data.yaml' file has been created!")


        print("Dataset division and organization complete!")
