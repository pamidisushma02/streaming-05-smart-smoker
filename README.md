# Name: Sushma Pamidi
## last updated on Feb 20, 23
#### Link to Repo: https://github.com/pamidisushma02/streaming-05-smart-smoker

# streaming-05-smart-smoker

> Create a Producer to Stream information from a smart smoker

One process will Design and Implement a Barbeque producer that streams information from a Smart Smoker into three queues 


## Below tasks are done

1. A new repo is created in Github 

2. Clone the repo down to local machine.
   ##### Done

3. Add .gitignore
   ##### Done

4. View / Command Palette - then Python: Select Interpreter
   ##### Done

5. Select your conda environment. 
   ##### Done

6. Add csv data file to repo 
   ##### Done

7. Create a bbq_producer.py file 
   ##### Done

## Reuse version 3 code from Module 4

## Execute the Producer

1. Read the csv data file
2. Read each column into a seperate variable
3. Use header = next(reader) to skip reading the header 
4. A main function has been defined
5. Call the send_message function thrice i.e. one for each queue 
6. Create a connection, first delete queue using queue_delete() and declare with queue_declare() function. "01-smoker" queue is declared. Publish time stamp and Smoker Temperature to this queue
7. Create a connection, first delete queue using queue_delete() and declare with queue_declare() function.  "02-food-A" queue is declared. Publish time stamp and Food A Temperature to this queue
8. Create a connection, first delete queue using queue_delete() and declare with queue_declare() function. "01-food-B" queue is declared. Publish time stamp and Food B Temperature to this queue
9. Use time.sleep(30) to read records once in 30 seconds

## Execute the Consumers

1. Three consumer process have been created 
2. Smoker Consumer monitors 01-smoker queue, prints the current smoker temperature, temperature change in the last 2.5 minutes
   And Alerts when the Smoker temperature has decreased more than 15 F in 2.5 min
3. FoodA Consumer monitors 02-food-A queue, prints the current Food A temperature, temperature change in the last 10 minutes
   And Alerts when the Food A temperature has not changed more than 1 degree in 10 min 
4. FoodB Consumer monitors 03-food-B queue, prints the current Food A temperature, temperature change in the last 10 minutes
   And Alerts when the Food B temperature has not changed more than 1 degree in 10 min 
5. Three seperate scripts are written, each having their own call backs. I chose this method to keep the code simple, reusable in future when just one call back is needed


## Screenshot

  ### Below Screen shots are that of the Anaconda prompts for Producer, Smoker Consumer, Food A Consumer and Food B Consumer 
 

## Anaconda prompts (Producer, Smoker consumer, Food A consumer and Food B consumer)
![Anaconda Prompts]( https://github.com/pamidisushma02/streaming-05-smart-smoker/blob/main/Consumers_Smoker%2C%20FoodA%2C%20FoodB.PNG "Console")


