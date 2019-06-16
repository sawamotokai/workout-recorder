from datetime import date

from flask import Blueprint, request, render_template, make_response, session, flash
from werkzeug.utils import redirect

import src.common.utils as utils
from src.common.database import Database
from src.models.exercises.exercise import Exercise
from src.models.users.user import User
import pygal

exercise_blueprint = Blueprint('exercises', __name__)


@exercise_blueprint.route('/<string:split>/')
@exercise_blueprint.route('/<string:split>/<string:user_id>')
def display_record(split, user_id=None):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    user = User.get_by_id(user_id)
    user.load_exercise_list(split)
    return render_template('records.html', split=split, user_id=user_id, exercise_list=user.exercise_list)


@exercise_blueprint.route('/<string:split>/new/<string:user_id>', methods=['POST', 'GET'])
def create_new_exercise(split,user_id):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    if request.method == 'GET':
        return render_template('new_exercise.html', split=split, user_id=user_id)
    else:
        name = request.form['exercise']
        name = name.strip().upper()
        weight = request.form['weight']
        reps = request.form['reps']
        sets = request.form['sets']
        comment = request.form['comment']

        record = [{'weight': weight,
                   'reps': reps,
                   'sets': sets,
                   'comment': comment,
                   'date': date.today().strftime("%x")}]

        exercise = Exercise.get_by_name(name)
        if exercise is None:
            Exercise(user_id=user_id, name=name,split=split, record=record).save_to_mongo()
        elif exercise.user_id == user_id:
            return redirect(f'/exercises/{split}/update/{exercise._id}')

        return make_response(display_record(split, user_id))


@exercise_blueprint.route('/<string:split>/update/<string:exercise_id>', methods=['POST', 'GET'])
def update_exercise(split, exercise_id):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    if request.method == 'GET':
        exercise = Exercise.get_by_id(exercise_id)
        return render_template('update.html', exercise=exercise, split=split)
    else:
        weight = int(request.form['weight'])
        reps = int(request.form['reps'])
        sets = int(request.form['sets'])
        comment = request.form['comment']
        record = {'weight': weight,
                  'reps': reps,
                  'sets': sets,
                  'comment': comment,
                  'date': date.today().strftime("%x")}
        exercise = Exercise.get_by_id(exercise_id)
        exercise.update_record(record)
        user_id = exercise.user_id
        exercise_name = exercise.name
        user = User.get_by_id(user_id)
        try:
            user.big3_counter[exercise_name] += 1
            Database.update('users', {'_id': user_id}, user.json())
        except:
            pass
        return redirect(f'/exercises/{split}/{user_id}')


@exercise_blueprint.route('/new/routine/<string:user_id>', methods=['POST', 'GET'])
def create_new_split(user_id):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    if request.method == 'GET':
        return render_template('new_split.html', user_id=user_id)
    else:
        split = request.form['split']
        split = split.strip().upper()
        user = User.get_by_id(user_id)

        if  split not in user.split_list:
            user.split_list.append(split)
            Database.update(collection='users', query={'_id':user_id}, data=user.json())

        return redirect(f'/users/welcome/{user_id}')


@exercise_blueprint.route('/delete/confirmation/<string:split>/<string:user_id>')
def delete_routine_confirmation(split, user_id):
    return render_template('delete_routine.html', split=split, user_id=user_id)


@exercise_blueprint.route('/delete/<string:split>/<string:user_id>')
def delete_routine(split, user_id):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    user = User.get_by_id(user_id)
    user.split_list.remove(split)
    Database.update('users', {'_id':user_id}, user.json())
    return redirect(f'/users/welcome/{user_id}')


@exercise_blueprint.route('/record/1rm/')
@exercise_blueprint.route('/record/1rm/<string:user_id>')
def graph_1rm(user_id=None):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    if user_id is None:
        user = User.get_by_email(session['email'])
        user_id = user._id
    bench_press = Exercise.get_by_user_id_and_name(user_id, 'BENCH PRESS')
    dead_lift = Exercise.get_by_user_id_and_name(user_id,'DEAD LIFT')
    squat = Exercise.get_by_user_id_and_name(user_id, 'SQUAT')
    records = {
        "BENCH PRESS": None,
        "DEAD LIFT": None,
        "SQUAT": None
    }
    if bench_press is not None:
        records['BENCH PRESS'] = [(utils.calculate_1rm(weight=e['weight'], reps=e['reps']), e['date']) for e in bench_press.record]
    if dead_lift is not None:
        records['DEAD LIFT'] = [(utils.calculate_1rm(weight=e['weight'], reps=e['reps']), e['date']) for e in dead_lift.record]
    if squat is not None:
        records['SQUAT'] = [(utils.calculate_1rm(weight=e['weight'], reps=e['reps']), e['date']) for e in squat.record]

    bench_graph = utils.create_graph(records, 'BENCH PRESS')
    dead_graph = utils.create_graph(records, 'DEAD LIFT')
    squat_graph = utils.create_graph(records, 'SQUAT')

    # Data structure of each list [(1RM, date), (),(),()]
    # 1rm are of strings
    return render_template('graph_1rm.html', bench_graph=bench_graph, dead_graph=dead_graph, squat_graph=squat_graph)


@exercise_blueprint.route('/weight_suggestion/<string:user_id>')
@exercise_blueprint.route('/weight_suggestion/')
def weight_suggestion(user_id=None):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    reps_sets = [(8,4),(12,3),(5,5),(16,3),(3,6)]
    if user_id is None:
        user = User.get_by_email(session['email'])
    else:
        user = User.get_by_id(user_id)

    counter_bench = user.big3_counter['BENCH PRESS'] % 5
    counter_squat = user.big3_counter['SQUAT'] % 5
    counter_dead = user.big3_counter['DEAD LIFT'] % 5
    weight_bench = utils.from_1rm(user.big3_max['BENCH PRESS'], reps_sets[counter_bench][1])
    weight_dead = utils.from_1rm(user.big3_max['DEAD LIFT'], reps_sets[counter_dead][1])
    weight_squat = utils.from_1rm(user.big3_max['SQUAT'], reps_sets[counter_squat][1])
    suggestion = {
        'bench': [weight_bench, reps_sets[counter_bench][0], reps_sets[counter_bench][1]],
        'dead': [weight_dead, reps_sets[counter_dead][0], reps_sets[counter_dead][1]],
        'squat':[weight_squat, reps_sets[counter_squat][0], reps_sets[counter_squat][1]]
    }
    return render_template('weight_suggestion.html', suggestion=suggestion)


@exercise_blueprint.route('/update/1rm/<string:user_id>', methods=['GET', 'POST'])
def update_1rm(user_id):
    if session['email'] is None:
        flash('You are not logged in')
        return redirect('/')
    if request.method == 'GET':
        return render_template('update_1rm.html', user_id=user_id)
    else:
        weights = [8,15,5,10,3]
        user = User.get_by_id(user_id)
        bench = request.form['bench']
        squat = request.form['squat']
        dead = request.form['dead']
        user =User.get_by_id(user_id)
        user.big3_max['BENCH PRESS'] = int(bench)
        user.big3_max['DEAD LIFT'] = int(dead)
        user.big3_max['SQUAT'] = int(squat)
        Database.update('users', {'_id':user_id}, user.json())
        return redirect(f'/users/welcome/{user_id}')


@exercise_blueprint.route('/history/<string:exercise_id>')
def history(exercise_id):
    exercise = Exercise.get_by_id(exercise_id)
    return render_template('history.html', exercise=exercise)