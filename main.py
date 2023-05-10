from flask import Flask
from flask_restful import Api, Resource

from scrapeFiles import scrapeBasicMatches
from scrapeFiles import scrapeBasicMatch
from scrapeFiles import scrapeFullMatches
from scrapeFiles import scrapeFullMatch
from scrapeFiles import scrapePlayerEventStats

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

class PlayerEventStats(Resource):
    def get(self, player_name, team_code, event_id, stat_code):
        result = scrapePlayerEventStats.find_stats(player_name, team_code, event_id, stat_code)
        return result

api.add_resource(BasicMatches, "/matches/<int:match_count>")
api.add_resource(FullMatches, "/matches/<int:match_count>/full")
api.add_resource(BasicMatch, "/match/<int:match_id>")
api.add_resource(FullMatch, "/match/<int:match_id>/full")
api.add_resource(PlayerEventStats, "/stats/<string:player_name>/<string:team_code>/<int:event_id>/<string:stat_code>")

if __name__ == "__main__":
    app.run(debug=True)
