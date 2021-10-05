from PIL import Image 
from IPython.display import display 
import random
import json

# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

body = ["1","2","3","4","5","6"] 
body_weights = [16,14,14,14,14,14]

eyes = ["1", "2", "3", "4", "5","6","8","9","10"] 
eyes_weights = [15,10,10,10,10,10,10,10,15]

mouth = ["1", "2", "3", "4", "5", "6", "7"] 
mouth_weights = [15,15,15,15,15,15,10]

# Dictionary variable for each trait. 
# Eech trait corresponds to its file name
body_files = {
    "1": "body1",
    "2": "body2",
    "3": "body3",
    "4": "body4",
    "5": "body5",
    "6": "body6"
}

eyes_files = {
    "1": "eyes1",
    "2": "eyes2",
    "3": "eyes3",
    "4": "eyes4",
    "5": "eyes5",
    "6": "eyes6",
    "7": "eyes7",
    "8": "eyes8",
    "9": "eyes9",
    "10": "eyes10"
}

mouth_files = {
    "1": "mouth1",
    "2": "mouth2",
    "3": "mouth3",
    "4": "mouth4",
    "5": "mouth5",
    "6": "mouth6",
    "7": "mouth7"
}
## Generate Traits

TOTAL_IMAGES = 200 # Number of random unique images we want to generate

all_images = [] 

# A recursive function to generate unique image combinations
def create_new_image():
    
    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    new_image["Body"] = random.choices(body, body_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image
    
    
# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 
    
    new_trait_image = create_new_image()
    
    all_images.append(new_trait_image)

    # Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1

print(all_images)

# Get Trait Counts

body_count = {}
for item in body:
    body_count[item] = 0
    
eyes_count = {}
for item in eyes:
    eyes_count[item] = 0

mouth_count = {}
for item in mouth:
    mouth_count[item] = 0

for image in all_images:
    body_count[image["Body"]] += 1
    eyes_count[image["Eyes"]] += 1
    mouth_count[image["Mouth"]] += 1
    
print(body_count)
print(eyes_count)
print(mouth_count)

#### Generate Metadata for all Traits 
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

#### Generate Images    
for item in all_images:

    im1 = Image.open(f'./trait-layers/body/{body_files[item["Body"]]}.png').convert('RGBA')
    im2 = Image.open(f'./trait-layers/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
    im3 = Image.open(f'./trait-layers/mouth/{mouth_files[item["Mouth"]]}.png').convert('RGBA')
    
    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)

    #Convert to RGB
    rgb_im = com2.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)

#### Generate Metadata for each Image    

f = open('./metadata/all-traits.json',) 
data = json.load(f)


IMAGES_BASE_URI = "IPFS_URI"
PROJECT_NAME = "BlockArcade"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Base", i["Body"]))
    token["attributes"].append(getAttribute("Case", i["Eyes"]))
    token["attributes"].append(getAttribute("Logo", i["Mouth"]))

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()