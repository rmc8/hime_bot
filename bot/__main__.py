import os

from dotenv import load_dotenv

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(THIS_DIR, ".env"))


def main():
    print("Hello World!")


if __name__ == "__main__":
    main()
