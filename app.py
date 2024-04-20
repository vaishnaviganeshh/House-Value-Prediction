import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
pkl_file = open('model.pkl','rb')
model = pickle.load(open('model.pkl', 'rb'))
index_dict = pickle.load(pkl_file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        result = request.form

        index_dict = pickle.load(open('cat','rb'))
        location_cat = pickle.load(open('location_cat','rb'))

        new_vector = np.zeros(151)  # Assuming the length of your feature vector is 151

        result_location = result['location']

        if result_location not in location_cat:
            new_vector[146] = 1
        else:
            new_vector[index_dict[str(result['location'])]] = 1

        new_vector[index_dict[str(result['area'])]] = 1

        new_vector[0] = result['sqft']
        new_vector[1] = result['bath']
        new_vector[2] = result['balcony']
        new_vector[3] = result['size']

        approved = result['approved']

        new = [new_vector]

        if approved == 'Yes':
            # Make prediction if approved
            prediction = model.predict(new)
            return render_template('index.html', Predict_score=' ₹ {}lakhs'.format(prediction))
        else:
            # Return 'DON'T BUY' if not approved
            return render_template('index.html', Predict_score="DON'T BUY")


if __name__ == "__main__":
    app.run(debug=True)
