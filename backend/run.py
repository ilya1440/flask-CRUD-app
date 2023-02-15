from application import my_app

flask_app = my_app.create_app()


if __name__ == '__main__':
    flask_app.run(debug=False)
