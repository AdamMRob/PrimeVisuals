import webbrowser
import tempfile
import os
from src.laser_builder import HTML


def main():
    path = os.path.join(tempfile.gettempdir(), "laser_plane_visualiser.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print("Opening browser...")
    webbrowser.open(f"file:///{path}")


if __name__ == "__main__":
    main()
