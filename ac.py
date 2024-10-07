import requests
import json

# Replace with your Zulip credentials
zulip_email = 'szurubooru@gmail.com'  # Your Zulip email
zulip_api_key = 'fgwT5umbrQdW6Y1buIWZJK6S2FVQZAeS'  # Your Zulip API key
zulip_api_url_streams = 'https://szurubooru.zulipchat.com/api/v1/streams'  # Zulip API endpoint for streams
zulip_api_url_messages = 'https://szurubooru.zulipchat.com/api/v1/messages'  # Zulip API endpoint for messages

# Function to retrieve all messages from a stream
def get_all_messages(stream_name):
    messages = []
    params = {
        'anchor': 'newest',
        'num_before': 100,
        'num_after': 0,
        'narrow': json.dumps([{"operator": "stream", "operand": stream_name}]),
    }

    while True:
        response = requests.get(
            zulip_api_url_messages,
            auth=(zulip_email, zulip_api_key),
            params=params
        )

        if response.status_code == 200:
            data = response.json()
            messages.extend(data.get('messages', []))
            if len(data.get('messages', [])) < params['num_before']:
                break  # Exit the loop if there are no more messages
            # Update params for the next batch
            params['anchor'] = messages[-1]['id']  # Set the anchor to the last message ID
        else:
            print("Failed to retrieve messages.")
            print(response.status_code, response.text)
            break

    return messages

# Get available streams
response = requests.get(
    zulip_api_url_streams,
    auth=(zulip_email, zulip_api_key)
)

if response.status_code == 200:
    streams = response.json().get('streams', [])
    print("Available streams:")
    for stream in streams:
        print(stream['name'])  # Print the name of each stream

    # Use the actual stream name retrieved above
    valid_stream_name = 'Szurubooru'  # Replace with the valid stream name you found

    # Retrieve all messages from the specified stream
    all_messages = get_all_messages(valid_stream_name)

    if all_messages:
        print("Received messages:")
        for msg in all_messages:
            print(f"Sender: {msg['sender_email']}, Content: {msg['content']}")
        
        # Save messages to a JSON file
        with open('zulip_messages.json', 'w', encoding='utf-8') as f:
            json.dump(all_messages, f, ensure_ascii=False, indent=4)
        print("Messages saved to zulip_messages.json.")
    else:
        print("No messages found.")
else:
    print("Failed to retrieve streams.")
    print(response.status_code, response.text)
