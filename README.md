# vlr-api
 An Unofficial REST API for [vlr.gg](https://www.vlr.gg/), the website for Valorant Esports matches, news and data.

# Current Endpoints
 All endpoints are relative to ().
 
### ```/match/<id>/preview```

- Method: ```GET```
- ID: Index of match
- Function: Returns the basic details of the match at an index.
- Response:
```javascript
{
    "data": {
        "tournament": {
            "name": str,
            "url": str
        },
        "match": {
            "name": str,
            "type": str
        },
        "date": str,
        "time": str,
        "score": {
            "team1": str,
            "team2": str
        },
        "teams": [
            {
                "name": str,
                "url": str
            }
        ]
    }
}
```

### ```/match/<id>/full```

- Method: ```GET```
- ID: Index of match
- Function: Returns the full details of the match at an index.
- Response:
```javascript
{
    "data": {
        "tournament": {
            "name": str,
            "url": str
        },
        "match": {
            "name": str,
            "type": str
        },
        "date": str,
        "time": str,
        "score": {
            "team1": str,
            "team2": str
        },
        "teams": [
            {
                "name": str,
                "url": str
            }
        ],
        "streams": [
            {
                "name": str,
                "url": str
            }
        ],
        "vods": [
            {
                "name": str,
                "url": str
            }
        ],
        "maps": [
            {
                "name": str,
                "time_played": str,
                "score": {
                    "team1": str,
                    "team2": str,
                    "team1_attack": str,
                    "team2_attack": str,
                    "team1_defend": str,
                    "team2_defend": str
                },
                "players": {
                    "team1": [
                        {
                            "name": str,
                            "agent": str,
                            "ACS": str,
                            "K": str,
                            "D": str,
                            "A": str,
                            "KDA_difference": str,
                            "KAST": str,
                            "ADR": str,
                            "HS%": str,
                            "FK": str,
                            "FD": str,
                            "FK_difference": str
                        }
                    ]
                }
            }
        ]
    }
}
```

### ```/matches/<count>/preview```

- Method: ```GET```
- Count: Number of matches
- Function: Returns the basic details of the matches.
- Response:
```javascript
{
    "data": [
        {
            "tournament": {
                "name": str,
                "url": str
            },
            "match": {
                "name": str,
                "type": str
            },
            "date": str,
            "time": str,
            "score": {
                "team1": str,
                "team2": str
            },
            "teams": [
                {
                    "name": str,
                    "url": str
                }
            ]
        }
    ]   
}
```

### ```/matches/<count>/full```

- Method: ```GET```
- Count: Number of matches
- Function: Returns the full details of the matches.
- Response:
```javascript
{
    "data": [
        {
            "tournament": {
                "name": str,
                "url": str
            },
            "match": {
                "name": str,
                "type": str
            },
            "date": str,
            "time": str,
            "score": {
                "team1": str,
                "team2": str
            },
            "teams": [
                {
                    "name": str,
                    "url": str
                }
            ],
            "streams": [
                {
                    "name": str,
                    "url": str
                }
            ],
            "vods": [
                {
                    "name": str,
                    "url": str
                }
            ],
            "maps": [
                {
                    "name": str,
                    "time_played": str,
                    "score": {
                        "team1": str,
                        "team2": str,
                        "team1_attack": str,
                        "team2_attack": str,
                        "team1_defend": str,
                        "team2_defend": str
                    },
                    "players": {
                        "team1": [
                            {
                                "name": str,
                                "agent": str,
                                "ACS": str,
                                "K": str,
                                "D": str,
                                "A": str,
                                "KDA_difference": str,
                                "KAST": str,
                                "ADR": str,
                                "HS%": str,
                                "FK": str,
                                "FD": str,
                                "FK_difference": str
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```
