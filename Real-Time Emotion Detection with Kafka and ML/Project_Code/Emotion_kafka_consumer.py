from kafka import KafkaConsumer
import json

# Set up the Kafka consumer
consumer = KafkaConsumer(
    'emotion-detection-stream',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,  # Disable automatic offset commits
    group_id=None  # Disable consumer group for reading from the beginning
)

try:
    # Open the file for reading
    with open('offset/external_offset.txt', 'r') as file:
        # Read the content of the file
        file_content = file.read()

        # Convert the content to an integer
        last_offset = int(file_content)

        # Print the integer value
        print("Last processed offset:", last_offset)

except FileNotFoundError:
    print("File not found. Please make sure the file exists.")
except ValueError:
    print("Error: The content of the file is not a valid integer.")
except Exception as e:
    print(f"An error occurred: {e}")


# Consume and print incremental messages
for message in consumer:
    if message.offset > last_offset or last_offset ==0 :
        print(f"Received message: {message.value.decode('utf-8')}, Offset: {message.offset}")
        
        json_string = message.value.decode('utf-8')
        data = json.loads(json_string)
        tweet = data.get('value', None)
        print(tweet)
        
        
        try:
    # Open the file for writing
            with open('Tweets_Input/tweets.txt', 'a') as file:
                # Append the content to a new line
                file.write('\"'+tweet + '\"' + '\n')
                
            with open('offset/external_offset.txt', 'w') as file:
                file.write(str(message.offset))
            

            


        except Exception as e:
            print(f"An error occurred: {e}")


# Close the consumer
consumer.close()