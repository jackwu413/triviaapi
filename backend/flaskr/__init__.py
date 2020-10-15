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

  @app.route('/questions/<int:id>', methods=['DELETE'])
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

  @app.route('/questions', methods=['POST'])
  def post_question(): 
    body = request.get_json()



    if (body.get('question') is None) or (body.get('answer') is None) or (body.get('difficulty') is None) or (body.get('category') is None): 
      abort(422)

    new_question = body.get('question')
    new_answer = body.get('answer')
    new_difficulty = body.get('difficulty')
    new_category = body.get('category')

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

  @app.route('/questions/search', methods=['POST'])
  def search_question(): 
    body = request.get_json()
    search_term = body.get('searchTerm')


    results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    if (len(results) == 0): 
      abort(404)

    paginated_results = paginate_questions(request, results)
    
    return jsonify({
      'success': True, 
      'questions': paginated_results, 
      'total_questions': len(results),
      'current_category': 'test'
    })

  @app.route('/categories/<int:id>/questions')
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

  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    body = request.get_json() 
    previous_questions = body.get('previous_questions')
    category = body.get('quiz_category')

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





  @app.errorhandler(404)
  def not_found(error): 
    return jsonify({
      "success": False, 
      "error": 404, 
      "message": "resource not found"
    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error): 
    return jsonify({
      "success": False, 
      "error": 422, 
      "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error): 
    return jsonify({
      "success": False, 
      "error": 400, 
      "message": "bad request"
    }), 400


  return app

    