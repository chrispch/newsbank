from eve import Eve
import os

settings_url = os.path.dirname(os.path.realpath(__file__)) + "/settings.py"
app = Eve(settings=settings_url)

if __name__ == "__main__":
    app.run(debug=True)