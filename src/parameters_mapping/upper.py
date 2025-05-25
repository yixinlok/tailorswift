from utils import *
from get_model import *

''' 
--- UPPER ---
meta category
- FittedShirt
- Shirt
call the following attribute functions:
- shirt (done)
- collar (split into neckline and collar)
- sleeve (add hardcoded ones)
- left (asymm)

'''
'''strapless, length, width (only matters for regular shirt), flare'''
def map_meta_upper(garment_class, attribute_scores, image, design):
    if garment_class not in ['shirt, blouse',
                        'top, t-shirt, sweatshirt',
                        'sweater', 'cardigan', 'jacket',
                        'vest','coat', 'dress', 'jumpsuit']:
        print("There is no upper component")
        return design
    TIGHTNESS_INDICES = [135, 136, 137]
    attr = max_attribute(TIGHTNESS_INDICES, attribute_scores) 
     
    # set regular shirt as default
    design["meta"]["upper"]["v"] = "Shirt"
    if attr == "tight":
        design["meta"]["upper"]["v"] = "FittedShirt"
    
    TUBE = 13
    if attribute_scores.iloc[TUBE] > 0.3:
       design["shirt"]["strapless"]["v"] = True

    design = map_shirt(garment_class, attribute_scores, image, design)
    # sleeveless set to true by default
    return design

def map_shirt(garment_class, attribute_scores, image, design):
    length = 1.2  # 0.5-3.5
    width = 1.05  # 1.0 - 1.3
    flare = 1.0  # 0.7-1.6
    print("shirt: ")
    # initialise width, length, flare from model 
    # model = get_vit("../models/SAVED_MODELS/shirt.pth", 3)
    # width, length, flare = test_model(model, image)
    # print("from model: width, length, flare", width, length, flare)
    
    # empire waistline, drop waistline
    if garment_class == "dress":
        attr = max_attribute(DRESS_RISE_INDICES, attribute_scores)  
        length = DRESS_TOP_LENGTHS[attr]
        
        # if it's a waistless dress, it's just super long. and it has no bottom component
        if attr == "no waistline":
            dress_attr = max_attribute(BOTTOM_LENGTH_INDICES, attribute_scores)
            length = SHIRT_DRESS_LENGTHS[dress_attr]
    else:
        attr = max_attribute(SHIRT_TOP_INDICES, attribute_scores)  
        length = SHIRT_TOP_LENGTHS[attr]
    
    # directly take width and flare from the model or default
    print(attr)
    # above the hip 146, hip 147
    design["shirt"]["length"]["v"] = length
    design["shirt"]["width"]["v"] = width
    design["shirt"]["flare"]["v"] = flare

    return design   
    
'''
--- NECKLINE ---
'''
''' CircleNeckHalf CurvyNeckHalf VNeckHalf SquareNeckHalf
TrapezoidNeckHalf CircleArcNeckHalf Bezier2NeckHalf '''

def map_collar_neckline(garment_class, attribute_scores, image, design):
    # -0.5 - 1
    collar_type = "CircleNeckHalf"
    width = 0.2
    fc_depth = 0.3
    # neckline shape
    NECKLINE_TYPE_INDICES = [181, 182, 183, 186, 187, 190, 191]
    attr = max_attribute(NECKLINE_TYPE_INDICES, attribute_scores)  
    
    BOAT_NECKLINE = 189
    if attribute_scores.iloc[BOAT_NECKLINE] > 0.1:
        width = 1

    PLUNGING_NECKLINE = 192
    if attribute_scores.iloc[PLUNGING_NECKLINE] > 0.1:
        fc_depth = 0.8

    if attr in ["round", "crew"]:
        collar_type = "CircleNeckHalf"
    elif attr in ["u-neck", "scoop"]:
        collar_type = "CircleNeckHalf"
        fc_depth = 0.5
    if attr == "v-neck":
       collar_type = "VNeckHalf"
    if attr == "square":
        collar_type = "SquareNeckHalf"
    if attr == "sweetheart":
        collar_type = "Bezier2NeckHalf"
        design["collar"]["f_bezier_x"]["v"] = 0.4
        design["collar"]["f_bezier_y"]["v"] = 0.175
    # TODO: for choker neckline we need to add a turtle lapel 

    design["collar"]["f_collar"]["v"] = collar_type
    design["collar"]["b_collar"]["v"] = collar_type
    design["collar"]["width"]["v"] = width
    design["collar"]["fc_depth"]["v"] = fc_depth
    
    return design
    

