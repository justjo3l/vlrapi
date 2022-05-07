from flask import Flask
from flask_restful import Api, Resource

from scrapeFiles import scrapeFullMatches
from scrapeFiles import scrapeFullMatch
from scrapeFiles import scrapeBasicMatch
from scrapeFiles import scrapeBasicMatches

app = Flask(__name__)
api = Api(app)

class BasicMatches(Resource):
    def get(self, match_count):
        result = scrapeBasicMatches.find_matches(match_count)
        return result

class BasicMatch(Resource):
    def get(self, match_id):
        result = scrapeBasicMatch.find_match(match_id)
        return result

class FullMatches(Resource):
    def get(self, match_count):
        result = scrapeFullMatches.find_matches(match_count)
        return result

class FullMatch(Resource):
    def get(self, match_id):
        result = scrapeFullMatch.find_match(match_id)
        return result
 

api.add_resource(BasicMatches, "/matches/<int:match_count>")
api.add_resource(FullMatches, "/matches/<int:match_count>/full")
api.add_resource(BasicMatch, "/match/<int:match_id>")
api.add_resource(FullMatch, "/match/<int:match_id>/full")

if __name__ == "__main__":
    app.run(debug=True)
