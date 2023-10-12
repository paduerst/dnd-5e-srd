import json
import os
import re

newlineRegex = re.compile(r'[\n]')
multispaceRegex = re.compile(r'\s{2,}')

abs_path_to_this_folder = os.path.dirname(os.path.abspath(__file__))
path_to_descriptions_folder = os.path.join(
    abs_path_to_this_folder, "descriptions")
path_to_output_file = os.path.join(
    abs_path_to_this_folder, "spell-descriptions.json")


def cleanSpellDescription(description: str):
    output = description.strip()
    output = newlineRegex.sub('', output)
    output = multispaceRegex.sub(' ', output)
    output = output.replace("<p> ", "<p>")
    output = output.replace("<ul> ", "<ul>")
    output = output.replace("<li> ", "<li>")
    output = output.replace(" </li>", "</li>")
    output = output.replace("</li> ", "</li>")
    output = output.replace("<table> ", "<table>")
    output = output.replace("<caption> ", "<caption>")
    output = output.replace(" </caption>", "</caption>")
    output = output.replace("</caption> ", "</caption>")
    output = output.replace("<thead> ", "<thead>")
    output = output.replace("</thead> ", "</thead>")
    output = output.replace("<tbody> ", "<tbody>")
    output = output.replace("<tr> ", "<tr>")
    output = output.replace(" </tr>", "</tr>")
    output = output.replace("</tr> ", "</tr>")
    output = output.replace("<th> ", "<th>")
    output = output.replace(" </th>", "</th>")
    output = output.replace("</th> ", "</th>")
    output = output.replace("<td> ", "<td>")
    output = output.replace(" </td>", "</td>")
    output = output.replace("</td> ", "</td>")
    return output


def main():
    output = {}
    filenames = os.listdir(path_to_descriptions_folder)
    for filename in filenames:
        spell_id = filename.split(".")[0]
        spell_path = os.path.join(path_to_descriptions_folder, filename)
        with open(spell_path, 'r') as fp:
            spell_description = fp.read()
        output[spell_id] = cleanSpellDescription(spell_description)

    with open(path_to_output_file, 'w') as fp:
        json.dump(output, fp, indent=2, sort_keys=True)
        fp.write('\n')

    print("Finished collating spell descriptions!")


if __name__ == "__main__":
    main()
