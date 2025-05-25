import yaml
import csv 
import copy
import pandas as pd

from upper import *
from waistband import * 
from bottom import *
from utils import *

filename = "collar_jacket"
image = "../../../FashionFormer/demo/test_images/collar_jacket.jpg"

df = pd.read_csv("csv_tests/"+filename+".csv")
df = df.sort_values(by="class score", ascending=False)

# each row is each garment class instance detected
# first col garment class
garment_classes = df.iloc[:, 0]
# third col onwards is the attribute scores
attribute_scores = df.iloc[:, 2:]

# create an abstract meta garment
meta_garment = dict()
meta_garment["upper"] = None
meta_garment["collar"] = None 
meta_garment["neckline"] = None
meta_garment["sleeve"] = None
meta_garment["waistband"] = None #omit for now
meta_garment["bottom"] = None

# run this function on each of the garment classes to extract the full garment
# prevents overlaps, like shirt andd dress
def generate_meta_garment(i, garment_class, meta_garment):
    garment_category = []
    if garment_class in ['shirt, blouse',
                        'top, t-shirt, sweatshirt',
                        'sweater', 'cardigan', 'jacket',
                        'vest','coat', 'dress', 'jumpsuit']:
        if meta_garment["upper"] != None:
            return meta_garment
        garment_category.append("upper")

    if garment_class in ['pants', 'shorts', 'skirt', 'dress', 'jumpsuit']:
        if meta_garment["bottom"] != None:
            return meta_garment
        garment_category.append("bottom")

    if garment_class == 'sleeve':
        if meta_garment["sleeve"] != None:
                return meta_garment
        garment_category.append("sleeve")

    if garment_class == 'neckline':
        if meta_garment["neckline"] != None:
                return meta_garment
        garment_category.append("neckline")

    if garment_class in ['collar', 'hood', 'lapel']:
        if meta_garment["collar"] != None:
                return meta_garment
        garment_category.append("collar")
    
    # loop through all, in case it's dress or jumpsuit
    for category in garment_category:
        meta_garment[category] = (i, garment_class)
        
    return meta_garment

for i, garment_class in enumerate(garment_classes):
    meta_garment = generate_meta_garment(i, garment_class, meta_garment)

print(meta_garment)
# open default design template and copy it
with open("default.yaml", "r") as file:
    default_design = yaml.safe_load(file)
new_design = copy.deepcopy(default_design)
garment = new_design['design']

# upper
if meta_garment["upper"] != None:
    index, garment_class = meta_garment["upper"]
    print("upper garment: ", garment_class)
    attribute_scores = df.iloc[index, 2:]
    garment = map_meta_upper(garment_class, attribute_scores, image, garment)

# sleeve
if meta_garment["sleeve"] != None:
    index, garment_class = meta_garment["sleeve"]
    print("sleeve: ", garment_class)
    attribute_scores = df.iloc[index, 2:]
    garment = map_sleeve(garment_class, attribute_scores, image, garment)

# neckline
if meta_garment["neckline"] != None:
    index, garment_class = meta_garment["neckline"]
    print("neckline: ", garment_class)
    attribute_scores = df.iloc[index, 2:]
    garment = map_collar_neckline(garment_class, attribute_scores, image, garment)

# collar
if meta_garment["collar"] != None:
    index, garment_class = meta_garment["collar"]
    print("collar: ", garment_class)
    attribute_scores = df.iloc[index, 2:]
    garment = map_collar_component(garment_class, attribute_scores, image, garment)

# bottom
if meta_garment["bottom"] != None:
    index, garment_class = meta_garment["bottom"]
    print("bottom: ", garment_class)
    attribute_scores = df.iloc[index, 2:]
    garment = map_meta_bottom(garment_class, attribute_scores, image, garment)
    new_design['design'] = garment

with open(filename+".yaml", "w") as file:
    yaml.dump(new_design, file)
