import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Canvas
from PIL import Image, ImageTk, ImageDraw, ImageFont


class AnnotationViewer:
    def __init__(self, folder_path, parent=None):
        self.folder_path = folder_path
        self.image_files = sorted(glob.glob(os.path.join(folder_path, "*.jpg")))
        self.annotation_files = [os.path.splitext(image_file)[0] + '.txt' for image_file in self.image_files]
        self._filter_valid_files()
        
        self.current_index = 0
        self.MAX_WIDTH = 1280  # Set max display dimensions
        self.MAX_HEIGHT = 720
        
        self.photo = None
        self._init_gui(parent)

    # ----------------------- File Management Methods ----------------------- #
    def _filter_valid_files(self):
        valid_image_files = []
        valid_annotation_files = []

        for img_file, ann_file in zip(self.image_files, self.annotation_files):
            if os.path.exists(img_file) and os.path.exists(ann_file):
                valid_image_files.append(img_file)
                valid_annotation_files.append(ann_file)
            else:
                if os.path.exists(img_file):
                    os.remove(img_file)
                if os.path.exists(ann_file):
                    os.remove(ann_file)

        self.image_files = valid_image_files
        self.annotation_files = valid_annotation_files

    # ----------------------- GUI Initialization Methods ----------------------- #
    def _init_gui(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Annotation Viewer")

        self._setup_canvas()
        self._setup_controls()
        self.root.bind('y', self._key_event)
        self.root.bind('n', self._key_event)

        self.display_current_image()
        #self.root.mainloop()

    def _setup_canvas(self):
        self.canvas = Canvas(self.root, width=self.MAX_WIDTH, height=self.MAX_HEIGHT)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    def _setup_controls(self):
        self.keep_label = tk.Label(self.root, text="Keep this image?")
        self.keep_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.yes_button = tk.Button(self.root, text="Yes", command=self.keep_image, width=20, height=3)
        self.yes_button.grid(row=2, column=0, padx=10, pady=10)

        self.no_button = tk.Button(self.root, text="No", command=self.remove_image, width=20, height=3)
        self.no_button.grid(row=2, column=1, padx=10, pady=10)

        self.back_button = tk.Button(self.root, text="Back", command=self.previous_image, width=20, height=3)
        self.back_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # ----------------------- Image Display and Annotation Methods ----------------------- #
    def resize_image(self, img):
        """Resize the given image while maintaining its aspect ratio."""
        width, height = img.size
        aspect_ratio = width / height
        new_width = min(self.MAX_WIDTH, width)
        new_height = new_width / aspect_ratio

        if new_height > self.MAX_HEIGHT:
            new_height = min(self.MAX_HEIGHT, height)
            new_width = new_height * aspect_ratio

        return img.resize((int(new_width), int(new_height)), Image.LANCZOS)

    def display_current_image(self):
        self.canvas.delete("all")
        image_path = self.image_files[self.current_index]
        annotation_path = self.annotation_files[self.current_index]
        annotations_list = self._parse_annotations(annotation_path)

        img = Image.open(image_path)
        img = self.resize_image(img)
        img = img.convert('RGBA')

        overlay = self._draw_annotations(img.size, annotations_list)

        print(f"Displaying image {self.current_index} from {len(self.image_files)} total images.")
        self._composite_and_display(img, overlay)

    def _parse_annotations(self, annotation_path):
        with open(annotation_path, 'r') as f:
            lines = f.readlines()
            annotations_list = []

            for line in lines:
                data = [float(coord) for coord in line.split()]
                annotations = data[1:]
                if len(annotations) % 2 != 0:
                    messagebox.showerror("Error", f"Incorrect annotation format for {annotation_path}.")
                    return []
                annotations_list.append(annotations)

        return annotations_list

    def _draw_annotations(self, img_size, annotations_list):
        overlay = Image.new('RGBA', img_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        large_font = ImageFont.truetype("arial.ttf", size=30)
        for annotations in annotations_list:
            width, height = img_size
            points = [(annotations[i] * width, annotations[i + 1] * height) for i in range(0, len(annotations), 2)]
            draw.line(points + [points[0]], fill=(0, 255, 0, 255), width=2)
            draw.polygon(points, fill=(255, 0, 0, 128))
            label_position = (points[0][0], points[0][1]+15)  # Adjust y-offset as needed
            try:
                large_font = ImageFont.truetype("arial.ttf", size=30)  # Use a larger font size
            except IOError:
                large_font = ImageFont.load_default()

            large_text_width, large_text_height = draw.textsize("Bag", font=large_font)
            large_box_margin = 10  # Larger margin around the text
            draw.rectangle(
                [label_position[0] - large_box_margin, label_position[1] - large_box_margin, 
                label_position[0] + large_text_width + large_box_margin, label_position[1] + large_text_height + large_box_margin],
                outline=(255, 255, 255, 255),
                fill=(0, 0, 0, 255),  # Filling the rectangle with black color
                width=2)
            draw.text(label_position, str("Bag"), fill=(255, 255, 255, 255), font=large_font)
        return overlay

    def _composite_and_display(self, img, overlay):
        try:
            img = Image.alpha_composite(img, overlay)
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        except Exception as e:
            print(f"Error encountered: {e}")

    # ----------------------- User Interaction Methods ----------------------- #
    def keep_image(self):
        self.next_image()

    def remove_image(self):
        os.remove(self.image_files[self.current_index])
        os.remove(self.annotation_files[self.current_index])
        del self.image_files[self.current_index]
        del self.annotation_files[self.current_index]
        if not self.image_files:
            #self.root.quit()
            self.root.destroy()
        else:
            self.display_current_image()

    def next_image(self):
        self.current_index += 1
        if self.current_index >= len(self.image_files):
            #self.root.quit()
            self.root.destroy()
        else:
            self.display_current_image()

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current_image()

    def _key_event(self, event):
        if event.char == 'y':
            self.keep_image()
        elif event.char == 'n':
            self.remove_image()
