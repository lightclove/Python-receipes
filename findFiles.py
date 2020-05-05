# https://stackoverflow.com/questions/46887870/find-files-with-regex
# I'm trying to find files in a directory.
# The files I'd like to find can be named in two possible ways. It's either a combination of three capital letters and the file extension 
# (e.g.: "ABC.xlsx") or a combination of 3 capital letters, the string "_diff" and the extension (e.g.: "ABC_diff.xlsx").
# This is my code until now:
def find_files(directory): # Function that iterates over files in a directory
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if re.search(r'[A-Z]{3}(_diff)?\.xlsx$', basename):
                basename = os.path.splitext(basename)[0]
                yield basename
########################################################################################################################