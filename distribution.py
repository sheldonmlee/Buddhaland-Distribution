import random

heads = {
        "Plain": 100,
        "Mathura": 100,
        "Gandara": 100,
        "Tang": 100,
        "Han": 100,
        "Gupta": 100,
        "Jewel": 100,
        "Tibetan": 100,
        "Thai": 100,
        "Khmer": 100,
        }
_heads = heads

materials = {
        "Aurora": 25,
        "Rainbow": 25,
        "Fire": 25,
        "Ocean": 25,
        "Gold": 150,
        "Forest": 150,
        "Lotus": 150,
        "Porelain": 150,
        "Earth": 150,
        "Silicon": 150,
        }
_materials = materials

hands = {
        "Combo": 90,
        "Dyana": 130,
        "Bhumisparsa": 130,
        "Dharmachakra": 130,
        "Varada": 130,
        "Abaya": 130,
        "Anjali": 130,
        "Vitarka": 130,
        }
_hands = hands

background_gems = {
        "Diamond": 100,
        "Ruby": 180,
        "Emerald": 180,
        "Lapis Lazuli": 180,
        "Amber": 180,
        "Taaffeite": 180,
        }
_background_gems = background_gems

parts = (heads, materials, hands, background_gems)

keys = heads.keys()


def pop_item(items):
    keys = list(items.keys())
    random.shuffle(keys)
    key = keys[0]
    key_index = 0

    while not items[key]:
        key_index += 1
        if key_index > len(keys)-1:
            return None

        key = keys[key_index]

    items[key] -= 1
    return key


csv = open('pivot.csv', 'w')
csv.write('Head,Material,Hand,Background Gem\n')

while True:
    head = pop_item(_heads)
    material = pop_item(_materials)
    hand = pop_item(_hands)
    background_gem = pop_item(_background_gems)

    if head is None or material is None or hand is None or background_gem is None:
        break

    print(head, material, hand, background_gem)
    csv.write('{},{},{},{}\n'.format(head, material, hand, background_gem))

csv.close()
