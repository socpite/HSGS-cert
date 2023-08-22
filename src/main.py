import sys
import csv
import os
import shutil
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import tqdm

template = PIL.Image.open('assets/template.PNG')
namefont = PIL.ImageFont.truetype('assets/Whitegone.ttf', size=100)
yearfont = PIL.ImageFont.truetype('assets/SFCompactDisplay-Thin.otf', size = 24)
rolefont = PIL.ImageFont.truetype('assets/SVN-ArtifexCF-Bold.ttf', size=35)

def generate_certificate(name: str, roles: list[str], year: str) -> PIL.Image.Image:
    name = name.split("_")[0]
    img = template.copy()
    canvas = PIL.ImageDraw.Draw(img)
    canvas.text((528, 408), name, font = namefont, fill=(0, 0, 0), align="center", anchor="mm")
    canvas.text((608, 485), year, font = yearfont, fill=(0, 0, 0), align="left", anchor="ls")
    canvas.text((678, 485+28), year, font = yearfont, fill=(0, 0, 0), align="left", anchor="ls")

    roles.sort(key = lambda x: len(x), reverse=True)

    for i, role in enumerate(roles):
        canvas.text((528, 485+28+38*(i+1)), role, font = rolefont, fill=(49, 169, 221), align="center", anchor="mm")
        
    return img

def main():
    filename = sys.argv[1]
    output = sys.argv[2]

    shutil.rmtree(output)
    os.mkdir(output)

    with open(filename, "r", encoding="UTF-8") as f:
        csvfile = csv.reader(f)
        data = list(csvfile)
    
    rolelist = {}

    for name, role in data:
        try:
            rolelist[name].append(role)
        except KeyError:
            rolelist[name] = [role]
    for name, rlist in tqdm.tqdm(rolelist.items()):
        img = generate_certificate(name, rlist, "2023")
        img.save(f"{output}/{name}.png")

    print("\n".join([f"{name}: {rlist}" for name, rlist in rolelist.items()]))


if __name__ == "__main__":
    main()
