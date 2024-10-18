
import os

# Function to get the replacement string based on directory depth
def get_replacement_string(depth):
    if depth == 0: return ''
    return '.' * depth


def get_path_lenth(file_path):
    splt = file_path.split(os.sep)
    splt = list(filter(lambda x: x != '' and x != '.', splt))
    l = len(splt)
    return l


# Function to perform the string replacement in files
def replace_in_files(directory, search_string):
    # Loop over files in the directory and subdirectories
    for root, _, files in os.walk(directory):
        # Calculate directory depth relative to the current working directory
        depth = get_path_lenth(root) - get_path_lenth(directory)

        # Loop through each file
        for file in files:

            file_path = os.path.join(root, file)
            if file_path.endswith('.pyc'):
                print('ignoring binary file: {}'.format(file_path))
                continue

            # Read the file content
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
            except Exception as e:
                print('unable to read file: {}\nException{}\n'.format(file_path, e))
                continue

            # Get the replacement string based on the current directory depth
            replace_string = get_replacement_string(depth)

            if search_string not in content: continue

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
    directory = './pyvim/toolkit/'
    
    # The string to search for
    search_string = "prompt_toolkit"
    
    # Perform the replacement in files
    replace_in_files(directory, search_string)
    
    print("Replacement done.")

# Ensure the script runs only if executed directly (not imported)
if __name__ == '__main__':
    main()
