from utils import *
from get_model import *
''' 
--- BOTTOM ---
meta category:
- SkirtCircle
- AsymmSkirtCircle 
- GodetSkirt
- Pants
- Skirt2 
- SkirtManyPanels 
- PencilSkirt 
- SkirtLevels
call the following attribute functions:
- skirt (done)
- flare skirt (done)
- godet skirt(done)
- pencil skirt (done)
- levels skirt 
- pants (done)
'''

def map_meta_bottom(garment_class, attribute_scores, image, design):
    image = image
    if garment_class not in ['pants', 'shorts', 'skirt', 'dress', 'jumpsuit']:
        return design


    if garment_class in ['pants', 'shorts', 'jumpsuit']:
        design["meta"]["bottom"]["v"] = "Pants"
        design = map_pants(garment_class, attribute_scores, image, design)

    else:
        SKIRT_TYPE_INDICES = [129, 94, 104, 106, 108, 113, 117, 118, 127, 128, 78, 113, 119, 120, 121]
        attr = max_attribute(SKIRT_TYPE_INDICES, attribute_scores)
        attr_i, score = max_index_score(SKIRT_TYPE_INDICES, attribute_scores)
        if score< 0.1:
            attr = 'None'

        # preset gowns
        GOWN_PRESET_INDICES= [119, 120, 121]
        if attr == 'gown':
            gown_attr = max_attribute(GOWN_PRESET_INDICES, attribute_scores)
            attr_i, score = max_index_score(GOWN_PRESET_INDICES, attribute_scores)
            if score> 0.1:
                attr = gown_attr

        # if the dress doens't have a waist, it doesn't have a bottom
        dress_waist_attr = max_attribute(DRESS_RISE_INDICES, attribute_scores)  
        if garment_class == 'dress' and dress_waist_attr == "no waistline":
            return design
        print("dress: ", attr)
        if attr in ['a line', 'straight']:
            design["meta"]["bottom"]["v"] = "Skirt2"
            design = map_skirt2(garment_class, attribute_scores, image, design)
        elif attr in ['flare', 'skater', 'swing', 'circle']:
            design["meta"]["bottom"]["v"] = "SkirtCircle"
            design = map_skirtcircle(garment_class, attribute_scores, image, design)
        elif attr in ['sundress', 'gown']:
            design["meta"]["bottom"]["v"] = "SkirtManyPanels"
        elif attr in ['pencil', 'bodycon']:
            design["meta"]["bottom"]["v"] = "PencilSkirt"
            design = map_pencilskirt(garment_class, attribute_scores, image, design)
        elif attr in ['godet']:
            design["meta"]["bottom"]["v"] = "GodetSkirt"
            design = map_godetskirt(garment_class, attribute_scores, image, design)
        elif attr in ['high low']:
            design["meta"]["bottom"]["v"] = "AsymmSkirtCircle"
            design = map_asymmskirtcircle(garment_class, attribute_scores, image, design)
        elif attr in ['mermaid', 'fit and flare', 'trumpet']:
            design["meta"]["bottom"]["v"] = "SkirtLevels"
            design = map_levelsskirt(garment_class, attribute_scores, image, design, attr)
        else: 
            design["meta"]["bottom"]["v"] = "Skirt2"
            design = map_skirt2(garment_class, attribute_scores, image, design)
    
    return design

'''
length, width(*), flare(*), rise
'''
def map_pants(garment_class, attribute_scores, image, design):
    # set default values
    length = 0.9
    width = 1.0
    flare = 1.0
    rise = 0.75
    
    # initialise width, flare from model 
    # model = get_vit("pants_vit.pth", 2)
    # width, flare = test_model(model, image)

    # model = get_vit("../models/SAVED_MODELS/pants.pth", 2)
    # width, flare = test_model(model, image)
    # print("from model: width, flare", width, flare)

    # length
    PANTS_LENGTHS = {
        "micro": 0.2,
        "mini": 0.3,
        "above-the-knee": 0.4,
        "knee": 0.5,
        "below the knee": 0.7,
        "midi": 0.8,
        "maxi": 0.9,
        "floor": 0.9,
    }
    attr = max_attribute(BOTTOM_LENGTH_INDICES, attribute_scores)
    length = PANTS_LENGTHS[attr]
    print("pants:")
    print(attr)

    # width
    PANTS_WIDTHS_INDICES = [46, 124, 125, 126, 127, 128, 131, 132, 135, 136, 137, 138]
    PANTS_WIDTHS = {
        "bell bottom": (1.0, 1.1),
        "bootcut": (1.0, 1.1),
        "peg": (1.3, 1.5),
        "pencil": (1.1, 1.3),
        "straight": (1.0, 1.2),
        "baggy": (1.3, 1.5),
        "wide leg": (1.3, 1.5),
        "tight": (1.0, 1.1),
        "regular": (1.0, 1.2),
        "loose": (1.3, 1.5),
        "oversized": (1.3, 1.5),
    }
    attr = max_attribute(PANTS_WIDTHS_INDICES, attribute_scores)
    width_min, width_max = PANTS_WIDTHS[attr] 
    width = max(width_min, min(width, width_max)) # clamp to be between these values
   
    # flare
    PANTS_FLARE_INDICES = [46, 124, 125, 126, 127, 128, 135, 136]
    PANTS_FLARES = {
        "bell bottom": (1.1, 1.2),
        "bootcut": (1.1, 1.2),
        "peg": (0.5, 0.7),
        "pencil": (0.6, 0.8),
        "straight": (0.9, 1.1),
        "tight": (0.5, 0.7),
        "regular": (0.9, 1.1),
    }
    attr = max_attribute(PANTS_FLARE_INDICES, attribute_scores)
    flare_min, flare_max = PANTS_FLARES[attr]  
    flare = max(flare_min, min(flare, flare_max)) # clamp to be between these values
    
    # rise
    attr = max_attribute(BOTTOM_RISE_INDICES, attribute_scores)
    rise = BOTTOM_RISES[attr] 

    design["pants"]["length"]["v"] = length
    design["pants"]["width"]["v"] = width
    design["pants"]["rise"]["v"] = rise
    design["pants"]["flare"]["v"] = flare

    return design

