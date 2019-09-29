from PIL import Image, ExifTags, ImageFilter
import pytesseract
import sys
import os

#filepath = "IMG_3135.jpg"
filepath = sys.argv[1]
image = Image.open(filepath)

pytesseract.pytesseract.tesseract_cmd = os.getenv('LOCALAPPDATA') + r"\Tesseract-OCR\tesseract.exe"

try:
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
except (AttributeError, KeyError, IndexError):
    # cases: image doesn't have exif
    pass

basewidth = 1200
wpercent = (basewidth / float(image.size[0]))
hsize = int((float(image.size[1]) * float(wpercent)))
image = image.resize((basewidth, hsize), Image.ANTIALIAS)

image = image.convert("L")
threshold = 150
imageBW = image.point(lambda p: p > threshold and 255)
#imageBW.save("imageBW.bmp")
text = pytesseract.image_to_string(image, lang='deu')
#print(text) # debug

text = text.splitlines()


for i in range(20):  # search only top lines
    weekPos = text[i].find('Woc')
    if weekPos != -1:
        weekString = text[i][:weekPos]
        weekString = weekString.translate({ord(i): None for i in ' ,.'})  # remove unnecessary characters
        week = [int(s) for s in weekString.split() if s.isdigit()][0]
        print(str(week) + ". Woche")
        date = text[i + 1]
        print(date)
        print()
        break

weekDays = ['onta', 'iensta', 'ittwoc', 'onnersta', 'reita']

for days in weekDays:
    for i in range(len(text)):
        dayPos = text[i].find(days)
        if dayPos != -1:
            dayString = text[i][dayPos - 1:]
            print(dayString)
            # search the next 10 lines for dishes
            for n in range(i + 1, min(i + 11, len(text))):
                if any(x in text[n] for x in weekDays):  # stop when next day is reached
                    break
                if text[n].find('usatz') != -1: # stop when end of menu is reached
                    break
                elif len(text[n]) > 17: #don't show empty lines
                    dishString = text[n]
                    #clean up beginning of string
                    for offset in range(5):
                        if dishString[offset].isalpha():
                            break
                    dishString = dishString[offset:]
                    print("  ", dishString)
            break

print()