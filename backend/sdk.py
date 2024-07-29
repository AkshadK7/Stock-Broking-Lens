from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import tensorflow as tf
import pandas as pd
import json

class ObjectRecognitionSDK:
    def __init__(self):
        try:
            self.processor = DetrImageProcessor.from_pretrained("./model/resnet-50")
            self.model = DetrForObjectDetection.from_pretrained("./model/resnet-50")

            with open('mappings_dictionary.json', 'r') as file:
                self.dictionary_data = file.read()

            self.dictionary_data_dict = json.loads(self.dictionary_data)

        except Exception as e:
            raise RuntimeError("Error initializing the Object Recognition SDK.")
            
            
    def draw_boxes(self, image, results):
    
        draw = ImageDraw.Draw(image)
        #font = ImageFont.truetype(font="arial.ttf", size=10)

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            label_text = self.model.config.id2label[label.item()]

            draw.rectangle(box, outline='red', width=2)
            label_width, label_height = draw.textsize(label_text)
            label_x = box[0]
            label_y = box[1] - label_height - 5
            draw.text((label_x, label_y), label_text, fill='red')

        return image
        

    def recognize_objects(self, image):
        try:
        
            inputs = self.processor(images=image, return_tensors="pt")
            outputs = self.model(**inputs)

            target_sizes = torch.tensor([image.size[::-1]])
            results = self.processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

            obj_dict = []
            obj_lst = []
            

            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = [round(i, 2) for i in box.tolist()]

                object_name = str(self.model.config.id2label[label.item()])
                confidence = round(score.item(), 3)
                coordinates = box
                obj_dict.append([object_name, confidence, coordinates])
                obj_lst.append(object_name)

            result_img = self.draw_boxes(image, results)
            

            return obj_dict, set(obj_lst), np.array(result_img)

        except Exception as e:
            raise RuntimeError("Error recognizing objects in the image.")



    def calculate_similarity(self, x, y):
        root_word = x
        root_word_embedding = self.similarity_model([root_word])
        other_words = [y]
        other_word_embedding = self.similarity_model(other_words)
        similarity_score = float(
            tf.reduce_sum((root_word_embedding * other_word_embedding) / (
                    tf.norm(root_word_embedding) * tf.norm(other_word_embedding))).numpy())
        return similarity_score

    def categorize_objects(self, obj_lst):
        obj_dict = {}

        for i in obj_lst:

            if i not in obj_dict:
                obj_dict[i] = []

            if(i not in self.dictionary_data_dict):
                obj_dict[i].append("Miscellaneous")

            else:
                for j in self.dictionary_data_dict[i]:
                    obj_dict[i].append(j)

        return obj_dict
