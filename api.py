from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET', 'POST'])
def home():
     # If a form is submitted
    if request.method == "POST":
        url = request.form.get("url")
        prediction = url
    else:
        prediction = ""
        
    return render_template("index.html", output = prediction)


# http://127.0.0.1:5000/api
@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(books)

# http://127.0.0.1:5000/api?id=1
@app.route('/api', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []

    for book in books:
        if book['id'] == id:
            results.append(book)

    return jsonify(results)

app.run()