import csv
import os
from pathlib import Path
import re
import time

from lxml import etree
import requests
import shutil

NS = {
    "x": "http://www.loc.gov/mods/v3",
}


def get_value_by_xpath(xml_tree, xpath):
    try:
        return xml_tree.xpath(
            xpath,
            namespaces=NS,
        )[0]
    except IndexError:
        return ""


# Takes an array of potential xpaths, returns the first one that matches,
# or the empty string
def get_value_by_xpaths(xml_tree, xpaths):
    for xpath in xpaths:
        value = get_value_by_xpath(xml_tree, xpath)
        if value != "":
            return value
    return value


def main():
    if not os.path.exists("cache"):
        os.mkdir("cache")

    if not os.path.exists("../menuez_images"):
        os.mkdir("../menuez_images")

    metadata_file = open("../metadata/menuez_all.txt", "w", encoding="utf-8")

    with_captions_file = open("../metadata/menuez.txt", "w", encoding="utf-8")

    metadata_file.write(
        "filename\ttitle\tartist\tplace\tdate\tcaption\tdescription\tpermalink\timage_url\n"
    )
    with_captions_file.write(
        "filename\ttitle\tartist\tplace\tdate\tcaption\tdescription\tpermalink\timage_url\n"
    )

    with open("menuez.csv", mode="r", encoding="utf-8") as data_file:
        csvFile = csv.DictReader(data_file)

        for line in csvFile:
            druid = line["Druid"]
            title = line["Title"]
            xml_filepath = Path(f"cache/{druid}.xml")
            if not xml_filepath.exists():
                xmldata = requests.get(f"https://purl.stanford.edu/{druid}.xml")
                with open(xml_filepath, "w", encoding="utf-8") as xmlfile:
                    xmlfile.write(xmldata.text)

            xml_data = xml_filepath.open("r", encoding="utf-8").read()

            try:
                content_xml = xml_data.split(r"<contentMetadata")[1].split(
                    r"</contentMetadata"
                )[0]
                image_xml = (
                    content_xml.split(r"<resource")[1].split(r"<file")[1].strip()
                )
                image_match = re.match(r"id=(\S*)\s", image_xml, flags=re.MULTILINE)
                original_image = image_match.group(1).replace('"', "")

                mods_xml = (
                    "<mods"
                    + xml_data.split(r"<mods")[1].split(r"</mods>")[0]
                    + "</mods>"
                )
                xml_tree = etree.fromstring(mods_xml)

            except Exception as e:
                print("UNABLE TO PARSE XML FOR", druid)
                continue

            caption = get_value_by_xpath(
                xml_tree, "x:titleInfo[@displayLabel='Caption']/x:title/text()"
            )

            date = get_value_by_xpath(
                xml_tree,
                "x:originInfo/x:dateCreated/text()",
            )

            image_path_base = f"{druid}/{original_image}".replace(".jp2", "")

            image_filename = f"{druid}_{original_image.replace('.jp2', '')}.jpg"

            image_url = f"https://stacks.stanford.edu/image/iiif/{image_path_base}/full/full/0/default.jpg"

            print("Getting image", image_url)

            if not os.path.isfile(f"../menuez_images/{image_filename}"):
                response = requests.get(image_url)
                with open(f"../menuez_images/{image_filename}", "wb") as out_file:
                    out_file.write(response.content)
                del response
                time.sleep(1)

            outstr = (
                "\t".join(
                    [
                        f"{image_filename}",
                        title,
                        "Douglas Menuez",
                        "",
                        date,
                        caption,
                        "",
                        f"https://purl.stanford.edu/{druid}",
                        image_url,
                    ]
                )
                + "\n"
            )

            metadata_file.write(outstr)
            if caption != "":
                with_captions_file.write(outstr)

    metadata_file.close()


if __name__ == "__main__":
    main()
