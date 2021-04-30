import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, query):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in query[start:end]]
    return questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    @cross_origin()
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # --------------------------------------------------------------
    # Routes
    # --------------------------------------------------------------

    @app.route('/categories', methods=['GET', 'POST'])
    def get_categories():
        if request.method == 'GET':
            if request.get_json():
                # executed if the client sends a json body
                abort(400)

            else:
                query = Category.query.order_by(Category.id).all()
                categories_arr = {}
                for category in query:
                    categories_arr[category.id] = category.type

                totalQuestions = Question.query.count()

                return jsonify({'success': True,
                                'totalQuestions': totalQuestions,
                                'categories': categories_arr})

        '''
            ----------------------------------------------
            play the game
            ----------------------------------------------
        '''

        if request.method == 'POST':
            data = request.get_json()
            #  data ={'previous_questions': [],
            #         'quiz_category': {'type': 'Science', 'id': '1'}}
            if data is None:
                abort(400)

            categories = [category.format() for category
                          in Category.query.all()]

            category_id = data['quiz_category'].get('id', 0)
            previous_questions = data.get('previous_questions', None)

            categories_id = [category.format()['id']
                             for category in Category.query.all()]

            if (int(category_id) not in categories_id
              and int(category_id) != 0):
                abort(404)

            filters = []
            if previous_questions:
                filters.append(~Question.id.in_(previous_questions))
            if int(category_id) != 0:
                filters.append(Question.category == str(category_id))

            questions = Question.query.filter(*filters)\
                .order_by(Question.id).all()

            try:
                game_question = random.choice(questions).format()

            except IndexError:
                game_question = None

            return jsonify({
                'success': True,
                'categories': categories,
                'question': game_question,
            })

    @app.route('/questions', methods=['GET', 'POST'])
    def get_questions():
        if request.method == 'GET':

            questions = Question.query.all()
            categories = Category.query.order_by(Category.id).all()

            categories_arr = {}
            for category in categories:
                categories_arr[category.id] = category.type

            category_id = request.args.get('category_id', '0', type=str)

            # if category == '0', query all questions from all categories
            if category_id == '0':
                paginated_questions = paginate_questions(request, questions)

            # if category_id provided in url argument not in category, abort
            elif (int(category_id) not in
            [record.format()['id'] for record in categories]):
                abort(400)

            else:
                # if valid category id, query questions from specific category
                questions_in_category = Question.query\
                    .filter_by(category=category_id).all()

                paginated_questions = paginate_questions(request,
                                                         questions_in_category)

            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': category_id,
                'categories': categories_arr,
            })

        if request.method == 'POST':
            ''' this route is used to search questions or to post
                a new question '''

            data = request.get_json()

            key_word = data.get('searchTerm', None)

            # When route is used for seaching purposes
            if key_word:
                matched_questions = Question.query\
                    .filter(Question.question.ilike(f'%{key_word}%')).all()

                current_questions = paginate_questions(request,
                                                       matched_questions)

                total_questions = Question.query.count()

                return jsonify({'success': True,
                                'total_questions': total_questions,
                                'matched_questions': len(matched_questions),
                                'questions': current_questions
                                })

            # When route is used for posting a new question
            keys = ['question', 'answer', 'category', 'difficulty']

            for k in keys:
                if k not in data.keys():
                    abort(400)

            if ((int(data['category']) < 1 or int(data['category']) > 6)
            or (int(data['difficulty']) < 1 or int(data['difficulty']) > 5)):
                abort(422)

            new_question = Question(question=data['question'],
                                    answer=data['answer'],
                                    category=data['category'],
                                    difficulty=data['difficulty'])

            # executed only when testing with unittest
            new_question_id = data.get('id', None)
            if new_question_id:
                new_question.id = new_question_id

            new_question.insert()

            return jsonify({'success': True,
                            'new_question_id': new_question.id,
                            'total_questions': Question.query.count()
                            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id)\
                .one_or_none()

            question.delete()

            total_questions = Question.query.count()
            return jsonify({'success': True,
                            'deleted_id': question_id,
                            'total_questions': total_questions,
                            })
        except:
            abort(404)

    @app.route('/categories/<int:category_id>/questions')
    def get_categorty_questions(category_id):
        categories = Category.query.all()
        categories_id = [category.id for category in categories]

        if category_id not in categories_id:
            abort(404)

        questions = Question.query.filter(
            Question.category == str(category_id)).all()

        paginated_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': category_id,
        })

    # --------------------------------------------------------------
    # error handlers
    # --------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Not processable'
        }), 422

    return app
