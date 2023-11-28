# Case Journal
#### Video Demo: https://youtu.be/FJsAlfTQFuo
#### Description:

This web application is designed to streamline the workflow of IT professionals, particularly those who frequently interact with ticketing systems. It addresses a common challenge: handling tickets with similar or identical symptoms, which often involves time-consuming searches for past cases with matching issues. To resolve this, the application enables users to log details of resolved tickets, creating a referenceable knowledge base for future cases. This feature significantly enhances efficiency by allowing quick access to previous solutions and methodologies.

The front end of the project incorporates HTML, CSS, Bootstrap, and Vanilla JavaScript. The back end is built using Python with Flask, SQL Alchemy, JWT, and SQLite3

In my templates folder I have 6 files including the layout file, which is basically where all
the rest of my html files will render into.

For authentication I got login.html and register.html.
Then, the main page is my index.html where the user can fill in the form to log a new case entry.
The cases.html is where they can view, update, delete and filter their existing cases.

Finally the apology.html is a custom error page, which was similarly used on Finance pset.

In my backend, the most important file is main.py because I am loading my environment variables, initilizing my flask application and creating my db.
Then, extensions.py is the second most important file, becasue that is where I am initializing SQL alchemy and JWT manager, which are then used in main.py.

Then, I got my application routes split into 2 different files: main_routes.py and auth.py,

In auth.py I am handling the user login, logout and registration.
For the register I am simply taking the parameters submitted by the user which are email, password and password confirmation.
Then I am running several checks such as ensure the user doesn't exist already, the email and password aren't empty and correct, etc.
In this case, I am only accepting emails for the domain of @xyz.com only, no hyphens or plus signs are accepted.

Finally, if it passes all checks a new user is inserted into the db with a hashed password.

The login route is making sure the username and password match an existing user in the db and not submitted as empty.
If these checks are passed, user is redirected to the index of the page and it is given an access and refresh tokens.

The logout route is clearing the session and removing the access and refresh tokens from the client's cookies and redirecting to the login page.

Now, in the main_routes.py I got my index route wich is protected, meaning only users with a valid access token are allowed to go into that page.
In fact, all my main routes are protected.

The index page displays the form with all of the data that user needs to fill in to log a new case entry when accessed via GET.
For POST, The values cannot be empty otherwise and alert will popup. Also, the user is not allowed to enter a case if the case number already exists in the db.

If these checks are passed, a new case is logged in the db.

The cases page is showing all cases related to the currently logged in user and showing them in an expandable format.
When accessed by posts it will update the the details of the case if the case id submitted automatically in the form matches an existing case.

The delete route will, of course delete a case from the db based on the case_id that is automatically submitted when button is clicked.

In the filter route, we are basically taking the filtering criteria entered by the user and the querying the db based on that.
The data returned will be filtered and rendered into the cases.html file. Both, filter and delete routes can only be accessed via POST.

In the models.py, I am defining my db schema using SQL alchemy, as well as all of the instance and class methods that allow me to perform 
CRUD operations in the DB without having to use SQL language explicitly.

I am also defining a couple of functions: populate_categories and populate_subcategories in order to populate that information when my flask app 
is initialized and the db is created.

There is an images table that I am not using for now, as my app is not yet handling images, but it will be a future addition.

My helpers.py contains the apology function that allows me to display the custom error pages.
Finally, my .env file has all the environment variables that my flask app is using, such as teh secret key, db URI, etc.







