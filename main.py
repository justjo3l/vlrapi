from flask import Flask
from flask_restful import Api, Resource

from scrapeFiles import scrapeMatches
from scrapeFiles import scrapeMatch

app = Flask(__name__)
api = Api(app)
class Matches(Resource):
    def get(self, match_count):
        result = scrapeMatches.find_matches(match_count)
        return result

class Match(Resource):
    def get(self, match_id):
        result = scrapeMatch.find_match(match_id)
        return result
 


api.add_resource(Matches, "/matches/<int:match_count>")
api.add_resource(Match, "/match/<int:match_id>")

if __name__ == "__main__":
    app.run(debug=True)
