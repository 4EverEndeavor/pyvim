import os
import subprocess

def refresh_index_os():
    # Get the CLASSPATH environment variable
    classpath = os.environ.get("CLASSPATH")

    # Check if CLASSPATH is set
    if classpath:
        # Split CLASSPATH by the separator (":" on Unix-like systems, ";" on Windows)
        directories = classpath.split(os.pathsep)
        # TODO add gradle project configuration directories here
        directories.append('/Users/eric/.jar')

        # Output file name
        output_file = "/Users/eric/.vim_indexes/java_class_index"

        # Open the output file for writing
        with open(output_file, "w") as file:
            # Iterate over each directory in CLASSPATH
            for directory in directories:
                # Check if the directory exists
                if os.path.exists(directory):
                    # Walk through all the directories and files in the given directory
                    for root, dirs, files in os.walk(directory):
                        for filename in files:
                            # Check if the file ends with '.class'
                            if filename.endswith(".class"):
                                # Get the full path of the file
                                full_path = os.path.join(root, filename)
                                # Write the file path to the output file
                                file.write(full_path + "\n")

        print(f"File paths with '.class' extension have been written to {output_file}.")
    else:
        print("CLASSPATH environment variable is not set.")

def refresh_index():
    java_file_index= open('/Users/eric/.vim_indexes/java_file_index', 'w')
    subprocess.run(['find', '/Users/eric/', '-type', 'f', '-regex', '.*\.java$'], stdout=java_file_index)
    java_file_index.close()
    java_class_index = open('/Users/eric/.vim_indexes/java_class_index', 'w')
    subprocess.run(['find', '/Users/eric/', '-type', 'f', '-regex', '.*\.class$'], stdout=java_class_index)

refresh_index_os()
