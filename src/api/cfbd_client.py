import requests

class CFBDataClient:
    def __init__(self, api_key: str):
        self.base_url = "https://apinext.collegefootballdata.com"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
    
    def get_games(self, year: int = None, team: str = None):
        """Fetch games data from the API"""
        endpoint = f"{self.base_url}/games"
        params = {}
        if year:
            params['year'] = year
        if team:
            params['team'] = team
            
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_teams(self, conference: str = None):
        """Fetch teams data from the API"""
        endpoint = f"{self.base_url}/teams"
        params = {}
        if conference:
            params['conference'] = conference
            
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()