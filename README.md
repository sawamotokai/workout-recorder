# workout-recorder
Keeps track of your workout log and displays graphs of your growth. It also suggests weight you might want to use.

This app is deployed on heroku server and connected to mlab database.
URL: https://sleepy-spire-95192.herokuapp.com/

HOW TO RUN THE APP

Run MongoDB.
Run the command:
Flask run

ABOUT THIS WEB APP Workout log was built by Kai Sawamoto as his final project for CPSC101.

FUNCTIONALITIES It keeps track of your workout records and generates graphs to show your growth of Big3 exercises - bench press, dead lift and squat. It also suggests weight, reps and sets for your Big3 exercises. The suggested weight is based on the current one rep max weight and is based on the principle of nonlinear periodization, an idea that one should train with different weight every time.

Technologies Used: • Flask • MongoDB • sha512 encryption • Pygal • HTML5(jinja2 template) • CSS(bootstrap4)

Difficulties • Learned Flask from scrach for this project, so the whole idea of fullstack development was hard to grasp. • (I'm writing this after taking software construction course at UBC) When I created this web app, I had no idea about software construction, so now that I learned a bit of it, I clearly know it was not a good design; for example, I would restructure most of the classes based on the single responsiblity principle. That is, most of the classes have a lot of responsiblity that they are not consistant in terms of their responsibilities.

Takeaways • Learned how to use Flask, including advanced features such as url parameters, blueprints, flash etc. • Understood how to interact with no-SQL database such as mongoDB.

Future Plan • I'd like to turn this app into a mobile app, so I am currently learning React so I will be able to use React Native eventually. • As I discussed with the prof, I would like to build the whole app on SQL database as opposed to mongoDB, becasue it will allow me to query data in a more flexible way.
