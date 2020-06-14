from kaguya import create_app

if __name__ == "__main__":
    app = create_app(create_db=True)
    app.run(debug=app.config['DEBUG_MODE'])
