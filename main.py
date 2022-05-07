from flask import Flask
from flask_restful import Api, Resource

from scrapeFiles import scrapeMatches
from scrapeFiles import scrapeMatch

app = Flask(__name__)
api = Api(app)

class BasicMatches(Resource):
    def get(self, match_count):
        result = scrapeMatches.find_matches(match_count, "")
        return result

class BasicMatch(Resource):
    def get(self, match_id):
        result = scrapeMatch.find_match(match_id, "")
        return result
class FullMatches(Resource):
    def get(self, match_count, match_type):
        result = scrapeMatches.find_matches(match_count, match_type)
        return result

class FullMatch(Resource):
    def get(self, match_id, match_type):
        result = scrapeMatch.find_match(match_id, match_type)
        return result
 

api.add_resource(BasicMatches, "/matches/<int:match_count>")
api.add_resource(FullMatches, "/matches/<int:match_count>/<string:match_type>")
api.add_resource(BasicMatch, "/match/<int:match_id>")
api.add_resource(FullMatch, "/match/<int:match_id>/<string:match_type>")

if __name__ == "__main__":
    app.run(debug=True)
