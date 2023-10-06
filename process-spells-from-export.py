import json
import os
import re
from typing import TypedDict

from bs4 import BeautifulSoup, Tag

normalizationRegexDash = re.compile(r'[ \/]')
normalizationRegexEmpty = re.compile(r'[^a-z\-]')

newlineRegex = re.compile(r'[\n]')
multispaceRegex = re.compile(r' {2,}')

allDashRegex = re.compile(r'[\u00ad\u2010\u2011]')
multiDashRegex = re.compile(r'\-{2,}')

abs_path_to_repo = os.path.dirname(os.path.abspath(__file__))

rel_path_to_parts_folder = os.path.join(
    "exported-from-adobe", "SRD5.1-CCBY4.0_License_live links_files")
abs_path_to_parts_folder = os.path.join(
    abs_path_to_repo, rel_path_to_parts_folder)

file_name_for_spell_descriptions = "part646.htm"
path_for_spell_descriptions = os.path.join(
    abs_path_to_parts_folder, file_name_for_spell_descriptions)


path_for_exported_descriptions = os.path.join(
    abs_path_to_repo, "spells", "exported-descriptions")

made_exported_descriptions_folder = False


def ensureExportedDescriptionsFolderExists():
    global made_exported_descriptions_folder
    if not made_exported_descriptions_folder:
        os.makedirs(path_for_exported_descriptions, exist_ok=True)
        made_exported_descriptions_folder = True


def normalizeString(string: str):
    string_with_dashes = normalizationRegexDash.sub(
        '-', string.lower().strip())
    return normalizationRegexEmpty.sub('', string_with_dashes)


def cleanString(string: str):
    output = string.strip()
    output = newlineRegex.sub(' ', output)
    output = multispaceRegex.sub(' ', output)
    output = allDashRegex.sub('-', output)
    output = multiDashRegex.sub('-', output)
    return output


class SpellLink:
    def __init__(self, soup_link):
        self.name = soup_link.string
        self.id = normalizeString(self.name)
        self.href = soup_link.get('href')
        self.subLink = None

    def addSubLink(self, soup_link):
        self.subLink = soup_link.get('href')

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"({self.name}, {self.id}, {self.href}, {self.subLink})"


class SpellInfo(TypedDict):
    name: str
    level: int
    school: str
    castingTime: str
    ritual: bool
    range: str
    components: str
    duration: str


def getSpellInfo(link: SpellLink) -> SpellInfo:
    output: SpellInfo = {}
    output["name"] = link.name

    # soup1 always contains the level, school, casting time, and range
    path_to_part1 = os.path.join(abs_path_to_parts_folder, link.href)
    with open(path_to_part1) as fp:
        soup1 = BeautifulSoup(fp, 'lxml')
    # print(soup1.prettify())

    subheading_tag = soup1.select_one('.s12')
    if subheading_tag == None:
        raise RuntimeError(
            f"Unable to find subheading_tag for spell {link}")
    subheading = subheading_tag.string.strip()
    subheading_arr = subheading.split(" ")
    is_ritual = False
    if subheading_arr[-1] == "(ritual)":
        is_ritual = True
        subheading_arr.pop()
    if subheading[0].isdigit():
        output["level"] = int(subheading[0])
        output["school"] = subheading_arr[-1].capitalize()
    else:
        output["level"] = 0
        output["school"] = subheading_arr[0]

    strings1 = list(soup1.stripped_strings)
    casting_time_index = strings1.index("Casting Time:")
    spell_range_index = strings1.index("Range:")
    casting_time = ' '.join(
        strings1[(casting_time_index + 1):spell_range_index])
    casting_time = cleanString(casting_time)
    output["castingTime"] = casting_time.strip()

    # ritual bool should come right after casting time
    output["ritual"] = is_ritual

    spell_range = strings1[spell_range_index + 1]
    spell_range = cleanString(spell_range)
    output["range"] = spell_range

    # soup2 contains the rest, starting with components
    path_to_part2 = path_to_part1
    if link.subLink != None:
        path_to_part2 = os.path.join(abs_path_to_parts_folder, link.subLink)
    with open(path_to_part2) as fp:
        soup2 = BeautifulSoup(fp, 'lxml')
    # print(soup2.prettify())

    strings2 = list(soup2.stripped_strings)
    components_index = strings2.index("Components:")
    duration_index = strings2.index("Duration:")
    components = ' '.join(strings2[(components_index + 1):duration_index])
    components = cleanString(components)
    output["components"] = components

    duration = strings2[duration_index + 1]
    duration = cleanString(duration)
    output["duration"] = duration

    SAVE_SPELL_DESCRIPTIONS = True
    if SAVE_SPELL_DESCRIPTIONS:
        description_arr: list[str] = []
        non_description_classes = [["top_nav"], ["nav"], ["s12"], ["s13"]]
        body_paragraphs: list[Tag] = list(soup2.body.find_all("p"))
        for tag in body_paragraphs:
            tag_class = tag.get('class')
            if not tag_class in non_description_classes:
                description_arr.append(tag.prettify().strip())
        description = '\n'.join(description_arr)

        ensureExportedDescriptionsFolderExists()
        save_path = os.path.join(
            path_for_exported_descriptions, f"{link.id}.htm")
        with open(save_path, 'w') as fp:
            fp.write(description)

    return output


def saveSpells(spells: list[SpellLink]):
    data = {}
    for i, link in enumerate(spells):
        try:
            data[link.id] = getSpellInfo(link)
        except Exception as err:
            print(f"ERROR: Unable to getSpellInfo for spells[{i}] = {link}")
            raise err

    output_path = os.path.join(
        abs_path_to_repo, 'spells', 'spells.json')
    with open(output_path, 'w') as fp:
        json.dump(data, fp, indent=2)
        fp.write('\n')


def main():
    with open(path_for_spell_descriptions) as fp:
        soup = BeautifulSoup(fp, 'lxml')

    srd_spell_links: list[SpellLink] = []
    for link in soup.find_all('a'):
        if link.get('class') == None:
            continue
        elif link.get('class') == ['toc0']:
            srd_spell_links.append(SpellLink(link))
        elif link.get('class') == ['toc1']:
            srd_spell_links[-1].addSubLink(link)
        else:
            continue

    DEBUG_SPELL_PROCESSING = False
    if DEBUG_SPELL_PROCESSING:
        print(getSpellInfo(srd_spell_links[0]))
        print(getSpellInfo(srd_spell_links[1]))
        # print(getSpellInfo(srd_spell_links[10]))
        # print(getSpellInfo(srd_spell_links[12]))
        # print(getSpellInfo(srd_spell_links[33]))
        print(getSpellInfo(srd_spell_links[42]))
        # print(getSpellInfo(srd_spell_links[59]))
        # print(getSpellInfo(srd_spell_links[64]))
        # print(getSpellInfo(srd_spell_links[260]))
        print("Spell processing DEBUG complete!")
    else:
        saveSpells(srd_spell_links)
        print("Spell processing complete!")


if __name__ == "__main__":
    main()
