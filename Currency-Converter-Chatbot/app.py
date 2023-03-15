from flask import Flask, request, jsonify
import requests

app = Flask(__name__) # Creating the Flask object that represents your application

#The __name__ variable passed to the Flask class is a Python predefined variable,
# which is set to the name of the module in which it is used.
# Flask uses the location of the module passed here as a starting point when it needs to load associated resources

@app.route('/', methods = ['POST'])
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
def index():
    data = request.get_json()
    print(data)
    print(type(data))
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    #print(source_currency)
    #print(amount)
    #print(target_currency)

# We need conversion factor for converting currency
    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    response = {
        'fulfillmentText' : '{} {} is {} {}'.format(amount, source_currency, final_amount, target_currency)
    }
    #print(final_amount)
    return response # or return jsonify(response)

# This is the function for fetching the conversion factor.
# For fetching the conversion factor currencyconverter API is used.
# Depending on source and target currency the API gives conversion factor accurately.
def fetch_conversion_factor(source, target):
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=504d38e3aae375ca55e9".format(source, target)

    response = requests.get(url)
    response = response.json()


    return response['{}_{}'.format(source, target)]

if __name__ == "__main__" :
    app.run(debug=True)

# To understand if __name__ == __main__ read https://realpython.com/if-name-main-python/
# To understand the matter in above website
# read https://medium.com/@thomas_k_r/whats-this-weird-arrow-notation-in-python-53d9e293113
