# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

# Using The Trivia API

## Getting Started

This API has not been deployed to the web yet so you will need to run it on your local environment. Follow instructions above to start the backend and refer to the frontend README if you wish to deploy the user interface.

	base URL: 		        http://127.0.0.1:5000/

	API Keys/Authentication: 	Not applicable

## Errors

The most common errors you are likely to encounter are returned in json format

{ 'success': False,
  'error': 400,
  'message': 'Bad request’ }


{ 'success': False,
  'error': 404,
  'message': 'Resource not found’ }


{ 'success': False,
  'error': 422,
  'message': ‘Not processable'}

## Resource endpoint library

Methods               Endpoints

------------------+—--------------------------

['GET', ‘POST']     '/categories'

['GET', ‘POST’]     '/questions'

[‘DELETE']          '/questions/<int:question_id>'

['GET']             '/categories/<int:category_id>/questions'

#### IMPORTAT NOTE: if you copy/paste the sample requests below and they don't work, try typing it from scratch in your CLI. Sometimes what may look as the same characters are actually not - and that will cause an error to occur.


### GET '/categories'

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

Request Arguments: None

Returns: An object with a three keys - categories, success, and totalQuestions.

Category contains an object of category_string key:value pairs.

Total questions contains an integer with the total questions available in the database

#### Sample Request:

curl 'http://127.0.0.1:5000/categories'

#### Response body:

{
 "categories": {
 "1": "Science",
 "2": "Art",
 "3": "Geography",
 "4": "History",
 "5": "Entertainment",
 "6": "Sports"
 },
 "success": true,
 "totalQuestions": 19
 }

### POST '/categories'

Used to play the game. Fetches a random question from a given category provided in the arguments. It takes the id of previous questions to avoid repetition of questions. If no more questions are available in a given category, it will return any random question. 

Request Arguments:
 An object of dictionary type with the following key-value pairs   :

{'previous_questions': [X, Y ],  (optional)   
 'quiz_category': {'id':  Z}}

  Where:
	 X,Y, Z are integers
	 Z is the category id or 0 for all categories

Returns: An object with 5 keys:

	- ‘previousQuestions’ with a list of questions ids of type integer or null
	- ‘question’ with a value of dictionary type containing all information about the question
	- ‘question_id’ with an integer value
	- ‘quizCategory’ with an integer value of the category id.
	- ‘success’ with a boolean true 

#### Sample Request:

curl 'http://127.0.0.1:5000/categories' -X POST -H 'Content-Type:application/json' -d '{"previous_questions":[18], "quiz_category":{"id":2}}'

#### Response body:

  {
    "previousQuestions": [
      18
    ],
    "question": {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    "question_id": 16,
    "quizCategory": 2,
    "success": true
   }

### GET '/questions'

Fetches questions, paginating them by 10 at time. It takes inline parameters to select questions from specific categories and page number. 

Request Arguments:

  category_id (optional)
  page (optional)

Returns: An object with 5 keys:

	- ‘categories’ with an object of all available categories an its ids parsed as a string-string key-value pair
	- ‘current_category’ with a string value of the category id.
	- ‘questions’ with a list of dictionaries containing all information about each question
	- ‘success’ with a boolean true
	- ‘total_questions’ with the integer value of all available questions in the database 

#### Sample Request:

curl 'http://127.0.0.1:5000/questions?category_id=1&page=1'


#### Response body:

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "1",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 19
}

### POST '/questions'

Used to search questions by key words or to post a new question, based on arguments provided on the json body

Request Arguments for Searching Purposes:

  {'searchTerm': ‘string type’}

	page=X (optional - url argument)

	where X is an integer

Returns: a dictionary body with for keys:

	- “matched_questions” - an integer of the total number questions matched in the query
	- “questions” - a list of dictionaries with the information of each question. Paginated by 10s
	- “success” - a boolean True
	- “total_questions” - an integer with the total number of questions in the database


#### Sample Request to search a question(s):

curl 'http://127.0.0.1:5000/questions' -X POST -H 'Content-Type:application/json' -d '{"searchTerm":"world cup”}'


#### Response body:

{
  "matched_questions": 2,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 20
}

Request Arguments for Posting a New Question:

  {'question':‘Your question',
   'answer': ‘your answer',
   'category': X,
   'difficulty': Y}

	Where the values of:
	 - ’question’ and ‘answer’ is a string
	 - ‘category’ X is in an integer between 1-6
	 - ‘difficulty’ Y is an integer between 1-5


Returns: A dictionary object with 3 keys:

	- “new_question_id” - integer with the question id number
 	- “success" - boolean value true
 	- “total_questions” - total number of questions in the database


#### Sample Request to post a new question:

curl 'http://127.0.0.1:5000/questions' -X POST -H 'Content-Type:application/json' -d '{"question":"what is the oldest continental settlement in America", "answer":"San Agustin, Fl", "category":3, "difficulty":5}'


#### Response body:

{
  "new_question_id": 24,
  "success": true,
  "total_questions": 20
}


### DELETE '/questions/<int:question_id>'

Errases a question from the database by its id

Request Arguments:

  A url argument with the integer number of the question id to be deleted

Returns: An object with 3 keys:
	- “deleted_id” - an integer with the id of the deleted question
	- “success” - a boolean true indicating the success of the operation
	- “total_questions" - an integer with new total of questions in the database


#### Sample Request:

curl 'http://127.0.0.1:5000/questions/10' -X DELETE

#### Response body:

{
  "deleted_id": 10,
  "success": true,
  "total_questions": 19
}


### GET '/categories/<int:category_id>/questions'

Fetches all questions of a given category and paginate them in sets of 10.

Request Arguments:  

  <int:category_id> - a url argument to select the desired category
  page=X (optional)

    Where X is an integer 

Returns: An object with 4 keys:  

  - ‘success’ - a boolean True 
  - ‘questions' - a list of dictionaries with information about the questions queried
  - ‘total_questions' - an integer of the total questions in the requested category
  - 'current_category': an integer of the category id


#### Sample Request:

curl 'http://127.0.0.1:5000/categories/1/questions?page=1'

#### Response body:

{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
