from bs4 import BeautifulSoup
import requests
import json

MAIN_URL = "https://linasm.sourceforge.net/docs/instructions/"
CATEGORIES = ["cpu.php", "fpu.php", "simd.php", "aes.php", "mpx.php", "smx.php", "tsx.php", "vmx.php"]
OUTPUT_FILE_NAME = "../x86-64_instructions.json"


instructions = {"instructions": []}
for category in CATEGORIES:
    url = f"{MAIN_URL}{category}"
    page = BeautifulSoup(requests.get(url).text, features="lxml")
    category_description = page.h1.text
    sections = page.find_all("section")
    if len(sections) == 1:
        start_index = 0
    else:
        start_index = 1
    for i in range(start_index, len(sections)):
        group = sections[i].h1.text
        instruction_records = sections[i].tbody.find_all("tr")
        for instruction_record in instruction_records:
            if instruction_record.td is not None:
                instructions["instructions"].append(
                    {
                        "instruction": instruction_record.th.text,
                        "category": category_description,
                        "group": group,
                        "description": instruction_record.td.text,
                    }
                )

with open(OUTPUT_FILE_NAME, "w") as file:
    json.dump(instructions, file, indent=4)
