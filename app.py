from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the hospital data from a CSV file
hospitals_df = pd.read_csv('hospital_data.csv')


# Define the model function to predict the best hospitals based on user input
def predict_hospitals(beds, oxy_cyl, ventilators, staff, doctors, severity, distance):
    # Filter hospitals based on distance
    nearby_hospitals_df = hospitals_df[hospitals_df['distance'] <= distance]

    # Check if there are any hospitals within the specified distance
    if nearby_hospitals_df.empty:
        return "No hospitals found within the specified distance."

    # Filter hospitals based on the input criteria and sort by distance
    filtered_hospitals_df = nearby_hospitals_df[
        (nearby_hospitals_df['beds'] >= beds) &
        (nearby_hospitals_df['oxy_cyl'] >= oxy_cyl) &
        (nearby_hospitals_df['ventilators'] >= ventilators) &
        (nearby_hospitals_df['staff'] >= staff) &
        (nearby_hospitals_df['doctors'] >= doctors) &
        (nearby_hospitals_df['severity'] == severity)
    ].sort_values(by='distance')

    # Convert the filtered hospitals DataFrame to a list of dictionaries
    hospitals_list = filtered_hospitals_df.to_dict(orient='records')

    return hospitals_list





# Define a route to render the form
@app.route('/')
def form():
    return render_template('home.html')


# Define a route to handle form submissions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input parameters from the form submission
    beds = int(request.form['beds'])
    oxy_cyl = int(request.form['oxy_cyl'])
    ventilators = int(request.form['ventilators'])
    staff = int(request.form['staff'])
    doctors = int(request.form['doctors'])
    severity = request.form['severity']
    distance = int(request.form['distance'])

    # Validate the distance input field
    if not distance:
        return jsonify({'error': 'Distance field is empty'})
    try:
        distance = int(distance)
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid distance value'})

    # Call the model function to predict the best hospital
    best_hospitals = predict_hospitals(beds, oxy_cyl, ventilators, staff, doctors, severity, distance)

    if isinstance(best_hospitals, str):
        return best_hospitals
    else:
        return render_template('result.html', best_hospitals=best_hospitals)        

if __name__ == '__main__':
    app.run(debug=True)
