from flask import Flask
from flask_restful import Api, Resource

from scrapeFiles import scrapeMatches
from scrapeFiles import scrapeMatch

app = Flask(__name__)
api = Api(app)
class Matches(Resource):
    def get(self, match_count, match_type):
        result = scrapeMatches.find_matches(match_count, match_type)
        return result

class Match(Resource):
    def get(self, match_id, match_type):
        result = scrapeMatch.find_match(match_id, match_type)
        return result
 


api.add_resource(Matches, "/matches/<int:match_count>/<string:match_type>")
api.add_resource(Match, "/match/<int:match_id>/<string:match_type>")

if __name__ == "__main__":
    app.run(debug=True)
