import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# function to paginate


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categoriesList = {}
        for category in categories:
            categoriesList[category.id] = category.type
        if len(categories) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories},
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
    @app.route('/questions')
    def fetch_questions():
        totalQuestions = Question.query.all()
        paginated_quests = paginate_questions(request, totalQuestions)
        categories = Category.query.all()
        categoriesList = {}
        for category in categories:
            categoriesList[category.id] = category.type
        if len(paginated_quests) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': paginated_quests,
            'total_questions': len(totalQuestions),
            'categories': categoriesList,
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
            if question == None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': id
            })
        except:
            abort(422)

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
    def add_question():
        try:
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)
            print('question is :', question)
            if question == "":
                abort(422)
            quest = Question(question=question, answer=answer,
                             difficulty=difficulty, category=category)
            quest.insert()
            return jsonify({
                'success': True,
                'created': quest.id,
            })
        except Exception as e:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        searchString = body.get('searchTerm', None)
        if searchString:
            results = Question.query.filter(
                Question.question.ilike(f'%{searchString}%')).all()
            if (len(results) == 0):
                abort(404)
            print('search res:', results)
            return jsonify({
                'success': True,
                'questions': [question.format() for question in results],
                'total_questions': len(results),
                'current_category': None
            })
        abort(404)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat_id>/questions')
    def questions_by_category(cat_id):
        try:
            questionsByCat = Question.query.filter(
                Question.category == cat_id).all()
            if len(questionsByCat) == 0:
                abort(404)
            questionByCatList = []
            print('questions by category', questionsByCat)
            for question in questionsByCat:
                questionByCatList.append(Question.format(question))
            print('question list:', questionByCatList)
            return jsonify({
                'success': True,
                'questions': questionByCatList,
                'total_questions': len(questionsByCat),
                'current_category': cat_id
            })
        except:
            abort(404)

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
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        bodyData = request.get_json()
        category_id = bodyData['quiz_category']['id']
        previous_questions = bodyData['previous_questions']
        if(category_id == 122):
            abort(422)
        if (category_id == 0):
            questions = Question.query.filter(
                Question.id.notin_((previous_questions))).all()
        else:
         
            category_filter = Question.query.filter_by(category=category_id)

            answered_filter = category_filter.filter(Question.id.notin_((previous_questions)))

            questions = answered_filter.all()
        print('quest are:',questions)

     

        def getNextquestion():
            next_question = random.choice(questions).format()
            return next_question

   
        next_question = getNextquestion()

   

        if (len(previous_questions) == len(questions)):
            return jsonify({
                'success': True,
                'message': "game over"
            }), 200

        return jsonify({
            'success': True,
            'question': next_question
        })

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
