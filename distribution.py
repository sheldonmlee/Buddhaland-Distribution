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


def get_total_rarity(head, material, hand, background_gem):
    return get_attribute_rarity(head, heads) * \
            get_attribute_rarity(material, materials) * \
            get_attribute_rarity(hand, hands) * \
            get_attribute_rarity(background_gem, background_gems)


def multiply_items(items, x):
    for key in items:
        items[key] *= x


def generate_objects(file_handle, coeff):
    existing_combos = {}
    raw_combinations = []
    _heads = copy.deepcopy(heads)
    _materials = copy.deepcopy(materials)
    _hands = copy.deepcopy(hands)
    _background_gems = copy.deepcopy(background_gems)

    multiply_items(_heads, coeff)
    multiply_items(_materials, coeff)
    multiply_items(_hands, coeff)
    multiply_items(_background_gems, coeff)

    print("populating raw")
    while True:
        head = pop_item(_heads)
        material = pop_item(_materials)
        hand = pop_item(_hands)
        background_gem = pop_item(_background_gems)

        if head is None or material is None or hand is None or background_gem is None:
            break

        raw_combinations.append([head, material, hand, background_gem])

    maxtries = 10000
    tries = 0
    count = 0
    print("sampling from raw")
    while tries < maxtries:
        i = random.randint(0, len(raw_combinations)-1)
        combination = raw_combinations[i]

        head = combination[0]
        material = combination[1]
        hand = combination[2]
        background_gem = combination[3]

        combination_string = f"{head},{material},{hand},{background_gem}"

        if combination_string in existing_combos:
            tries += 1
            continue

        total_rarity = get_total_rarity(head, material, hand, background_gem)

        out_line = f'{head},{material},{hand},{background_gem},{total_rarity*100:.4f}\n'
        file_handle.write(out_line)

        existing_combos[combination_string] = True
        count += 1

        if count == 1000:
            break

    if tries == maxtries:
        print(f"max tries reached ({maxtries})")


def generate_header(file_handle):
    file_handle.write('Head,Material,Hand,Background Gem,Rarity %\n')


def generate_file(filename, coeff):
    csv = open(filename, 'w')
    generate_header(csv)
    generate_objects(csv, coeff)
    csv.close()
    print(f'written to {filename}')


def generate_all_possible(filename):
    csv = open(filename, 'w')
    generate_header(csv)

    for head in heads:
        for material in materials:
            for hand in hands:
                for background_gem in background_gems:
                    total_rarity = get_total_rarity(head, material, hand, background_gem)

                    out_line = f'{head},{material},{hand},{background_gem},{total_rarity*100:.4f}\n'
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

        if args.concatenate:
            print("Warning: this option does not check for duplicates between multiple generations at the moment")

        while bulk_count:
            if args.concatenate:
                if concatenate_file_handle is None:
                    concatenate_file_handle = open(f'{filename}.csv', 'w')
                    generate_header(concatenate_file_handle)
                generate_objects(concatenate_file_handle, args.coeff)
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
