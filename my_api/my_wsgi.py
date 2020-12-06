"""
DATE: 12/02/2020
NAME: Hector Carrillo
DESCRIPTION: WSGI server set use_reloader and debug false for production
"""


from my_api.app import app

if __name__ == "__main__":
    app.run(use_reloader=False, debug=False)