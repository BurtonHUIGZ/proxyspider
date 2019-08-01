from angelspider.schedule import Schedule
from angelspider.api import app

def main():
    s = Schedule()
    s.run()
    app.run()

if __name__ == '__main__':
    main()