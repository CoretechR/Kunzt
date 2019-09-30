import sys
import os
import io
import PyPDF2

#filepath = "Speiseplan Kunzmann.pdf"
filepath = sys.argv[1]

text_file = io.open("Speiseplan.txt", "w", encoding='utf-8')

pdf_file = open(filepath, 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
page = read_pdf.getPage(0)
text = page.extractText()

text = text.replace('•', '€')

weekPos = text.find('Woc')
print(text[weekPos-3:weekPos+5])
print(text[weekPos-3:weekPos+5], file=text_file)
for i in range(20):
  if text[weekPos+3+i].isdigit():
    for n in range(20):
      if text[weekPos + 28 + n] == ' ':
        print(text[weekPos+3+i:weekPos+28+n])
        print(text[weekPos+3+i:weekPos+28+n], file=text_file)
        print('', file=text_file)
        break
    break

weekDays = ['Monta', 'Diensta', 'Mittwoc', 'Donnersta', 'Freita', 'Zusatz']

for d in range(0, 5):
  dayPos = text.find(weekDays[d])
  dayEnd = dayPos+16+text[dayPos+16:].find(' ')
  print(text[dayPos:dayEnd])
  print(text[dayPos:dayEnd], file=text_file)
  for i in range(dayEnd, dayEnd+20):
    if text[i].isalpha():
      mealPos = i
      mealEnd = text[mealPos:mealPos+10].find("Feiert")
      if mealEnd > -1:
        print(text[mealPos:mealPos+mealEnd + 8])
        print(text[mealPos:mealPos+mealEnd + 8], file=text_file)
      else: # no holiday
        nextDay = mealPos+text[mealPos:].find(weekDays[d+1])
        mealEnd = [n for n, x in enumerate(text[mealPos:nextDay]) if x == '€']
        if mealPos+mealEnd[1] > nextDay:
          print(text[mealPos:mealPos+mealEnd[1]+1])
          print(text[mealPos:mealPos+mealEnd[1]+1], file=text_file)
        else:
          print(text[mealPos:nextDay])
          print(text[mealPos:nextDay], file=text_file)
        #if len(mealEnd) > 2:
        #  print(text[mealPos + mealEnd[1] + 1:mealPos + mealEnd[3] + 1])
      break


#text = text[weekPos-3:]

#print(text)


text_file.close()