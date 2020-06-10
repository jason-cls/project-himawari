from kaguya import create_app

if __name__ == "__main__":
    app = create_app(create_db=False)
    app.run(debug=app.config['DEBUG_MODE'])
