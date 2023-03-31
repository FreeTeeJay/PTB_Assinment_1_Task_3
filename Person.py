import pika
import random
import time

# Parse command-line arguments
middleware_endpoint = sys.argv[1]
person_id = sys.argv[2]
movement_speed = int(sys.argv[3])

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(middleware_endpoint))
channel = connection.channel()

# Create the person's initial position
x = random.randint(0, 9)
y = random.randint(0, 9)
position = f'{x},{y}'.encode()

# Publish the initial position to the 'position' topic
channel.basic_publish(exchange='',
                      routing_key='position',
                      body=person_id.encode() + b',' + position)

# Continuously move to a random adjacent square and publish the new position
while True:
    # Choose a random direction to move in
    dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    # Calculate the new position, taking into account boundary conditions
    new_x = max(min(x + dx, 9), 0)
    new_y = max(min(y + dy, 9), 0)

    # Publish the new position to the 'position' topic
    position = f'{new_x},{new_y}'.encode()
    channel.basic_publish(exchange='',
                          routing_key='position',
                          body=person_id.encode() + b',' + position)

    # Wait for the specified amount of time before making the next move
    time.sleep(1 / movement_speed)

