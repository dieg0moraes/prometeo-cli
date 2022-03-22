"""
Entry point script.
"""
# prometeo/__main__.py

from pmo import prometeo, __app_name__

def main():
    prometeo.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()

