"""
    This program listens for Smoker messages contiously.
    
    Name: Sushma Pamidi 
    Date: 2/12/23
    
    We want know if (Condition To monitor):
    The smoker temperature decreases by more than 15 degrees F in 2.5 minutes (smoker alert!)
    
    Smoker time window is 2.5 minutes
    
    Deque Max Length:
    At one reading every 1/2 minute, the smoker deque max length is 5 (2.5 min * 1 reading/0.5 min)
    
"""

import pika
import sys
import time
from collections import deque

# Create deques to store last messages
# limited to the 5 recent readings
smoker_deque = deque(maxlen=5)


# define a callback function for Smoker to be called when a message is received
def smoker_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received in Smoker Consumer {body.decode()}")

    #Append to deque 
    smoker_deque.append(body.decode())


    #Current items in queue
    smoker_current = body.decode()

    # Current Date timestamp
    smoker_current_date_time = smoker_current.split(",")
    #print(f" [x] Current in queue:  {smoker_current_date_time}")

    # Current temp
    smoker_current_temp = float("0.0" if smoker_current_date_time[1] == 'Channel1' or smoker_current_date_time[1] == '' else smoker_current_date_time[1]) 
    #print(f" [x] Current temp:  {smoker_current_temp}")
   
    if len(smoker_deque) == 5:
        if smoker_current_temp > 1:
            # First item from 2.5 min ago
            smoker_oldest = smoker_deque[0]

            #Smoker Date timestamp from 2.5 min ago
            smoker_oldest_date_time = smoker_oldest.split(",")
            print(f" [x] Oldest in queue:  {smoker_oldest_date_time}")

            #Smoker temp from 2.5 min ago
            smoker_oldest_temp = float("0.0" if smoker_oldest_date_time[1] == 'Channel1' or smoker_oldest_date_time[1] == '' else smoker_oldest_date_time[1])
            print(f" [x] Oldest temp:  {smoker_oldest_temp}")

            if smoker_oldest_temp > 1 and smoker_oldest_temp - smoker_current_temp >= 15:
                print("Current smoker temp is:", smoker_current_temp,";", "Smoker temp change in last 2.5 minutes is:", smoker_oldest_temp)
                print(f">>> Smoker alert! The temperature of the smoker has decreased more than 15 F in 2.5 min")
            else:
                print("Current smoker temp is:", smoker_current_temp,";", "Smoker temp change in last 2.5 minutes is:", smoker_oldest_temp)
    else:
        print(f" [x] Current smoker temp is:", smoker_current_temp)

    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


# define a main function to run the program
def main(hn: str = "localhost", qn: str = "01-smoker"):
    """ Continuously listen for task messages on a named queue."""

    # when a statement can go wrong, use a try-except block
    try:
        # try this code, if it works, keep going
        # create a blocking connection to the RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))

    # except, if there's an error, do this
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)

    try:
        # use the connection to create a communication channel
        channel = connection.channel()

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        channel.queue_declare(queue=qn, durable=True)

        # The QoS level controls the # of messages
        # that can be in-flight (unacknowledged by the consumer)
        # at any given time.
        # Set the prefetch count to one to limit the number of messages
        # being consumed and processed concurrently.
        # This helps prevent a worker from becoming overwhelmed
        # and improve the overall system performance. 
        # prefetch_count = Per consumer limit of unaknowledged messages      
        channel.basic_qos(prefetch_count=1) 

        # configure the channel to listen on a specific queue,  
        # use the callback function named callback,
        # and do not auto-acknowledge the message (let the callback handle it)
        channel.basic_consume(queue=qn, on_message_callback=smoker_callback)

        # print a message to the console for the user
        #print(" [*] Ready for work. To exit press CTRL+C")

        # start consuming messages via the communication channel
        channel.start_consuming()

    # except, in the event of an error OR user stops the process, do this
    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        #print("\nClosing connection. Goodbye.\n")
        #channel.queue_delete(qn)
        connection.close()


# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":
    # call the main function with the information needed
    main("localhost", "01-smoker")
