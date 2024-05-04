from flask import jsonify, Blueprint, request
from event_scraper import generate_events
import json

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def user_portal():
    response_object = {'status':'success'}

    if request.method == "GET":
            user_id = request.args.get('user_id')


            if not user_id:
                response_object['status'] = 'error'
                response_object['msg'] = 'user_id param is missing'
                return jsonify(response_object)
            
            try:
                event_data = generate_events()
                response_object['data']=event_data
                return jsonify(response_object)
            
            except ValueError:
                response_object['status'] = 'error'
                response_object['msg'] = 'Invalid user_id'
                return jsonify(response_object)
