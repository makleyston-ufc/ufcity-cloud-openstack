from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

# List of interest
available_interests = [
    {'title': 'slow-traffic-forecast', 'description': 'This notification service informs about slow traffic in the city based on weather conditions, time of day, peak hours, accidents, and traffic density.'},
]

client_registrations = []


@app.route('/available-interests', methods=['GET'])
def get_available_interests():
    return jsonify(available_interests)


@app.route('/manage-interests', methods=['POST'])
def manage_interests():

    new_interest = request.json
    available_interests.append(new_interest)

    return jsonify({"message": "Interest added successfully", "interest": new_interest})


@app.route('/register', methods=['POST'])
def register_client():
    data = request.json
    endpoint = data.get('endpoint')
    interests = data.get('interests', [])

    # Verify that the interests provided by the customer are in the list of available interests
    valid_interests = [interest for interest in interests if any(interest == available_interest['title'] for available_interest in available_interests)]

    # Register customer only with valid interests
    client_registrations.append({"endpoint": endpoint, "interests": valid_interests})
    print(f"Registered client: {endpoint} - Interests: {valid_interests}")

    return 'Registration successful!'


@app.route('/trigger-event', methods=['POST'])
def trigger_event():
    event_data = request.json

    # Iterate over client registrations and send data to corresponding interests
    for registration in client_registrations:
        endpoint = registration["endpoint"]
        interests = registration["interests"]

        # Check if there is any interest corresponding to the event
        if event_data["interest"] in interests:

            # POST to the client's endpoint
            client_data = {"interest": event_data["interest"], "data": event_data["data"]}
            print("Sending data to {} with interest {}: {}".format(endpoint, event_data['interest'], client_data))
            response = requests.post(endpoint, json=client_data)

            # Check if the client's response was successful
            if response.status_code == 200:
                print(f"Client response ({endpoint}): {response.text}")
            else:
                print(f"Failed to send data to {endpoint}. Status code: {response.status_code}")

    return 'Event processed and sent to registered endpoints.'


# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=3000)
