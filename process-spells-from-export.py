import os
import re
from bs4 import BeautifulSoup


normalizationRegex = re.compile('[^a-z\-]')


def normalizeString(string: str):
    return normalizationRegex.sub('', string.lower().strip().replace(' ', '-'))


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


rel_path_to_parts_folder = os.path.join(
    "exported-from-adobe", "SRD5.1-CCBY4.0_License_live links_files")
file_name_for_spell_descriptions = "part646.htm"
path_for_spell_descriptions = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), rel_path_to_parts_folder, file_name_for_spell_descriptions)

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

print(srd_spell_links)
