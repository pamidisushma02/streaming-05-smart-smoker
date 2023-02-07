"""
    This program reads tasks from tasks.csv and sends to a queue on the RabbitMQ server.
    Make tasks harder/longer-running by adding dots at the end of the message.

    Author: Sushma Pamidi
    Date: February 6, 2023

"""

import pika
import sys
import webbrowser
# Import the below module whenever csv is involved 
import csv



def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()

        # Delete queue 
        ch.queue_delete(queue=queue_name) 

        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        
        print("Sent message to", queue_name, message)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

# Standard Python idiom to indicate main program entry point
# This allows us to import this module and use its functions
# without executing the code below.
# If this is the program being run, then execute the code below
if __name__ == "__main__":  
    
    # Only offer to show the prompt based on the below
    show_offer = "False"

    if show_offer == "True":
       # ask the user if they'd like to open the RabbitMQ Admin site
       offer_rabbitmq_admin_site()
    else:
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

    # Declare variables needed to read csv file as input
    # The file name does not have to be hard coded. We can change the file name assigned to the input_file_name variable 
    # if no arguments are provided, use the default message
    # use the join method to convert the list of arguments into a string
    

    input_file_name = "smoker-temps.csv"

    input_file = open(input_file_name, "r")

    reader = csv.reader(input_file, delimiter=",")

    header = next(reader)
    header_list = ["message"]

    # Get message from the file
    for row in reader:
        #Read each row of csv file and put Time Stamp, Smoker temp, Food A temp and Food B temp in different variables
        var1, var2, var3, var4 = row

        #Below converts list to a string. If the below is not done an error is thrown
        #message = ",".join(row)
        message_ch1 = (var1, var2)
        message_ch1_str = ",".join(message_ch1)

        message_ch2 = (var1, var3)
        message_ch2_str = ",".join(message_ch2)

        message_ch3 = (var1, var4)
        message_ch3_str = ",".join(message_ch3)

        # send the time stamp and Smoker temp to the first queue
        send_message("localhost","01-smoker",message_ch1_str)

        # send the time stamp and Food A temp to the Second queue
        send_message("localhost","02-food-A",message_ch2_str)

        # send the time stamp and Food B temp to the Third queue
        send_message("localhost","03-food-B",message_ch3_str)
        

    input_file.close()