from definitions import loadMoviesDictionary, FILE_SIZE_LIMIT,writeDataToFile,format_bytes

moviesCountWithMultipleVersions = 0
versionsTooMany = []
versionsMoreThanOne = []
overFileLimit = []
totalOverLimitFileSize = 0

if __name__ == "__main__":
    movies = loadMoviesDictionary()
    for movieName, versions in movies.items():
        
        # Count versions
        if len(versions) > 1:
            moviesCountWithMultipleVersions = moviesCountWithMultipleVersions + 1
        if len(versions) > 3:
            versionsTooMany.append(f"[{len(version)}] - {movieName}")
        if len(versions) > 1 and len(versions) <= 3:
            versionsMoreThanOne.append(f"[{len(versions)}] - {movieName}")
        
        for version in versions:    
            #File Size Check
            if version["filesize"] > FILE_SIZE_LIMIT:
                totalOverLimitFileSize = totalOverLimitFileSize + version["filesize"]
                overFileLimit.append(version)

    
    writeDataToFile("overFileLimit.txt", overFileLimit)
    writeDataToFile("versionsTooMany.txt", versionsTooMany)
    writeDataToFile("versionsMoreThanOne.txt", versionsMoreThanOne)


    print("\nTotal movies count: " + str(len(movies)))
    print("\nMovies with multiple versions: " + str(moviesCountWithMultipleVersions))

    print(f"\n Total over file size limit data filesize: {format_bytes(totalOverLimitFileSize)}")