# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
Response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}

```
#### GET '/questions'
- Fetches a a list of questions including pagination.
- Request Arguments: None
- Example: http://127.0.0.1:5000/questions
- Returns: return a list of questions (with answers, category, difficulty and id), number of total questions, current category, categories.  
Response:
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }],
    "success": true,
    "total_questions": 21
}
```
#### DELETE '/questions/<int:question_id>'
- Deletes a question based on its ID.
- Request Arguments: None
- Example: http://127.0.0.1:5000/questions/24
- Returns: the id of the deleted question, and the total of the remaining questions.
Response:
```
{
    "deleted": 26,
    "success": true,
    "total_questions": 17
}
```
#### POST '/questions'
- Posts a question, answer, category, and difficulty score.
- Example: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Question1?", "answer": "answer1", "difficulty": 1, "category": "2" }'
Request: 
```
{
  "question": "Question1",
  "answer": "Answer1",
  "category": 1,
   "difficulty": 1
}
```
Response:
```
{
    "created": 34,
    "created_question": {
        "answer": "Answer1",
        "category": 1,
        "difficulty": 1,
        "id": 34,
        "question": "Question1"
    },
    "success": true,
    "total_questions": 25
}

```
#### GET '/categories/<int:category_id>/questions'
- Gets questions based on category type.
- Request Arguments: category id (using url parameters).
- Example: http://127.0.0.1:5000/categories/4/questions
- Returns: all questions that belong to that category id (with pagination).
Response:

```
{
    "current_category": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "success": true,
    "total_questions": 1
}

```
#### POST '/search'
- Post a search term, and get all questions that has the searched term.
- Request Arguments: searchTerm.
- Example: curl -d '{"searchTerm":"action"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/search
- Returns: all questions that has that search term.
Request:
```
{
"searchTerm": "action"
}
```

Response:
```
{
    "questions": [
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
    ],
    "success": true,
    "total_questions": 26
}
```
#### POST '/quizzes'

- Take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
- Request Arguments: previous questions and category.
- Example: curl -d '{"previous_questions": [10, 13], "quiz_category": {"type": "Science", "id": "1"}}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/quizzes

- Returns: ranom questions that has that search term.
Request:
```
{
	"previous_questions": [10, 13],
    "quiz_category":
    	{
			"type": "Science", "id": "1"
    	}
}
```
Response:
```
{
    "question": {
        "answer": "Answer1",
        "category": 1,
        "difficulty": 1,
        "id": 34,
        "question": "Question1"
    },
    "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
