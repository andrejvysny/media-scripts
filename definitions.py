import os
import json
import re
from moviepy.editor import VideoFileClip



# Define the directory where your movie folders are located
MOVIES_LOCATION = "E:\media\movies"

# Outputs FILES
OUTPUTS_FOLDER = "result"

MOVIES_DICTIONARY_OUTPUT = "moviesDisctionary.json"

FILE_SIZE_LIMIT = 3500000000
VIDEO_COMPLEX_ANALYSIS = False


VIDEO_EXTENSIONS_TO_COUNT_AND_CHECK = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.divx']
ID_PATTERNS = [r'\[tmdbid-(\d+)\]', r'\[tvdbid-(\d+)\]']





# Versions
VERSIONS_COUNT_BASE_OUTPUT = os.path.join(OUTPUTS_FOLDER,"version_count_base.txt")
VERSIONS_COUNT_OVER_LIMIT_OUTPUT = os.path.join(OUTPUTS_FOLDER,"version_count_over_limit.txt")
VERSIONS_COUNT_LIMIT = 2



if not os.path.exists(OUTPUTS_FOLDER):
    os.mkdir(OUTPUTS_FOLDER)

# ---------------------- END CONFIG ----------------------


def loadMoviesDictionary():
    fullPath = os.path.join(OUTPUTS_FOLDER,MOVIES_DICTIONARY_OUTPUT)
    if os.path.exists(fullPath):
        with open(fullPath, 'r') as file:
            data = file.read()
        return json.loads(data)
    

def writeDataToFile(filename, data):
    with open(os.path.join(OUTPUTS_FOLDER,filename), 'w') as file:
        for item in data:
            file.write(str(item) + '\n')



# ---------------------- DATA EXTRACTION METHODS ----------------------

# Function to extract ID from string
def extractId(strongToExtractFrom):
    for pattern in ID_PATTERNS:
        match = re.search(pattern, strongToExtractFrom)
        if match:
            return match.group(0).replace("[","").replace("]","")
    return None


# Analyse given video file and returns dictionary with data about file
def analyseVideoFile(movie_directory, directory, filename, complexAnalysis = False):

    fileFullPath = os.path.join(movie_directory,directory,filename)

    if complexAnalysis:
        video_clip = VideoFileClip(fileFullPath)
        videoMetadata = {
            "size": video_clip.size,
            "duration": video_clip.duration,
            "frame_rate": video_clip.fps,
            "resolution": f"{video_clip.size[0]}x{video_clip.size[1]}",
        }
    else:
        videoMetadata = None

    return {
        "filename" : filename,
        "extension": os.path.splitext(filename)[1].lower(),
        "filesize" : os.path.getsize(fileFullPath),
        "filesize_format": format_bytes(os.path.getsize(fileFullPath)),
        "metadata": videoMetadata,
    }



# ---------------------- FORMATTING METHODS ----------------------

def format_bytes(size_bytes, precision=2):
    size_bytes = float(size_bytes)
    kb = 1024
    mb = kb ** 2
    gb = kb ** 3
    if size_bytes < mb:
        return f"{size_bytes / kb:.{precision}f} KB"
    elif size_bytes < gb:
        return f"{size_bytes / mb:.{precision}f} MB"
    else:
        return f"{size_bytes / gb:.{precision}f} GB"
    





# ---------------------- LISTING METHODS ----------------------


# List files in given directory and analyse file with analyseVideoFile() method
def listFilesInDirectory(directoryName):
    filesInDirectory = list()
    directoryFullPath = os.path.join(MOVIES_LOCATION, directoryName)
    for filename in os.listdir(directoryFullPath):
        if os.path.isfile(os.path.join(directoryFullPath, filename)):
            if os.path.splitext(filename)[1].lower() in VIDEO_EXTENSIONS_TO_COUNT_AND_CHECK:
                filesInDirectory.append(
                    analyseVideoFile(MOVIES_LOCATION, directoryName, filename, VIDEO_COMPLEX_ANALYSIS)
                )
    return filesInDirectory



# Iterate through the directories in MOVIES_LOCATION and returns dictionary with listed files
def listMoviesAndSaveJson():
    moviesDictionary = {}
    print("\nSTART LISTING ...")
    for root, dirs, files in os.walk(MOVIES_LOCATION):
        for directoryName in dirs:
            moviesDictionary[directoryName] = listFilesInDirectory(directoryName)
            print (f" -- [{str(len(moviesDictionary[directoryName]))}] - {directoryName}")
    print("END LISTING ...\n")

    # Write the dictionary to a JSON file
    fullSavePath = os.path.join(OUTPUTS_FOLDER,MOVIES_DICTIONARY_OUTPUT)
    with open(fullSavePath, "w") as json_file:
        json.dump(moviesDictionary, json_file)
    print(f"LIST SAVED TO: {fullSavePath}\n\n")

    return moviesDictionary