'''
length, rise, suns, bottom cut, flare
'''
def map_skirt2(garment_class, attribute_scores, image, design):
    length = 0.9
    rise = 0.75

    # length
    attr = max_attribute(BOTTOM_LENGTH_INDICES, attribute_scores)
    length = SKIRT_LENGTHS[attr]

    # rise
    attr = max_attribute(BOTTOM_RISE_INDICES, attribute_scores)
    rise = BOTTOM_RISES[attr] 

    design["pencil-skirt"]["length"]["v"] = length
    design["pencil-skirt"]["rise"]["v"] = rise
    return design

def map_pencilskirt(garment_class, attribute_scores, image, design):
    # set default values
    length = 0.9
    rise = 0.75
    flare = 0.6

    # length
    attr = max_attribute(BOTTOM_LENGTH_INDICES, attribute_scores)
    length = SKIRT_LENGTHS[attr]

    # rise
    attr = max_attribute(BOTTOM_RISE_INDICES, attribute_scores)
    rise = BOTTOM_RISES[attr] 

    design["pencil-skirt"]["length"]["v"] = length
    design["pencil-skirt"]["rise"]["v"] = rise
    design["pencil-skirt"]["flare"]["v"] = flare

    return design

'''
length, rise, suns, skirts-many-panels, asymm, cut
'''
def map_skirtcircle(garment_class, attribute_scores, image, design):
    # set default values
    length = 0.9
    rise = 0.75
    suns = 1.0
    
    # initialise width, flare from model 
    # model = get_vit("flare_skirt_vit.pth", 1)
    # suns = test_model(model, image)

    # length
    attr = max_attribute(BOTTOM_LENGTH_INDICES, attribute_scores)
    length = SKIRT_LENGTHS[attr]

    # rise
    attr = max_attribute(BOTTOM_RISE_INDICES, attribute_scores)
    rise = BOTTOM_RISES[attr] 

    # suns
    # directly take model output

    design["flare-skirt"]["length"]["v"] = length
    design["flare-skirt"]["rise"]["v"] = rise
    design["flare-skirt"]["suns"]["v"] = suns

    return design 

def map_asymmskirtcircle(garment_class, attribute_scores, image, design):
    design = map_skirtcircle(garment_class, attribute_scores, image, design)
    # overwrite the meta skirt
    # TODO: learn the front length later
    design["flare-skirt"]["asymm"]["v"] = 0.5
    return design

def map_skirtmanypanels(garment_class, attribute_scores, image, design):
    design = map_skirtcircle(garment_class, attribute_scores, image, design)
    # overwrite the meta skirt
    design["meta"]["bottom"]["v"] = "SkirtManyPanels"
    design["flare-skirt"]["panels"]["v"] = 5
    return design

def map_godetskirt(garment_class, attribute_scores, image, design):
    map_pencilskirt(garment_class, attribute_scores, image, design)
    return design

def map_levelsskirt(garment_class, attribute_scores, image, design, attr):
    design["levels-skirt"]["num_levels"]["v"] = 1
    design["levels-skirt"]["level"]["v"] = "SkirtCircle"
   
    base_length_frac = 0.5
    if attr == 'mermaid':
        base_length_frac = 0.65
    elif attr == 'trumpet':
        base_length_frac = 0.5   
    elif attr == 'fit and flare':
        base_length_frac = 0.25
    
    # length
    attr = max_attribute(BOTTOM_LENGTH_INDICES, attribute_scores)
    length = SKIRT_LENGTHS[attr]

    # rise
    attr = max_attribute(BOTTOM_RISE_INDICES, attribute_scores)
    rise = BOTTOM_RISES[attr] 
    
    design["levels-skirt"]["length"]["v"] = length
    design["levels-skirt"]["rise"]["v"] = rise
    design["levels-skirt"]["base_length_frac"]["v"] = base_length_frac

    return design
