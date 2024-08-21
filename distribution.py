import random
import copy
import argparse

parser = argparse.ArgumentParser(description="Buddhaland distribution csv generator")

parser.add_argument('--filename', '-f', type=str, help='The csv file name')
parser.add_argument('--bulk', '-b', type=int, help='Generate the distribution n times')
parser.add_argument('--concatenate', '-c', action='store_true',
                    help='For use with --bulk. Concatenate into one big file instead of separtate files')
parser.add_argument('--all-possible', action='store_true',
                    help='Generate all possible combinations without regard to attribute distribution')

args = parser.parse_args()

mudras = {
        "Dhyana": 200,
        "Bhumisparsha": 110,
        "Dharmchakra": 60,
        "Varada": 120,
        "Abhaya": 150,
        "Anajali": 200,
        "Vitarka": 130,
        "Combo": 30,
        }

hairstyles = {
        "Sixteen Kingdoms": 50,
        "Mathura": 30,
        "Gandhara": 150,
        "Tang": 70,
        "338": 20,
        "Gupta": 200,
        "LotusSutra": 130,
        "Himalayas": 160,
        "Sukkothai": 90,
        "Khmer": 100,
        }

materials = {
        "Aurora": 80,
        "Rainbow": 40,
        "Fire": 100,
        "Ocean": 90,
        "Gold": 210,
        "Forest": 80,
        "Lotus": 70,
        "Porelain": 150,
        "Earth": 80,
        "Silicon": 100,
        }

background_urnas = {
        "Diamond": 150,
        "Ruby": 210,
        "Emerald": 120,
        "Lapis Lazuli": 170,
        "Amber": 260,
        "Taaffeite": 90,
        }


def pop_item(items, key):
    if key is None:
        return None

    if not items[key]:
        return None

    items[key] -= 1
    return key


def get_random_key(items):
    keys = list(items.keys())
    _keys = list(items.keys())

    for key in _keys:
        if not items[key]:
            keys.remove(key)

    if len(keys) == 0:
        return None
    random.shuffle(keys)
    return keys[0]


def get_attribute_rarity(attribute, attribute_distribution):
    sum = 0
    for key in attribute_distribution:
        sum += attribute_distribution[key]

    rarity = attribute_distribution[attribute]/sum
    return rarity


def get_total_rarity(mudra, material, hairstyle, background_urna):
    return get_attribute_rarity(mudra, mudras) * \
            get_attribute_rarity(material, materials) * \
            get_attribute_rarity(hairstyle, hairstyles) * \
            get_attribute_rarity(background_urna, background_urnas)


def multiply_items(items, x):
    for key in items:
        items[key] *= x


def generate_objects(file_handle):
    existing_combos = {}
    _mudras = copy.deepcopy(mudras)
    _hairstyles = copy.deepcopy(hairstyles)
    _materials = copy.deepcopy(materials)
    _background_urnas = copy.deepcopy(background_urnas)

    coefficient = 1
    multiply_items(_mudras, coefficient)
    multiply_items(_hairstyles, coefficient)
    multiply_items(_materials, coefficient)
    multiply_items(_background_urnas, coefficient)

    maxtries = 100000
    tries = 0
    count = 0
    while tries < maxtries:
        mudra_key = get_random_key(_mudras)
        material_key = get_random_key(_materials)
        hairstyle_key = get_random_key(_hairstyles)
        background_urna_key = get_random_key(_background_urnas)
        combo = f'{mudra_key}{material_key}{hairstyle_key}{background_urna_key}'
        if combo in existing_combos:
            tries += 1
            continue

        mudra = pop_item(_mudras, mudra_key)
        material = pop_item(_materials, material_key)
        hairstyle = pop_item(_hairstyles, hairstyle_key)
        background_urna = pop_item(_background_urnas, background_urna_key)

        if mudra is None or material is None or hairstyle is None or background_urna is None:
            continue

        total_rarity = get_total_rarity(mudra, material, hairstyle, background_urna)

        out_line = f'{mudra},{hairstyle},{material},{background_urna},{total_rarity*100:.4f}\n'
        file_handle.write(out_line)

        count += 1
        if count == 1000:
            break

        existing_combos[combo] = True

    if tries == maxtries:
        print("max tries")


def generate_header(file_handle):
    file_handle.write('Mudra,Hairstyle,Material,Background & Urnas,Rarity %\n')


def generate_file(filename):
    csv = open(filename, 'w')
    generate_header(csv)
    generate_objects(csv)
    csv.close()
    print(f'written to {filename}')


def generate_all_possible(filename):
    csv = open(filename, 'w')
    generate_header(csv)

    for mudra in mudras:
        for hairstyle in hairstyles:
            for material in materials:
                for background_urna in background_urnas:
                    total_rarity = get_total_rarity(mudra, material, hairstyle, background_urna)

                    out_line = f'{mudra},{material},{hairstyle},{background_urna},{total_rarity*100:.4f}\n'
                    csv.write(out_line)
    csv.close()
    print(f'written to {filename}')


def main():
    bulk_count = args.bulk if args.bulk is not None else 1
    filename = args.filename if args.filename is not None else 'pivot'

    if args.all_possible:
        generate_all_possible(f'{filename}.csv')
        return

    if args.bulk is not None:
        concatenate_file_handle = None
        bulk_count = args.bulk
        while bulk_count:
            if args.concatenate:
                if concatenate_file_handle is None:
                    concatenate_file_handle = open(f'{filename}.csv', 'w')
                    generate_header(concatenate_file_handle)
                generate_objects(concatenate_file_handle)
            else:
                generate_file(f'{filename}-{bulk_count}.csv')
            bulk_count -= 1

        if concatenate_file_handle is not None:
            concatenate_file_handle.close()
            print(f'written to {filename}.csv')
        return

    generate_file(f'{filename}.csv')


if __name__ == "__main__":
    main()
