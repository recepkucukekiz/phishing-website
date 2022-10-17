from flask import Flask, request, render_template
import numpy as np
import pickle
from URLfeature import *

app = Flask(__name__)
app.config["DEBUG"] = True

def featureExtraction(test_url):
    feature_result = []
    test_domain = getDomain(test_url)

    feature_result.append(havingIP(test_url))
    feature_result.append(getLength(test_domain))
    feature_result.append(tinyURL(test_url))
    feature_result.append(redirection(test_url))
    feature_result.append(httpDomain(test_url))
    feature_result.append(web_traffic(test_url))
    feature_result.append(ServerFormHandler(test_url))
    feature_result.append(UsingPopupWindow(test_url))
    feature_result.append(domainAge(test_domain))
    feature_result.append(domainEnd(test_domain))
    feature_result.append(NonStdPort(test_domain))
    feature_result.append(forwarding(test_url))
    feature_result.append(rightClick(test_url))

    return feature_result

def decetion(url):
    computed = featureExtraction(url)
    return np.array([computed])

@app.route('/', methods=['GET', 'POST'])
def home():
     # If a form is submitted
    if request.method == "POST":
        url = request.form.get("url")

        if len(url) == 0:
          prediction = ""
          return render_template("index.html", output = prediction)

        model = pickle.load(open("XGBV2.pickle.dat", "rb"))

        decetion_result = decetion(url)
        prediction = model.predict(decetion_result)[0]

        if prediction == 1:
            prediction_result = "SAFE"
        else:
            prediction_result = "UNSAFE"

        prediction = prediction_result
    else:
        prediction = ""
        
    return render_template("index.html", output = prediction)


# # http://127.0.0.1:5000/api
# @app.route('/api/all', methods=['GET'])
# def api_all():
#     return jsonify(
#         {
#             'id': 0,
#             'title': 'A Fire Upon the Deep',
#             'author': 'Vernor Vinge',
#             'first_sentence': 'The coldsleep itself was dreamless.',
#             'year_published': '1992'
#         },
#         {
#             'id': 1,
#             'title': 'The Ones Who Walk Away From Omelas',
#             'author': 'Ursula K. Le Guin',
#             'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#             'published': '1973'
#         },
#         {
#             'id': 2,
#             'title': 'Dhalgren',
#             'author': 'Samuel R. Delany',
#             'first_sentence': 'to wound the autumnal city.',
#             'published': '1975'
#         }
#      )

# # http://127.0.0.1:5000/api?id=1
# @app.route('/api', methods=['GET'])
# def api_id():
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     results = []
#     books = [
#                 {
#                     'id': 0,
#                     'title': 'A Fire Upon the Deep',
#                     'author': 'Vernor Vinge',
#                     'first_sentence': 'The coldsleep itself was dreamless.',
#                     'year_published': '1992'
#                 },
#                 {
#                     'id': 1,
#                     'title': 'The Ones Who Walk Away From Omelas',
#                     'author': 'Ursula K. Le Guin',
#                     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#                     'published': '1973'
#                 },
#                 {
#                     'id': 2,
#                     'title': 'Dhalgren',
#                     'author': 'Samuel R. Delany',
#                     'first_sentence': 'to wound the autumnal city.',
#                     'published': '1975'
#                 }
#             ]
    
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     return jsonify(results)

app.run()