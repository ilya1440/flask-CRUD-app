from application import my_app as app

app = app.create_app()


if __name__ == '__main__':
    app.run(debug=False)
