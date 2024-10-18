import os

# Function to get the replacement string based on directory depth
def get_replacement_string(depth):
    return '.' * depth + 'toolkit'

# Function to perform the string replacement in files
def replace_in_files(directory, search_string):
    # Loop over files in the directory and subdirectories
    for root, _, files in os.walk(directory):
        # Calculate directory depth relative to the current working directory
        depth = root.count(os.sep) - directory.count(os.sep)

        # Loop through each file
        for file in files:
            # Ignore __init__.py
            if file == "__init__.py":
                continue

            file_path = os.path.join(root, file)

            # Read the file content
            with open(file_path, 'r') as f:
                content = f.read()

            # Get the replacement string based on the current directory depth
            replace_string = get_replacement_string(depth)

            # Replace occurrences of the search string
            updated_content = content.replace(search_string, replace_string)

            # Write back the updated content to the file only if changes were made
            if updated_content != content:
                with open(file_path, 'w') as f:
                    f.write(updated_content)

            # Print information about the replacement
            print(f"Replaced '{search_string}' with '{replace_string}' in file: {file_path}")

# Main function to be run when script is executed
def main():
    breakpoint()
    # Directory to search (current directory)
    directory = '.'
   
    # The string to search for
    search_string = ""
    
    # Perform the replacement in files
    replace_in_files(directory, search_string)
    
    print("Replacement done.")


# Ensure the script runs only if executed directly (not imported)
if __name__ == '__main__':
    main()
