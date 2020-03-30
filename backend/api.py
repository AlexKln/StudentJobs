from flask_restful import Resource, Api
from app import app, db
from scraper import Scraper
import models
import resources

api = Api(app)

scraper = Scraper(db)
scraper.activate()  # Scraping on diff thread for faster launchtime


class Home(Resource):
    def get(self):
        jobs = models.Job.query.all()
        job_schema = models.JobSchema(many=True)
        output = job_schema.dump(jobs).data
        return output


api.add_resource(Home, '/')
api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.ValidateToken, '/validate')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
