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

background_gems = {
        "Diamond": 100,
        "Ruby": 180,
        "Emerald": 180,
        "Lapis Lazuli": 180,
        "Amber": 180,
        "Taaffeite": 180,
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


def get_total_rarity(head, material, hand, background_gem):
    return get_attribute_rarity(head, heads) * \
            get_attribute_rarity(material, materials) * \
            get_attribute_rarity(hand, hands) * \
            get_attribute_rarity(background_gem, background_gems)


def generate_objects(file_handle):
    _heads = copy.deepcopy(heads)
    _materials = copy.deepcopy(materials)
    _hands = copy.deepcopy(hands)
    _background_gems = copy.deepcopy(background_gems)

    while True:
        head = pop_item(_heads)
        material = pop_item(_materials)
        hand = pop_item(_hands)
        background_gem = pop_item(_background_gems)

        if head is None or material is None or hand is None or background_gem is None:
            break

        total_rarity = get_attribute_rarity(head, material, hand, background_gem)

        out_line = f'{head},{material},{hand},{background_gem},{total_rarity*100:.4f}\n'
        file_handle.write(out_line)


def generate_header(file_handle):
    file_handle.write('Head,Material,Hand,Background Gem,Rarity %\n')


def generate_file(filename):
    csv = open(filename, 'w')
    generate_header(csv)
    generate_objects(csv)
    csv.close()
    print(f'written to {filename}')


def generate_all_possible(filename):
    csv = open(filename, 'w')
    generate_header(csv)

    for head in heads:
        for material in materials:
            for hand in hands:
                for background_gem in background_gems:
                    total_rarity = get_attribute_rarity(head, material, hand, background_gem)

                    out_line = f'{head},{material},{hand},{background_gem},{total_rarity*100:.4f}\n'
                    csv.write(out_line)
    csv.close()


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
