from linkedlist import app, models

def run():
    models.create_tables()
    app.run()

if __name__ == "__main__":
	run()
