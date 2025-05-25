import numpy as np

classes_names = ['shirt, blouse', 'top, t-shirt, sweatshirt', 'sweater', 'cardigan', 'jacket',
               'vest', 'pants', 'shorts', 'skirt', 'coat', 'dress', 'jumpsuit', 'cape', 'glasses', 'hat',
               'headband, head covering, hair accessory', 'tie', 'glove', 'watch', 'belt', 'leg warmer',
               'tights, stockings', 'sock', 'shoe', 'bag, wallet', 'scarf', 'umbrella', 'hood',
               'collar', 'lapel', 'epaulette', 'sleeve', 'pocket', 'neckline', 'buckle', 'zipper', 'applique', 'bead',
               'bow', 'flower', 'fringe', 'ribbon', 'rivet', 'ruffle', 'sequin', 'tassel']

ATTRIBUTE_NAMES = ["classic","polo","undershirt","henley","ringer","raglan","rugby","sailor","crop","halter","camisole","tank","peasant","tube","tunic","smock","hoodie","blazer","pea","puffer","biker","trucker","bomber","anorak","safari","mao","nehru","norfolk","classic military","track","windbreaker","chanel","bolero","tuxedo","varsity","crop.1","jeans","sweatpants","leggings","hip-huggers","cargo","culottes","capri","harem","sailor.1","jodhpur","peg","camo","track.1","crop.2","short","booty","bermuda","cargo.1","trunks","boardshorts","skort","roll-up","tie-up","culotte","lounge","bloomers","tutu","kilt","wrap","skater","cargo.2","hobble","sheath","ball gown","gypsy","rah-rah","prairie","flamenco","accordion","sarong","tulip","dirndl","godet","blanket","parka","trench","pea.1","shearling","teddy bear","puffer.1","duster","raincoat","kimono","robe","dress (coat )","duffle","wrap.1","military","swing","halter.1","wrap.2","chemise","slip","cheongsams","jumper","shift","sheath.1","shirt","sundress","kaftan","bodycon","nightgown","gown","sweater","tea","blouson","tunic.1","skater.1","asymmetrical","symmetrical","peplum","circle","flare","fit and flare","trumpet","mermaid","balloon","bell","bell bottom","bootcut","peg.1","pencil","straight","a-line","tent","baggy","wide leg","high low","curved","tight","regular","loose","oversized","empire waistline","dropped waistline","high waist","normal waist","low waist","basque","no waistline","above-the-hip","hip","micro","mini","above-the-knee","knee","below the knee","midi","maxi","floor","sleeveless","short.1","elbow-length","three quarter","wrist-length","asymmetric","regular.1","shirt.1","polo.1","chelsea","banded","mandarin","peter pan","bow","stand-away","jabot","sailor.2","oversized.1","notched","peak","shawl","napoleon","oversized.2","collarless","asymmetric.1","crew","round","v-neck","surplice","oval","u-neck","sweetheart","queen anne","boat","scoop","square","plunging","keyhole","halter.2","crossover","choker","high","turtle","cowl","straight across","illusion","off-the-shoulder","one shoulder","set-in sleeve","dropped-shoulder sleeve","ragla","cap","tulip.1","puff","bell.1","circular flounce","poet","dolma, batwing","bishop","leg of mutto","kimono.1","cargo.3","patch","welt","kangaroo","seam","slash","curved.1","flap","single breasted","double breasted","lace up","wrapping","zip-up","fly","chained","buckled","toggled","no opening","plastic","rubber","metal","feather","gem","bone","ivory","fur","suede","shearling.1","crocodile","snakeskin","wood","non-textile material","burnout","distressed","washed","embossed","frayed","printed","ruched","quilted","pleat","gathering","smocking","tiered","cutout","slit","perforated","lining","applique","bead","rivet","sequin","no special manufacturing technique","plain","abstract","cartoon","letters, numbers","camouflage","check","dot","fair isle","floral","geometric","paisley","stripe","houndstooth","herringbone","chevron","argyle","leopard","snakeskin.1","cheetah","peacock","zebra","giraffe","toile de jouy","plant"]

BOTTOM_LENGTH_INDICES = [148, 149, 159, 151, 152, 153, 154, 155]

BOTTOM_RISE_INDICES = [141, 142, 143]
BOTTOM_RISES = {
    "high waist": 1.0,
    "normal waist": 0.75,
    "low waist": 0.5,
}
# tight, regular, loose
TIGHTNESS_INDICES = [135, 136, 137]

SKIRT_LENGTHS = {
    "micro": 0.2,
    "mini": 0.3,
    "above-the-knee": 0.4,
    "knee": 0.5,
    "below the knee": 0.7,
    "midi": 0.8,
    "maxi": 0.9,
    "floor": 1.2,
}
SHIRT_DRESS_LENGTHS = {
    "mini": 2.0,
    "above-the-knee": 2.15,
    "knee": 2.5,
    "below the knee": 2.6,
    "midi": 2.85,
    "maxi": 3.4,
}
# empire, dropped, no waistline
DRESS_RISE_INDICES = [139, 140, 145]
DRESS_TOP_LENGTHS = {
    "empire waistline":0.65,
    "dropped waistline": 0.9,
    "no waistline": 1.0,  
}
SHIRT_TOP_INDICES = [146,147]
SHIRT_TOP_LENGTHS = {
    "above-the-hip": 0.95,
    "hip": 1.2,
}
DRESS_BOTTOM_RISES = {
    "empire waistline": 1.0,
    "dropped waistline": 0.75,
    "no waistline": 0.5,   
}

SLEEVE_LENGTHS = {
    "short.1": 0.3,
    "elbow-length" :0.5,
    "three quarter": 0.75, 
    "wrist-length": 0.9
}
def max_index_score(indices, attribute_scores):
    indices = np.array(indices)
    attribute_scores = np.array(attribute_scores)
    
    values = attribute_scores[indices]  # Get values at given indices
    max_idx_in_indices = np.argmax(values)
    return indices[max_idx_in_indices], max_idx_in_indices

def max_attribute(indices, arr):
    index, score = max_index_score(indices, arr)
    return ATTRIBUTE_NAMES[index]

