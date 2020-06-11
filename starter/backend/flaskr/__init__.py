import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from psycopg2.extras import DateTimeRange
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


  
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs [DONE]
  '''
  cors = CORS(app, resources={'/': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow [DONE]
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  def paginate_questions(request, selection):
    #Defaul method that will take the request and selection to paginate the selection
    page = request.args.get('page', 1, type=int)

    #Store/calculate tha start and end of the questions
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  '''
  @TODO: 
  Create an endpoint to handle GET requests [DONE paginaton is not needed]
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    #Query the db and get all categories
    #categories=Category.query.all()
    categories_1=Category.query.order_by(Category.id).all()
    current_categories=[category.format() for category in categories]
    category_types=[category['type']for category in current_categories]
   # categories = list(map(Category.format, Category.query.all())) #List the categories
    #list_categories=[category.format() for category in categories]
    return jsonify({
        'success': True,
        'categories':current_categories,
        'total_categories':leng(current_categories)
    })
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). [DONE + PAGINATION]
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  [DONE] All categories are listed at the end of the questions

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. [DONE]
  '''
  
  @app.route('/questions')
  def get_questions():
    # Select all questions and order them by their ID
    selection = Question.query.order_by(Question.id).all()

    #Paginate all questions
    current_questions = paginate_questions(request, selection)

    #If there are no questions then abort
    if len(current_questions) == 0:
      abort(404)

    #query all categories 
    categories=Category.query.all()
   
   #looping the categories to display the categories with ID and type
    #list_categories=[category.format() for category in categories]
    category_formatted = {category.id: category.type for category in categories}
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': category_formatted,
      'current_category': None #Set to none as mentioned in one of the questions in the knowledge area https://knowledge.udacity.com/questions/82424
      })
      
 
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID.  [DONE]

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. [DONE]
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    #Try to filter the id of the question to make sure that it exists
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

    # abort if the question is none (id does not corresponds to any of the question ids)
      if question is None:
        abort(404)

      #Delete the question that matches the above id, then display all questions
      question.delete()
      #Select all the remaining questions and order then by id, then paginate them
      selection = Question.query.order_by(Question.id).all()
      remaining_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': remaining_questions,
        'total_questions': len(Question.query.all())
      })

    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score [DONE].

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  [DONE]
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    #Get the request body
    body = request.get_json()
   
    #Get the values for question, answer, category and difficulty
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    # Try to insert the values that were taken from the request body
    try:
      question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      #Paginate the selection with the iserted questions
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'Questions': current_questions,
        'total_questions': len(Question.query.all())
      })

    except:
     abort(422)

#curl -X DELETE http://127.0.0.1:5000/questions

#curl http://127.0.0.1:5000/questions
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. [DONE]

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. [DONE]
  '''
  
  # curl -d '{"searchTerm":"xyz"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/search
  @app.route('/search', methods=['POST'])
  def search_question():

    #Get the request body
    body = request.get_json()

    # get the search term from the body
    search_term = body.get('searchTerm')

    #Select questions that has the searched term (case insensitive + substring)
    selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    
    # if there are no questions that corresponds to the searched term Abort (not found)
    if (len(selection) == 0):
        abort(404)
    
    #If there are questions then paginate them and return the values.
    paginated = paginate_questions(request, selection)
    
    return jsonify({
          'success': True,
          'questions': paginated,
          'total_questions': len(Question.query.all())
      })
  
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. [DONE]

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    category = Category.query.filter_by(id=category_id).one_or_none()

    #If the provided category is not one of the 6 categories
    if (category is None):
      abort(404)
    # If the category is one of the 6 types, then select all questions that belong to that category
    selection = Question.query.filter_by(category=category.id).all()
    
    # Paginate the selected questions.
    paginated = paginate_questions(request, selection)
    
    return jsonify({
        'success': True,
        'questions': paginated,
        'total_questions': len(selection), #Will display total of questions per category
        'current_category': category.type #displat the type of the category
    })

  # curl http://127.0.0.1:5000/categories/2/questions


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
  def get_quiz():
    try:
      #loading request body
      data = request.get_json()
      
      #get the previous question from the Request Body
      prev_questions = data['previous_questions']

      #get the category ID  from the Request Body
      category_id = data["quiz_category"]["id"]
      
      if category_id == 0:
      #If a category was not specified in the response body (not one of the 6 categories)
          if prev_questions is not None: 
          #Select all questions and exculde prev_questions.
              questions = Question.query.filter(Question.id.notin_(prev_questions)).all()
          else:
          #Select all questions (prev_questions has no values).
            questions = Question.query.all()
      else:
      #If a category is  specified in the response body (one of the 6 categories)
          category = Category.query.get(category_id)
          # Get category
          if prev_questions is not None:
          #Select all questions and exculde prev_questions.
            questions = Question.query.filter(Question.id.notin_(prev_questions),Question.category == category.id).all()
          else:
            #Select all questions in that category (prev_questions has no values).
            questions = Question.query.filter(Question.category == category.id).all()
      
      #Set the next question randomly from the questions that excluded the prev_questions
      random_question = random.choice(questions).format()
      
      if random_question is None:
        #If all questions were selected (prev_question = all questions ids)
        random_question = False 

      #Return the values with the randomly selected question
      return jsonify({
        'success': True,
        'question': random_question
      })
    except:
      abort(422)


# curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": "21", "quiz_category": "1"}

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. [DONE] + INCLUDED 500 ERROR
  '''
  # Handle errors [422][404] [500] [405] 
  # will be displayed after abort(Error Code) 
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success': False,
          'Error': 422,
          'Message':'unprocessable'
      }),422

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'Error': 404,
          'Message':'not found'
      }),404

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success': False,
          'Error': 405,
          'Message':'method not allowed'
      }),405

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          'success': False,
          'Error': 500,
          'Message':'Internal Server Error'
      }),500  

  return app

