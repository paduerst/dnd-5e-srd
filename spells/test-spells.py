import json

SPELL_NAME_MIN_LENGTH = 3
SPELL_LEVEL_VALUES = range(10)
SPELL_SCHOOL_VALUES = [
    'Abjuration',
    'Conjuration',
    'Divination',
    'Enchantment',
    'Evocation',
    'Illusion',
    'Necromancy',
    'Transmutation'
]


def testSpell(spell: dict) -> bool:
    output = True

    name = spell.get("name")
    if name == None:
        output = False
        print(f"Failure: no name found in {spell}")
    elif not isinstance(name, str):
        output = False
        print(f"Failure: name not string in {spell}")
    elif len(name) < SPELL_NAME_MIN_LENGTH:
        output = False
        print(f"Failure: name too short in {spell}")
    else:
        pass

    ritual = spell.get("ritual")
    if ritual == None:
        output = False
        print(f"Failure: no ritual found in {spell}")
    elif not isinstance(ritual, bool):
        output = False
        print(f"Failure: ritual not bool in {spell}")
    else:
        pass

    level = spell.get("level")
    if level == None:
        output = False
        print(f"Failure: no level found in {spell}")
    elif not isinstance(level, int):
        output = False
        print(f"Failure: level not int in {spell}")
    elif not level in SPELL_LEVEL_VALUES:
        output = False
        print(f"Failure: level not valid in {spell}")
    else:
        pass

    school = spell.get("school")
    if school == None:
        output = False
        print(f"Failure: no school found in {spell}")
    elif not isinstance(school, str):
        output = False
        print(f"Failure: school not str in {spell}")
    elif not school in SPELL_SCHOOL_VALUES:
        output = False
        print(f"Failure: school not valid in {spell}")
    else:
        pass

    return output


def main():
    spells_path = "spells.json"
    with open(spells_path) as fp:
        spells = json.load(fp)

    all_passed = True
    failed_count = 0
    for key in spells:
        if not testSpell(spells[key]):
            all_passed = False
            failed_count = failed_count + 1
            print(f"Failed for key: {key}")

    if all_passed:
        print("Testing complete: all spells passed!")
    else:
        print(f"Testing complete: {failed_count} spell(s) failed.")


if __name__ == "__main__":
    main()
