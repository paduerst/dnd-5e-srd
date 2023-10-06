import json
import re

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
SPELL_CASTING_TIME_VALUES = [
    '1 action',
    '1 bonus action',
    '1 minute',
    '10 minutes',
    '1 hour',
    '8 hours',
    '12 hours',
    '24 hours',
    '1 action or 8 hours',
    '1 reaction, which you take when you see a creature within 60 feet of you casting a spell',
    '1 reaction, which you take when you or a creature within 60 feet of you falls',
    '1 reaction, which you take in response to being damaged by a creature within 60 feet of you that you can see',
    '1 reaction, which you take when you are hit by an attack or targeted by the magic missile spell',
]
SPELL_RANGE_VALUES = [
    'Self',
    'Touch',
    'Sight',
    'Unlimited',
    'Special',
    '5 feet',
    '10 feet',
    '30 feet',
    '60 feet',
    '90 feet',
    '100 feet',
    '120 feet',
    '150 feet',
    '300 feet',
    '500 feet',
    '1 mile',
    '500 miles',
    'Self (10-foot radius)',
    'Self (15-foot radius)',
    'Self (30-foot radius)',
    'Self (5-mile radius)',
    'Self (10-foot-radius sphere)',
    'Self (10-foot-radius hemisphere)',
    'Self (15-foot cone)',
    'Self (30-foot cone)',
    'Self (60-foot cone)',
    'Self (60-foot line)',
    'Self (100-foot line)',
    'Self (15-foot cube)',
]


def testSpellName(spell: dict) -> bool:
    name = spell.get("name")
    if name == None:
        print(f"Failure: no name found in {spell}")
        return False
    elif not isinstance(name, str):
        print(f"Failure: name not string in {spell}")
        return False
    elif len(name) < SPELL_NAME_MIN_LENGTH:
        print(f"Failure: name too short in {spell}")
        return False
    else:
        return True


def testSpellLevel(spell: dict) -> bool:
    level = spell.get("level")
    if level == None:
        print(f"Failure: no level found in {spell}")
        return False
    elif not isinstance(level, int):
        print(f"Failure: level not int in {spell}")
        return False
    elif not level in SPELL_LEVEL_VALUES:
        print(f"Failure: level not valid in {spell}")
        return False
    else:
        return True


def testSpellSchool(spell: dict) -> bool:
    school = spell.get("school")
    if school == None:
        print(f"Failure: no school found in {spell}")
        return False
    elif not isinstance(school, str):
        print(f"Failure: school not str in {spell}")
        return False
    elif not school in SPELL_SCHOOL_VALUES:
        print(f"Failure: school not valid in {spell}")
        return False
    else:
        return True


def testSpellCastingTime(spell: dict) -> bool:
    castingTime = spell.get("castingTime")
    if castingTime == None:
        print(f"Failure: no castingTime found in {spell}")
        return False
    elif not isinstance(castingTime, str):
        print(f"Failure: castingTime not str in {spell}")
        return False
    elif (not castingTime in SPELL_CASTING_TIME_VALUES):
        print(f"Failure: castingTime not valid in {spell}")
        return False
    else:
        return True


def testSpellRitual(spell: dict) -> bool:
    ritual = spell.get("ritual")
    if ritual == None:
        print(f"Failure: no ritual found in {spell}")
        return False
    elif not isinstance(ritual, bool):
        print(f"Failure: ritual not bool in {spell}")
        return False
    else:
        return True


def testSpellCastingRange(spell: dict) -> bool:
    spellRange = spell.get("range")
    if spellRange == None:
        print(f"Failure: no range found in {spell}")
        return False
    elif not isinstance(spellRange, str):
        print(f"Failure: range not str in {spell}")
        return False
    elif (not spellRange in SPELL_RANGE_VALUES):
        print(f"Failure: range not valid in {spell}")
        return False
    else:
        return True


def testSpell(spell: dict) -> bool:
    output = True

    output = output and testSpellName(spell)

    output = output and testSpellLevel(spell)

    output = output and testSpellSchool(spell)

    output = output and testSpellCastingTime(spell)

    output = output and testSpellRitual(spell)

    output = output and testSpellCastingRange(spell)

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
