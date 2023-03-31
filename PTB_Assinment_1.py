import pika

# Create a dictionary to store each person's current position
positions = {}

# Create a set to store pairs of people who have occupied the same position
collisions = set()

def position_callback(ch, method, properties, body):
    # Parse the received message
    person, x, y = body.split(b',')

    # Store the person's current position
    positions[person] = (int(x), int(y))

    # Check for collisions
    for other_person, other_position in positions.items():
        if other_person != person and other_position == positions[person]:
            collision_pair = tuple(sorted((person.decode(), other_person.decode())))
            collisions.add(collision_pair)
    
def query_callback(ch, method, properties, body):
    # Parse the received message
    person = body.decode()

    # Find all people that the requested person has collided with
    contacts = [p for p1, p2 in collisions if p1 == person or p2 == person]

    # Send the response back on the 'query-response' topic
    response = ', '.join(contacts).encode()
    channel.basic_publish(exchange='',
                          routing_key='query-response',
                          body=response)

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create the 'position' and 'query' topics if they don't already exist
channel.queue_declare(queue='position')
channel.queue_declare(queue='query')
channel.queue_declare(queue='query-response')

# Set up the position and query message consumers
channel.basic_consume(queue='position', on_message_callback=position_callback, auto_ack=True)
channel.basic_consume(queue='query', on_message_callback=query_callback, auto_ack=True)

# Start consuming messages
print('Tracker application started. Waiting for messages...')
channel.start_consuming()

