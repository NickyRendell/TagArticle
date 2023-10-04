
from flask import Flask, render_template, request, jsonify
import main
# import other scripts if needed

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        results = main.categorise_url(url)  # assuming your main module has a function like this
        
        return render_template('index.html', results=results, url=url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()