'''
--- COLLAR ---
collars are directly mapped!
'''
def map_collar_component(garment_class, attribute_scores, image, design):
    if garment_class not in ['hood', 'collar', 'lapel']:
        print("this is not a collar component")
        return design
    if garment_class == 'hood':
        design["collar"]["component"]["style"]["v"] = "Hood2Panels"
        # TODO: hood length and depth
    else:
        COLLAR_TYPE_INDICES = [162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172]
        collar_attr = max_attribute(COLLAR_TYPE_INDICES, attribute_scores)
        design["collar"]["component"]["style"]["v"] = "SimpleLapel"

        if collar_attr == "turtle":
            design["collar"]["component"]["style"]["v"] = "Turtle"
        
        # TODO: lapel depth (thickness)
    return design

'''
--- SLEEVE ---
sleeves are directly mapped!
- sleeveless
- armhole shape
- length
- connecting_width
- end_width
- sleeve_angle (only matters for angled armhole)
- opening_dir_mix
- standing_shoulder
- standing_shoulder_len
- connect_ruffle
- smoothing_coeff
- cuff
'''

def map_sleeve(garment_class, attribute_scores, image, design):
    if garment_class != 'sleeve':
        print("this is not a sleeve")
        return design
    design["sleeve"]["sleeveless"]["v"] = False

    length = 0.9
    connecting_width = 0.2
    end_width = 1.0
    # length
    SLEEVE_LENGTH_INDICES = [156, 157, 158, 159, 160]
    attr = max_attribute(SLEEVE_LENGTH_INDICES, attribute_scores)  
    if attr == "sleeveless":
        return design
    length = SLEEVE_LENGTHS[attr]
    # if there is a specific sleeve type, customise it. otherwise, use regular, 
    # hardcoded sleeves
    SLEEVE_TYPE_INDICES = [207, 209, 210, 211, 212, 213, 214, 215, 216]
    type_attr = max_attribute(SLEEVE_TYPE_INDICES, attribute_scores)  
    index, score = max_index_score(SLEEVE_TYPE_INDICES, attribute_scores)

    if score < 0.1:
        type_attr = None
    # 'cap','puff', 'bell', 'circular flounce', 'poet', 'dolma, batwing', 'bishop', 'leg of mutton', 'kimono',
    if type_attr == "cap":
        length = 0.15
        connecting_width = 0.5
        end_width = 0.5
    elif type_attr == "puff":
        connecting_width = 0.5
        end_width = 0.5
        design["sleeve"]["cuff"]["type"]["v"] = "CuffBand"
    elif type_attr == "bell":
        connecting_width = 0.5
        end_width = 0.5
    elif type_attr == "circular flounce":
        design["sleeve"]["cuff"]["type"]["v"] = "CuffSkirt"
    elif type_attr == "poet":
        design["sleeve"]["cuff"]["type"]["v"] = "CuffBandSkirt"
    elif type_attr == "dolma, batwing":
        pass
    elif type_attr == "bishop":
        length = 0.8
        design["sleeve"]["cuff"]["type"]["v"] = "CuffBand"
    elif type_attr == "leg of mutton":
        # connecting ruffle
        design["sleeve"]["cuff"]["type"]["v"] = "CuffBand"
    elif type_attr == "kimono":
        connecting_width = 2.0
        end_width = 2.0

    if type_attr == None:
        attr = max_attribute(TIGHTNESS_INDICES, attribute_scores)  
        if attr == "tight":
            connecting_width = 0
            end_width = 0.2
        if attr == "regular":
            connecting_width = 0.2
            end_width = 0.6
        if attr == "loose":
            connecting_width = 0.5
            end_width = 0.8

    design["sleeve"]["connecting_width"]["v"] = connecting_width
    design["sleeve"]["end_width"]["v"] = end_width
    design["sleeve"]["length"]["v"] = length
    return design 