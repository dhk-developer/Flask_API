from app.factory import create_app


app = create_app()

@app.route("/")
def welcome():
    return "<h1>Main</h1>"


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8080, debug=True)