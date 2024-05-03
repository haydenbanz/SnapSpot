# -*- coding: utf-8 -*-
"""Copy of Object_dection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15NgKyevs83lDyM0gU4a9S2G-pN6Dcu4d
"""

pip install torch

pip install transformers

pip install pillow

from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import requests

url = "https://www.wallpapers13.com/wp-content/uploads/2016/02/Dinosaurs-Tyrannosaurus-Rex-lost-world-of-animals-from-the-past-HD-Wallpaper-840x525.jpg"
image = Image.open(requests.get(url, stream=True).raw)

# you can specify the revision tag if you don't want the timm dependency
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)

# convert outputs (bounding boxes and class logits) to COCO API
# let's only keep detections with score > 0.9
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    print(
            f"Detected {model.config.id2label[label.item()]} with confidence "
            f"{round(score.item(), 3)} at location {box}"
    )