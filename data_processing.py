import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to read data from a text file
def read_movie_data(file_path):
    movies_data = []  # Initialize an empty list to store movie data
    with open(file_path, 'r') as f:
        movie_data_str = f.read().strip().split('\n\n')  # Read the file and split movie entries by double newlines
        for movie_str in movie_data_str:
            movie = json.loads(movie_str)  # Parse each movie entry as a JSON object
            movies_data.append(movie)  # Append the movie data to the list
    return movies_data

# Function to clean and process data
def process_movie_data(movies_data):
    df = pd.DataFrame(movies_data)  # Convert the list of movie data into a DataFrame
    df['rating'] = df['rating'].str.extract(r'(\d+\.\d+)').astype(float)  # Extract numeric rating and convert to float
    df['year'] = df['title'].str.extract(r'\((\d{4})\)').astype(int)  # Extract year from title and convert to int
    df['genres'] = df['genres'].apply(lambda x: x if isinstance(x, list) else [])  # Ensure genres is a list
    return df

# Function to analyze data
def analyze_movie_data(df):
    highest_rated = df.sort_values(by='rating', ascending=False).head(10)  # Get the top 10 highest-rated movies
    return highest_rated

# Function to plot histogram
def plot_histogram(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df['rating'], bins=[0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], edgecolor='black')  # Plot histogram of ratings
    plt.title('Histogram of Movie Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')  # Frequency shows the count of movies in each rating bin
    plt.xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])  # Set x-axis ticks
    plt.show()

# Function to plot pie chart
def plot_pie_chart(df):
    rating_categories = ['0-1', '1-2', '2-3', '3-4', '4-5']  # Define rating categories
    bins = [0, 1, 2, 3, 4, 5]  # Define bin edges for categorizing ratings
    df['rating_category'] = pd.cut(df['rating'], bins=bins, labels=rating_categories, include_lowest=True)  # Bin the ratings
    rating_counts = df['rating_category'].value_counts().sort_index()  # Count the number of movies in each category
    
    plt.figure(figsize=(8, 8))
    plt.pie(rating_counts, labels=rating_categories, autopct='%1.1f%%', startangle=140)  # Plot pie chart
    plt.title('Distribution of Movie Ratings')
    plt.show()

# Function to plot bar chart for top 10 highest-rated movies
def plot_bar_chart(highest_rated):
    plt.figure(figsize=(12, 8))
    highest_rated = highest_rated.iloc[::-1]  # Reverse the order for better display
    plt.bar(highest_rated['title'], highest_rated['rating'], color='skyblue')  # Plot bar chart
    plt.ylim(0, 5)  # Set y-axis limits
    plt.yticks([i * 0.5 for i in range(11)])  # Set y-axis ticks
    plt.xlabel('Movie Title')
    plt.ylabel('Rating')
    plt.title('Top 10 Highest Rated Movies')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.show()

# Function to plot scatter plot
def plot_scatter(df, highest_rated):
    plt.figure(figsize=(12, 8))
    all_movies_index = range(len(df))  # Get index range for all movies
    top_movies_index = highest_rated.index  # Get index for top 10 movies

    plt.scatter(all_movies_index, df['rating'], color='green', alpha=0.5, label='Other Movies')  # Plot scatter for all movies
    plt.scatter(top_movies_index, highest_rated['rating'], color='red', alpha=1, label='Top 10 Movies')  # Highlight top 10 movies
    plt.ylim(0, 5)  # Set y-axis limits
    plt.yticks([i * 0.5 for i in range(11)])  # Set y-axis ticks

    # Adjust xticks to match the number of movies
    step = max(1, len(df) // 5)
    tick_labels = ['2020', '2021', '2022', '2023', '2024']
    tick_positions = range(0, len(df), step)
    if len(tick_positions) > len(tick_labels):
        tick_positions = tick_positions[:len(tick_labels)]
    plt.xticks(tick_positions, tick_labels[:len(tick_positions)])

    plt.xlabel('Movies')
    plt.ylabel('Rating')
    plt.title('Ratings of All Movies')
    plt.legend(loc='best')
    plt.show()

# Function to plot heatmap
def plot_heatmap(df):
    genres = df['genres'].explode().unique()  # Get unique genres
    genre_ratings = {genre: [] for genre in genres}  # Initialize a dictionary to store ratings for each genre

    for _, row in df.iterrows():
        for genre in row['genres']:
            genre_ratings[genre].append(row['rating'])  # Append ratings to respective genre lists

    avg_genre_ratings = {genre: sum(ratings)/len(ratings) for genre, ratings in genre_ratings.items()}  # Calculate average ratings for each genre
    genre_ratings_df = pd.DataFrame(list(avg_genre_ratings.items()), columns=['Genre', 'Average Rating'])  # Convert to DataFrame

    genre_ratings_df = genre_ratings_df.sort_values(by='Average Rating', ascending=False)  # Sort genres by average rating

    plt.figure(figsize=(12, 8))
    sns.heatmap(genre_ratings_df.pivot_table(values='Average Rating', index='Genre'), annot=True, cmap='coolwarm', cbar_kws={'label': 'Average Rating'})  # Plot heatmap
    plt.title('Heatmap of Average Ratings by Genre')
    plt.show()

# Main function
def main():
    movies_data = read_movie_data('movies_data.txt')  # Read movie data from file
    df = process_movie_data(movies_data)  # Clean and process the data
    highest_rated = analyze_movie_data(df)  # Analyze the data to get top 10 highest-rated movies

    print("Top 10 Highest Rated Movies:")
    print(highest_rated[['title', 'rating']])  # Print the top 10 highest-rated movies

    # Plotting the charts on separate pages
    plot_histogram(df)  # Plot histogram
    plot_pie_chart(df)  # Plot pie chart
    plot_bar_chart(highest_rated)  # Plot bar chart
    plot_scatter(df, highest_rated)  # Plot scatter plot
    plot_heatmap(df)  # Plot heatmap

if __name__ == "__main__":
    main()  # Execute the main function
