# importing the modules
import PyPDF2
import pyttsx3
import os
gradePath = ''
# path of the PDF file
filelst=os.listdir(gradePath)
for file in filelst:
    try:
        filename = gradePath + file
        path = open(filename, 'rb')
        
        # creating a PdfFileReader object
        pdfReader = PyPDF2.PdfFileReader(path)
        
        # the page with which you want to start
        # this will read the page of 25th page.
        i = 0
        fullText = ''
        while i < 15:
            try:
                from_page = pdfReader.getPage(i)
                # extracting the text from the PDF
                text = from_page.extractText()
                fullText += text
                i = i+1
            except:
                print(f"No page {i}")
                i = 15
        # reading the text
        fullText = fullText.replace('\n', ' ')
        speak = pyttsx3.init()
        name = file.split('_')
        savePath = gradePath+name[0]+'.mp3'
        speak.save_to_file(fullText, savePath)
        speak.runAndWait()
    except Exception as e:
        print(e)