from autodistill_grounded_sam import GroundedSAM
from autodistill.detection import CaptionOntology
from autodistill_yolov8 import YOLOv8

class newmodel:
     def annotation(self):
#while True:
#    while True:
        base_model = GroundedSAM(ontology=CaptionOntology({
        "Bag": "Bag"
            }))

        # label all images in a folder called `context_images`
        base_model.label(
        input_folder="./data",
        output_folder="./trainset"
        )
#        break
#    break