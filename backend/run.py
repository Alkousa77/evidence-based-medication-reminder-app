from app import create_app
#create an instance of the flask app
app = create_app()

if __name__ == "__main__":
    # debug=True for development
    app.run(debug=True)