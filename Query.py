import argparse
import pika

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Query the tracker for people who came into contact with a specific person.')
parser.add_argument('endpoint', help='the RabbitMQ endpoint to connect to')
parser.add_argument('person_id', help='the identifier of the person to query')
args = parser.parse_args()

# Set up the connection to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(args.endpoint))
channel = connection.channel()

# Set up the query-response queue and subscribe to it
result = channel.queue_declare('', exclusive=True)
callback_queue = result.method.queue
channel.basic_consume(queue=callback_queue, on_message_callback=lambda ch, method, props, body: print(body.decode()))

# Publish the query message to the query queue
channel.basic_publish(
    exchange='',
    routing_key='query',
    body=args.person_id,
    properties=pika.BasicProperties(
        reply_to=callback_queue
    )
)

# Wait for the response
connection.process_data_events()

# Close the connection
connection.close()

