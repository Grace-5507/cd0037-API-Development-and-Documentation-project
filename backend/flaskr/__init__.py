import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from random import choice
import sys



from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTION')
        return response
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
   
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories =[Category.format() for category in categories]
        return jsonify({
            'success':True,
            'categories':formatted_categories
            })
    
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()
        
        formatted_questions =[question.format() for question in questions]
       
        return jsonify({
            'success':True,
            'questions':formatted_questions[start:end],
            'total_questions':len(formatted_questions),
            'current category':category[start:end]})
            


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
           question = Question.query.filter(Question.id == question_id).one_or_none()
           if question is None:
               abort(404)
           question.delete()
           return jsonify({
               'success':True
               })
        except:
            abort(400)
            
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        try:
            question = Question(question=new_question, answer=new_answer, category=new_category,difficulty=new_difficulty)
            question.insert()
        
        
            return jsonify({
                 'success':True,
                 'created':question.id,
                 'questions':len(formatted_questions)
                 })
        except:
            abort(400)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
   

    @app.route("/questions/search", methods=['POST'])
    def get_search():
        body = request.get_json()
        search_phrase = body
        questions = Question.query.all()
        if search_phrase == questions.substring:
            return questions
        
       
    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/<int:category_id>', methods=['GET'])
    def questions_based_on_category(category_id):
        
        questions = Question.query.filter_by(Question.category)
        
        formatted_questions =[question.format() for question in questions]
       
        return jsonify({
            'success':True,
            'str(questions)':formatted_questions
            })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/questions', methods=['POST'])
    def ask(category, previous_question):
        
        body = request.get_json(questions)
        questions = [Question.query.filter_by(category),Question.query.one()]
        
        for ask in questions:
           ask[0] = body
           n = 1
        for category in ask['category']:
           return "%d) %s" % (n, category)
           n = n + 1
        response = sys.stdin.readline().strip()
        if int(response) == ask['answer']:
             print ("CORRECT")
        else:
             print ("wrong")
        random.shuffle(questions)    

        for question in questions:
            return question.ask()

    
        
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
       return jsonify({
           "success": False, 
           "error": 404,
           "message": "Not found"
           }), 404
       
    @app.errorhandler(422)
    def unprocessable(error):
       return jsonify({
           "success": False, 
           "error": 422,
           "message": "unprocessable"
           }), 422

    return app

