from app import create_app
from flask import redirect

app = create_app()

@app.route('/')
def index():
    return redirect('/inicio/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)