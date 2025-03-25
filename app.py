from flask import Flask, flash, redirect, render_template, request, session
from pypdf import PdfReader as read
import re
import os
from pdf2image import convert_from_path

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
@app.route("/results", methods=["GET", "POST"])
def results():
    # try:
    for file in os.listdir("static/images"):
        os.remove(f"static/images/{file}")
    subject = request.args.get("subject")
    unit = re.sub("Unit ", "", request.args.get("unit"))
    if subject != "Physics" and subject != "Chemistry":
        subject = "Maths"
        module = request.args.get("subject")
    search = request.args.get("search")

    name = ""
    page = ""
    results = []
    if subject == "Maths":
        for file in os.listdir(f"static/Papers/{subject}/{module}/Unit {unit}"):
            if file[len(file)-3:len(file)] == "txt" and file[len(file)-6:len(file)-4] != "MS":
                QP = open(f"static/Papers/{subject}/{module}/Unit {unit}/{file}", "r", encoding="utf-8")
                content = QP.read()    
                content = re.sub(" ", "", content)
                search = re.sub(" ", "", search)
                if content.find(search) != -1:
                    for index in range(content.find(search), len(content)):
                        if content[index: index + 15] == "-----EndofPage:":
                            page = content[index + 15]
                            if content[index + 16] != "-":
                                page = page + content[index + 16]
                                break
                            else:
                                break
                    name = re.sub(".txt", "", file)
                    if name == "Sample Assessment":
                        page = int(page) + 1
                    else:
                        page = int(page) + 1
                    pdf_path = f"static/Papers/{subject}/{module}/Unit {unit}/{name}.pdf"
                    image = convert_from_path(pdf_path, dpi = 300, first_page=int(page), poppler_path=r"bin")
                    image[0].save(f"static/images/{name} pg{page}.png", 'PNG')            
                    results.append([name, page, f"static/images/{name} pg{page}.png", pdf_path, re.sub(".pdf", " MS.pdf", pdf_path)])
    else:
        for file in os.listdir(f"static/Papers/{subject}/Unit {unit}"):
            if file[len(file)-3:len(file)] == "txt" and file[len(file)-6:len(file)-4] != "MS":
                QP = open(f"static/Papers/{subject}/Unit {unit}/{file}", "r", encoding="utf-8")
                content = QP.read()    
                content = re.sub(" ", "", content)
                search = re.sub(" ", "", search)
                if content.find(search) != -1:
                    for index in range(content.find(search), len(content)):
                        if content[index: index + 15] == "-----EndofPage:":
                            page = content[index + 15]
                            if content[index + 16] != "-":
                                page = page + content[index + 16]
                                break
                            else:
                                break
                    name = re.sub(".txt", "", file)
                    if name == "Sample Assessment":
                        page = int(page) + 2
                    else:
                        page = int(page) + 1
                    pdf_path = f"static/Papers/{subject}/Unit {unit}/{name}.pdf"
                    image = convert_from_path(pdf_path, dpi = 300, first_page=int(page), poppler_path=r"bin")
                    image[0].save(f"static/images/{name} pg{page}.png", 'PNG')            
                    results.append([name, page, f"static/images/{name} pg{page}.png", pdf_path, re.sub(".pdf", " MS.pdf", pdf_path)])
    if name == "" and page == "":
        return render_template("error.html", txt="Nothing found")
    else:
        return render_template("results.html", results = results)

if __name__ == '__main__':  
   app.run()