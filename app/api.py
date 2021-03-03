from flask import Flask
from flask import jsonify
from flask import request
from applicationinsights.flask.ext import AppInsights
from healthcheck import HealthCheck, EnvironmentDump


app_name = 'comentarios'
app = Flask(app_name)
app.debug = True


# Azure Application Insights
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '__APPINSIGHTS_INSTRUMENTATIONKEY__'
appinsights = AppInsights(app)

@app.after_request
def after_request(response):
    appinsights.flush()
    return response


# Health Check
health = HealthCheck()
envdump = EnvironmentDump()

def api_available():
    return True, "api ok"

health.add_check(api_available)

def application_data():
    return {"health check": "ok"}

envdump.add_section("application", application_data)

app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())


comments = {}


@app.route('/api/comment/new', methods=['POST'])
def api_comment_new():
    request_data = request.get_json()

    email = request_data['email']
    comment = request_data['comment']
    content_id = '{}'.format(request_data['content_id'])

    new_comment = {
            'email': email,
            'comment': comment,
            }

    if content_id in comments:
        comments[content_id].append(new_comment)
    else:
        comments[content_id] = [new_comment]

    message = 'comment created and associated with content_id {}'.format(content_id)
    response = {
            'status': 'SUCCESS',
            'message': message,
            }
    return jsonify(response)


@app.route('/api/comment/list/<content_id>')
def api_comment_list(content_id):
    content_id = '{}'.format(content_id)

    if content_id in comments:
        return jsonify(comments[content_id])
    else:
        message = 'content_id {} not found'.format(content_id)
        response = {
                'status': 'NOT-FOUND',
                'message': message,
                }
        return jsonify(response), 404
