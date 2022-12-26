from flask import Flask, render_template, request
import pytesseract as tess
import easyocr as ocr  #OCR
tess.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
import requests
from PIL import Image

app = Flask(__name__)

def image_to_text(url):
    img = Image.open(requests.get(url, stream=True).raw)
    text = tess.image_to_string(img)
    return text




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
        reader = ocr.Reader(['en'],model_storage_directory='.')

        result = reader.readtext("outliers.jpeg")

        for text in result:
            result = text[1]
        
       
    except:
        return render_template("error.html", error = "Invalid Url")

    print(text[1])
    return render_template("result.html", result = text[1], url = url)

