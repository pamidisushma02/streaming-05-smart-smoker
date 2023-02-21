"""
    This program listens for Food A messages contiously.
    
    Name: Sushma Pamidi
    Date: 2/12/23
   
    We want know if (Condition To monitor):
    Food A temperature changes less than 1 degree F in 10 minutes (food stall!)
    
    Time Windows:
    Food time window is 10 minutes
    
    Deque Max Length:
    At one reading every 1/2 minute, the food deque max length is 20 (10 min * 1 reading/0.5 min) 
    
    Listening queue: 02-food-A
    
"""

import pika
import sys
import time
from collections import deque

# Create deques to store last messages

# limited to the 20 most recent readings
foodA_deque = deque(maxlen=20)



# define a callback function for Food A to be called when a message is received
def foodA_callback(ch, method, properties, body):
    """ Define behavior on getting a message."""
    # decode the binary message body to a string
    print(f" [x] Received in foodA Queue {body.decode()}")

    #Append to deque 
    foodA_deque.append(body.decode())

    #Current items in queue
    foodA_current = body.decode()

    # Current Date timestamp
    foodA_current_date_time = foodA_current.split(",")
    #print(f" [x] Current in queue:  {smoker_current_date_time}")

    # Current temp
    foodA_current_temp = float("0.0" if foodA_current_date_time[1] == 'Channel2' or foodA_current_date_time[1] == '' else foodA_current_date_time[1]) 
    #print(f" [x] Current temp:  {smoker_current_temp}")
   
    if len(foodA_deque) == 20:
        if foodA_current_temp > 1:
            # First item from 10 min ago
            foodA_oldest = foodA_deque[0]

            #Food A Date timestamp from 10 min ago
            foodA_oldest_date_time = foodA_oldest.split(",")
            print(f" [x] Oldest in queue:  {foodA_oldest_date_time}")

            #Food A temp from 10 min ago
            foodA_oldest_temp = float("0.0" if foodA_oldest_date_time[1] == 'Channel2' or foodA_oldest_date_time[1] == '' else foodA_oldest_date_time[1])
            print(f" [x] Oldest temp:  {foodA_oldest_temp}")

            if foodA_oldest_temp > 1 and foodA_oldest_temp - foodA_current_temp <= 1:
                print("Current Food A temp is:", foodA_current_temp,";", "Food A temp change in last 10 minutes is:", foodA_oldest_temp)
                print(f">>> Food A alert! The temperature of Food A has changed by 1 degree or less in 10 min. Old temp")
            else:
                print("Current Food A temp is:", foodA_current_temp,";", "Food A temp change in last 10 minutes is:", foodA_oldest_temp)
    else:
        print(f" [x] Current foodA temp is:", foodA_current_temp)

    # simulate work by sleeping for the number of dots in the message
    time.sleep(body.count(b"."))
    # when done with task, tell the user
    print(" [x] Done.")
    # acknowledge the message was received and processed 
    # (now it can be deleted from the queue)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


# define a main function to run the program
def main(hn: str = 'localhost', qn: str = '02-food-A'):
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
        channel.basic_consume(queue=qn, auto_ack = True, on_message_callback=foodA_callback)

        # print a message to the console for the user
        print(" [*] Ready for work. To exit press CTRL+C")

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
    main('localhost', '02-food-A')
   
