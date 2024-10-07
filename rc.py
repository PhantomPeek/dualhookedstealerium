import requests
import json

# Replace with your Zulip credentials
zulip_email = 'szurubooru@gmail.com'  # Your Zulip email
zulip_api_key = 'fgwT5umbrQdW6Y1buIWZJK6S2FVQZAeS'  # Your Zulip API key
zulip_api_url_streams = 'https://szurubooru.zulipchat.com/api/v1/streams'  # Zulip API endpoint for streams
zulip_api_url_messages = 'https://szurubooru.zulipchat.com/api/v1/messages'  # Zulip API endpoint for messages

# Get available streams
response = requests.get(
    zulip_api_url_streams,
    auth=(zulip_email, zulip_api_key)  # Use your Zulip email and API key for basic auth
)

if response.status_code == 200:
    streams = response.json().get('streams', [])
    print("Available streams:")
    for stream in streams:
        print(stream['name'])  # Print the name of each stream

    # Use the actual stream name retrieved above
    valid_stream_name = 'Szurubooru'  # Replace with the valid stream name you found

    # Parameters for the message retrieval API call
    params = {
        'anchor': 'newest',
        'num_before': 100,
        'num_after': 0,
        'narrow': json.dumps([{"operator": "stream", "operand": valid_stream_name}])
    }

    # Make the GET request to retrieve messages
    response = requests.get(
        zulip_api_url_messages,
        auth=(zulip_email, zulip_api_key),  # Use your Zulip email and API key for basic auth
        params=params  # Send parameters with the request
    )

    # Check the response for messages
    if response.status_code == 200:
        messages = response.json().get('messages', [])
        if messages:
            print("Received messages:")
            for msg in messages:
                print(f"Sender: {msg['sender_email']}, Content: {msg['content']}")
        else:
            print("No messages found.")
    else:
        print("Failed to retrieve messages.")
        print(response.status_code, response.text)

else:
    print("Failed to retrieve streams.")
    print(response.status_code, response.text)
