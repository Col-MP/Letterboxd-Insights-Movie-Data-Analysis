# Function to check for duplicate URLs in a file
def check_for_duplicates(file_path):
    # Open the file and read all URLs into a list
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    seen = set()  # Set to keep track of seen URLs
    duplicates = set()  # Set to keep track of duplicate URLs
    unique_urls = []  # List to store unique URLs

    # Iterate over each URL
    for url in urls:
        if url in seen:
            # If URL is already in seen set, add to duplicates set
            duplicates.add(url)
        else:
            # If URL is not in seen set, add to seen set and unique_urls list
            seen.add(url)
            unique_urls.append(url)

    # Print duplicate URLs if any
    if duplicates:
        print("Found duplicates:")
        for duplicate in duplicates:
            print(duplicate)
    else:
        print("No duplicates found.")

    # Save unique URLs to a new file
    with open('final_movie_urls.txt', 'w') as f:
        for url in unique_urls:
            f.write(url + '\n')

    print("Unique URLs have been saved to final_movie_urls.txt")

# Run the check
check_for_duplicates('movie_urls.txt')
