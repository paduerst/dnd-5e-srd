import json
import os
import re
from typing import TypedDict

from bs4 import BeautifulSoup

normalizationRegexDash = re.compile('[ \/]')
normalizationRegexEmpty = re.compile('[^a-z\-]')

abs_path_to_repo = os.path.dirname(os.path.abspath(__file__))

rel_path_to_parts_folder = os.path.join(
    "exported-from-adobe", "SRD5.1-CCBY4.0_License_live links_files")
abs_path_to_parts_folder = os.path.join(
    abs_path_to_repo, rel_path_to_parts_folder)

file_name_for_spell_descriptions = "part646.htm"
path_for_spell_descriptions = os.path.join(
    abs_path_to_parts_folder, file_name_for_spell_descriptions)


def normalizeString(string: str):
    string_with_dashes = normalizationRegexDash.sub(
        '-', string.lower().strip())
    return normalizationRegexEmpty.sub('', string_with_dashes)


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
    ritual: bool


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
    if subheading_arr[-1] == "(ritual)":
        output["ritual"] = True
        subheading_arr.pop()
    else:
        output["ritual"] = False
    if subheading[0].isdigit():
        output["level"] = int(subheading[0])
        output["school"] = subheading_arr[-1].capitalize()
    else:
        output["level"] = 0
        output["school"] = subheading_arr[0]

    # soup2 contains the rest, starting with components
    path_to_part2 = path_to_part1
    if link.subLink != None:
        path_to_part2 = os.path.join(abs_path_to_parts_folder, link.subLink)
    with open(path_to_part2) as fp:
        soup2 = BeautifulSoup(fp, 'lxml')
    # print(soup2.prettify())

    return output


def saveSpells(spells: list[SpellLink]):
    data = {}
    for link in spells:
        data[link.id] = getSpellInfo(link)
    output_path = os.path.join(
        abs_path_to_repo, 'spells', 'spells.json')
    with open(output_path, 'w') as fp:
        json.dump(data, fp, indent=2)


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

    saveSpells(srd_spell_links)


if __name__ == "__main__":
    main()
