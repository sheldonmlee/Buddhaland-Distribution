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


def generate_objects(file_handle):
    _mudras = copy.deepcopy(mudras)
    _hairstyles = copy.deepcopy(hairstyles)
    _materials = copy.deepcopy(materials)
    _background_urnas = copy.deepcopy(background_urnas)

    while True:
        mudra = pop_item(_mudras)
        material = pop_item(_materials)
        hairstyle = pop_item(_hairstyles)
        background_urna = pop_item(_background_urnas)

        if mudra is None or material is None or hairstyle is None or background_urna is None:
            break

        total_rarity = get_total_rarity(mudra, material, hairstyle, background_urna)

        out_line = f'{mudra},{hairstyle},{material},{background_urna},{total_rarity*100:.4f}\n'
        file_handle.write(out_line)


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
