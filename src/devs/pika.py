import pika

# Variables to hold our connection and channel
connection = None
channel = None

# Called when our connection to RabbitMQ is closed
def on_closed(frame):
    global connection

    # connection.ioloop is blocking, this will stop and exit the app
    connection.ioloop.stop()

# Called when we have connected to RabbitMQ
def on_connected(connection):
    global channel

    # Create a channel on our connection passing the on_channel_open callback
    connection.channel(on_channel_open)

# Called after line #110 is finished, when our channel is open
def on_channel_open(channel_):
    global channel

    # Our usable channel has been passed to us, assign it for future use
    channel = channel_

    # Declare a queue
    channel.queue_declare(queue="test", durable=True,
                          exclusive=False, auto_delete=False,
                          callback=on_queue_declared)

# Called when line #119 is finished, our queue is declared.
def on_queue_declared(frame):
    global channel

    # Send a message
    channel.basic_publish(exchange='',
                          routing_key="test",
                          body="Hello World!",
                          properties=pika.BasicProperties(
                            content_type="text/plain",
                            delivery_mode=1))

    # Add a callback so we can stop the ioloop
    connection.add_on_close_callback(on_closed)

    # Close our connection
    connection.close()

# Create our connection parameters and connect to RabbitMQ
parameters = pika.ConnectionParameters('localhost')
connection = pika.SelectConnection(parameters, on_connected)

# Start our IO/Event loop
connection.ioloop.start()
