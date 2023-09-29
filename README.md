# **#YOLOview: Advanced YOLO Visualizer with tkinter**

Welcome to YOLOScope, a comprehensive solution for visualizing YOLO-based object detections and annotations, seamlessly integrated with a tkinter GUI.

**Features**
* Efficient YOLO Visualizations: Accurate real-time object detections and visual representation using YOLO.
* Tkinter Integration: A user-friendly graphical user interface for efficient and intuitive operation.
* Segmentation Capabilities: Precise and effective segmentation tools for enhanced visualization.

**Installation and Setup**
1. Clone this repository: git clone https://github.com/Pecako2001/YOLOview.git
2. Navigate to the project directory: cd YOLOview
3. Install the required dependencies: pip install -r requirements.txt
4. Run the application: python main.py

**Contributing**
We value contributions from the community and encourage developers to improve and expand YOLOview's capabilities:
1. Fork the repository.
2. Create a new branch for your features or fixes: git checkout -b [branch-name]
3. Commit your changes with a descriptive message.
4. Push your branch to your fork.
5. Create a Pull Request detailing the changes introduced.

All contributions, either in the form of feature requests or pull requests, are greatly appreciated.

**Contact & Credits**
Developed by Koen van Wijlick. For inquiries or feedback, please reach out to koenvanwijlick@gmail.com.


# **User Interface Overview**

![v1](https://github.com/Pecako2001/YOLOview/assets/77498283/fa5c3fc4-302f-4945-a621-8a80f6a92b2a)

**Ask for Video Path**


Upon clicking this button, the user will be prompted to select or input a path to a video file. This video will then be the subject of subsequent operations.

**Process Video**

After specifying the video path, use this button to initiate processing on the chosen video. The exact processing steps will be determined by the underlying functionality, which might include tasks like extracting frames, basic edits, etc.

**Annotate Data**

Clicking on this button allows users to annotate the video data. Annotations could include marking objects, specifying regions of interest, or tagging frames with specific labels.

**Annotation Viewer**

Use this feature to view the annotations made on the data. It provides a visual representation of all the markings and tags added during the annotation process.

**Generate Dataset**

Once the video has been annotated, this button triggers the process to generate a structured dataset. This dataset can be used for various machine learning tasks, ensuring all annotations are appropriately integrated.

**Train Model**

After generating a dataset, click this button to initiate the training process of a machine learning model using the dataset. Progress or results of the training might be displayed or stored based on the underlying code.

# Issues and Enhancements

**Current Issues:**

- Training Model Problem: The "Train Model" function is currently non-operational due to an incorrect file structure within data.yaml.

**Feature Requests:**

- Enhanced File Selection: Allow the selection of models and files without relying on file extensions, providing greater flexibility and a more intuitive user experience.
