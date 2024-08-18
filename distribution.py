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
parser.add_argument('--coeff', type=int, default=1000,
                    help='Random sampling pool generation size multiplied by COEFF (default 1000)')

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
    key = keys[random.randint(0, len(keys)-1)]
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


def multiply_items(items, x):
    for key in items:
        items[key] *= x


def generate_objects(file_handle, coeff=10):
    existing_combos = {}
    raw_combinations = []
    _mudras = copy.deepcopy(mudras)
    _hairstyles = copy.deepcopy(hairstyles)
    _materials = copy.deepcopy(materials)
    _background_urnas = copy.deepcopy(background_urnas)

    multiply_items(_mudras, coeff)
    multiply_items(_hairstyles, coeff)
    multiply_items(_materials, coeff)
    multiply_items(_background_urnas, coeff)

    print("populating raw")
    while True:
        mudra = pop_item(_mudras)
        material = pop_item(_materials)
        hairstyle = pop_item(_hairstyles)
        background_urna = pop_item(_background_urnas)

        if mudra is None or material is None or hairstyle is None or background_urna is None:
            break

        raw_combinations.append([mudra, material, hairstyle, background_urna])

    maxtries = 10000
    tries = 0
    count = 0
    print("sampling from raw")
    while tries < maxtries:
        i = random.randint(0, len(raw_combinations)-1)
        combination = raw_combinations[i]

        mudra = combination[0]
        material = combination[1]
        hairstyle = combination[2]
        background_urna = combination[3]

        combination_string = f"{mudra},{hairstyle},{material},{background_urna}"

        if combination_string in existing_combos:
            tries += 1
            continue

        total_rarity = get_total_rarity(mudra, material, hairstyle, background_urna)

        out_line = f'{mudra},{hairstyle},{material},{background_urna},{total_rarity*100:.4f}\n'
        file_handle.write(out_line)

        existing_combos[combination_string] = True
        count += 1

        if count == 1000:
            break

    if tries == maxtries:
        print(f"max tries reached ({maxtries})")


def generate_header(file_handle):
    file_handle.write('Mudra,Hairstyle,Material,Background & Urnas,Rarity %\n')


def generate_file(filename, coeff):
    csv = open(filename, 'w')
    generate_header(csv)
    generate_objects(csv, coeff)
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
                generate_file(f'{filename}-{bulk_count}.csv', args.coeff)
            bulk_count -= 1

        if concatenate_file_handle is not None:
            concatenate_file_handle.close()
            print(f'written to {filename}.csv')
        return

    generate_file(f'{filename}.csv', args.coeff)


if __name__ == "__main__":
    main()
