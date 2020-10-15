# Full Stack Trivia API Backend

## Getting Started

This is a full stack trivia application with the following features:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It's recommended that you work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation

### Getting Started 
* Base URL: This application is hosted at http://localhost:3000

### Endpoints

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the values are the corresponding string of the category 
- Example Response: 
```
{
    'success': True, 
    'categories': {
        '1': 'Science', 
        '2': 'Art', 
        '3': 'Geography', 
        '4': 'History', 
        '5': 'Entertainment', 
        '6': 'Sports'
    } 
}
```

#### GET '/questions'
- Fetches a list of questions that are paginated in groups of 10 along with list of categories and total number of questions
- Example Response: 
```
{
    'success': True, 
    'questions': [
        {
            'answer': 'Muhammad Ali'
            'category': 6, 
            'difficulty': 1, 
            'id': 9, 
            'question': "What boxer's original name is Cassius Clay?"
        },
        {
            'answer': '1974'
            'category': 4, 
            'difficulty': 1, 
            'id': 2, 
            'question': "What year did Nixon resign?"
        }
    ],
    'total_questions': 2, 
    'categories': {
        '1': 'Science', 
        '2': 'Art', 
        '3': 'Geography', 
        '4': 'History', 
        '5': 'Entertainment', 
        '6': 'Sports'
    }
}
```

#### DELETE '/questions/<int:id>'
- Deletes a question, given an id 
- Example Response: 
```
{
    'success': True, 
    'deleted': 4
}
```

#### POST '/questions'
- Adds a new question to the database, given all the required parameters 
- Required parameters: question, answer, difficulty, category
- Example Response: 
```
{
    'success': True, 
    'created': 14, 
    'questions': [
        ...list of all questions (including latest addition)
    ], 
    'total_questions': 14
}
``` 

#### POST '/questions/search'
- Searches for questions using a search term in JSON request parameters 
- Example Response: 
```
{
    'success': True, 
    'questions': [
        ...list of all questions with a substring matching the search term parameter
    ], 
    'total_questions': 2, 
    'current_category': None
}
```

#### GET '/categories/<int:id>/questions'
- Fetches a dictionary of questions for a specific category 
- Example Response: 
```
{
    'success': True, 
    'questions': [
        ...list of all questions within the given category
    ], 
    'total_questions': 12, 
    'current_category': 2
}
```

#### POST '/quizzes'
- Fetches a random question from the selected category 
- Example Response: 
```
{
    'success': True, 
    'question': {
        'answer': 'Muhammad Ali'
        'category': 6, 
        'difficulty': 1, 
        'id': 9, 
        'question': "What boxer's original name is Cassius Clay?"
    }
}
```