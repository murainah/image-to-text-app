from flask import Flask, render_template, request
import pytesseract as tess
import easyocr as ocr  
tess.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
import requests
from PIL import Image

app = Flask(__name__)

def image_from_url(url):
    img = Image.open(requests.get(url, stream=True).raw)
    return img


@app.route('/')
def root():
    #Homepage to take input
    return render_template("index.html")

@app.route('/result', methods=["POST", "GET"])
def result():
    url = ""
    results = ""
    #getting url ussing a get request
    if request.method == "GET":
        url = request.args.get("url"," ")
    else:
        #Getting from the POST method
        url = request.form.get("url")

    #Error Handling
    if url == " " or not url :
        return render_template("error.html", error = "No url Found!")
 
    final_text = []
    try:
        img = image_from_url(url)
        reader = ocr.Reader(['en'],model_storage_directory='.')

        result = reader.readtext(img)

        for text in result:
            final_text.append(text[1])
        
    except:
        return render_template("error.html", error = "Invalid Url")

    print(text)
    return render_template("result.html", result = final_text, url = url)



