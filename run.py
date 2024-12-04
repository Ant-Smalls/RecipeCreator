from app.main import app

app.name = "app"

if __name__ == "__main__":
    app.run(debug=True, port=8080)
