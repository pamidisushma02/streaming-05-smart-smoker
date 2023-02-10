# Name: Sushma Pamidi
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


## Screenshot

  ### Below Screen shots are that of the console showing the messages published to three queues
  ##### This screen shot shows that the Smoker Temp is published to the first queue, Food A temp is published to the second queue 
  ##### and Food B temp is published to the third queue 
  

## Console
![Console Terminal]( https://github.com/pamidisushma02/streaming-05-smart-smoker/blob/main/Console.PNG "Console")


