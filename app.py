from flask import Flask, request, jsonify, render_template
import os
from static.PY.Product_scrapper import Scrapper

app = Flask(__name__)
app.template_folder = 'static/HTML'

# Endpoint raíz que devuelve un mensaje de bienvenida
@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')

@app.route('/Scrapping', methods=['POST'])
def exe_scrappeo():
    test = Scrapper(
        URL     = request.form['url'],
        verbose = True,
        daemon  = True,
    )
    dictionary = test.get_all_attributes()
    name = dictionary["name"]
    price = dictionary["prices"]
    images = dictionary["images"]
    description = dictionary["descriptions"]
    return render_template('scrapped_page.html',name=name,price=price,images=images,description=description)

if __name__ == '__main__':
    print("STARTING THE SERVER...")
    app.run()