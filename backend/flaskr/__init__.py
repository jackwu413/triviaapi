import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions): 
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  selection = [question.format() for question in questions]
  current_questions = selection[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  cors = CORS(app, resources={'/': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request 
  def after_request(response): 
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    category_dict = {}
    for category in categories: 
      category_dict[category.id] = category.type 

    if len(category_dict) == 0:
      abort(404)

    return jsonify({
      'success': True, 
      'categories': category_dict
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_questions():
    questions = Question.query.all() 
    total_questions = len(questions)
    current_questions = paginate_questions(request, questions)

    categories = Category.query.all()
    category_dict = {}
    for category in categories: 
      category_dict[category.id] = category.type

    if len(current_questions) == 0: 
      abort(400)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': category_dict,
      'current_category': 'test'
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<id>', methods=['DELETE'])
  def delete_question(id): 
    try:
      question = Question.query.get(id)
      if question == None: 
        abort(404)
      question.delete()
      return jsonify({
        'success': True, 
        'deleted': id
      })
    except: 
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def post_question(): 
    body = request.get_json()

    new_question = body['question']
    new_answer = body['answer']
    new_difficulty = body['difficulty']
    new_category = body['category']

    if ((new_question == None) or (new_answer == None) or (new_difficulty == None) or (new_category == None)): 
      abort(422)

    try: 
      question = Question(
        question = new_question, 
        answer = new_answer, 
        difficulty = new_difficulty, 
        category = new_category
      )

      question.insert()

      questions = Question.query.all()
      current_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True, 
        'created': question.id, 
        'questions': current_questions, 
        'total_questions': len(questions)
      })
    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question(): 
    body = request.get_json()
    search_term = body['searchTerm'] 
    results = Question.query.filter(
      Question.question.ilike(f'%{search_term}%')).all()
  

    if (len(results) == 0): 
      abort(404)

    paginated_results = paginate_questions(request, results)
    
    return jsonify({
      'success': True, 
      'questions': paginated_results, 
      'total_questions': len(results),
      'current_category': 'test'
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<id>/questions')
  def get_questions_by_category(id):
    category = Category.query.get(id)

    if category == None: 
      abort(400)

    #Get questions with same category id
    questions = Question.query.filter_by(category=category.id).all()

    paginated_questions = paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': paginated_questions, 
      'total_questions': len(questions), 
      'current_category': category.type  
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json() 
    previous_questions = body['previous_questions']
    category = body['quiz_category']

    if (previous_questions == None) or (category == None): 
      abort(400)

    #id 0 means all categories, else query from specific category 
    if (category['id'] == 0): 
      questions = Question.query.all() 
    else: 
      questions = Question.query.filter_by(category=category['id']).all()

    #get random question
    def get_random_question(): 
      r = random.randrange(0,len(questions),1)
      return questions[r]

    #check if question has been used 
    def check_in_previous(q):
      used = False 
      for question in previous_questions: 
        if question == q.id: 
          used = True 
      return used 

    current_question = get_random_question()

    while(check_in_previous(current_question)):
      current_question = get_random_question() 
      if len(previous_questions) == len(questions): 
        return jsonify({
          'success': True
        })

    return jsonify({
      'success': True, 
      'question': current_question.format()
    }) 



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error): 
    return jsonify({
      "success": False, 
      "error": 404, 
      "message": "resource not found"
    })
  
  @app.errorhandler(422)
  def unprocessable(error): 
    return jsonify({
      "success": False, 
      "error": 422, 
      "message": "unprocessable"
    })

  @app.errorhandler(400)
  def bad_request(error): 
    return jsonify({
      "success": False, 
      "error": 400, 
      "message": "bad request"
    })


  return app

    