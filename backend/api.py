from flask_restful import Resource, Api
from app import app, db
from scraper import Scraper

api = Api(app)

scraper = Scraper(db)
scraper.scrape()

import models, resources

class Home(Resource):
    def get(self):
        jobs = models.Job.query.all()
        job_schema = models.JobSchema(many=True)
        output = job_schema.dump(jobs).data
        return output


# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
        # return 'Subpath %s' % escape(subpath)

api.add_resource(Home, '/')
api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.ValidateToken, '/validate')

if __name__ == '__main__':
    app.run(debug=True)
