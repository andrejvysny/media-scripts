
from definitions import MOVIES_LOCATION, loadMoviesDictionary

if __name__ == "__main__":
    movies = loadMoviesDictionary()
    extensions = {}
    for directoryName, versions in movies.items():
        for version in versions:
            currentExtension = version["extension"]
            if currentExtension in extensions:
                extensions[currentExtension] = extensions[currentExtension] + 1
            else:
                extensions[currentExtension] = 1
    print("\n\nCount of video file types:\n")
    for extension in extensions:
        print(f"[{extension}]: {extensions[extension]}")
    print("\n\n")