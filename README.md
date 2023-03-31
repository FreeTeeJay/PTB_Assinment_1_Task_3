# PTB_Assinment_1

this is the prossees that I took to get the code up and running:

1.Download Docker and set up RabbitMQ to make a virtual host fort the application.

2.Create the topics for the middleware in RabbitMQ :'position' and 'query'.

3.Tracker application: The tracker application is responsible for tracking the positions of each person and logging whenever two or more people occupy the 
  same position. The tracker should subscribe to the 'position' topic and keep a view of the environment detailing each person's current position. 
  If two or more people occupy the same position, the tracker should log this fact in a suitable data structure. The tracker should also subscribe to
  the 'query' topic and respond to the 'query-response' topic with all the names that person came into contact with, in reverse-chronological order.

4.Person application: The person application represents a person that starts with a position and randomly moves one square once every 'n' seconds.
  The person application should connect to the middleware endpoint, communicate its initial (randomised) position to the 'position' topic along with the 
  person's identifier, and continually make a move in a random direction (one square at a time) and publish that move to the 'position' topic. 
  The movement speed should be configurable based on the start-up argument provided.

5.Query application: The query application should connect to the middleware and publish the person identifier provided
  at start-up onto the 'query' topic. It should then await the response on the 'query-response' topic from the tracker and print that response to the console, 
  then exit.
  
6.GUI: A GUI should be created that gives a visual representation of the environment and allows the user to query a person identifier and see with whom they
  have come into contact. The GUI should be built using a suitable Python GUI library such as Tkinter.
 
7.Environment size: The solution should be extended to work for boards/environments of different sizes. 
  This can be achieved by making the virtual size of the board configurable, up to a maximum of 1,000 x 1,000.
