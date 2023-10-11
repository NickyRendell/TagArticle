
from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
import article.TagArticle.Artifacts.OldMain2 as OldMain2
# import other scripts if needed

app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "admin": "Willmore",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    if request.method == 'POST':
        url = request.form['url']
        results = OldMain2.categorise_url(url)  # assuming your main module has a function like this
        
        return render_template('index.html', results=results, url=url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()