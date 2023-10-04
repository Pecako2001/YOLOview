import os
from ultralytics import YOLO

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

model = YOLO('./runs/segment/train2/weights/best.pt')  # load a pretrained model (recommended for training)

if __name__ == '__main__':
    # train a model
    results = model.train(data='trainset\data.yaml', epochs=1000, show=True)
