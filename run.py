from app import create_app

app = create_app()

# test api
@app.get('/')
def test():
    print('Testing Application...')
    return 'Testing Application...'

# entry point
if __name__ == '__main__': 
    app.run(debug=True)
