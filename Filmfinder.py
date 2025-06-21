import tkinter as tk
from tkinter import ttk
import imdb

# Create an instance of the IMDb class
ia = imdb.IMDb()

# Function to get top-rated movies by genre and language
def get_top_rated_movies_by_genre(genre, language, num_movies=10):
    try:
        # Search for movies based on genre and language
        results = ia.search_movie(f"{genre} {language}")[0:num_movies]
        
        # Filter out TV shows and non-feature films
        movies = [result for result in results if 'movie' in result.data['kind'] and 'tv' not in result.data['kind']]
        
        # Sort the movies by rating
        top_rated_movies = sorted(movies, key=lambda x: x.data.get('rating', 0), reverse=True)
        
        return top_rated_movies[:num_movies]
    except imdb.IMDbDataAccessError as e:
        print(f"Error occurred. Unable to fetch movie details: {e}")
        return None

# Function to display movie suggestions
def show_suggestions():
    selected_genre = genre_combobox.get()
    selected_language = language_combobox.get()
    suggestions_tree.delete(*suggestions_tree.get_children())  # Clear previous suggestions

    if selected_genre and selected_language:
        movies = get_top_rated_movies_by_genre(selected_genre, selected_language)

        if movies:
            for movie in movies:
                title = movie['title']
                year = movie.data.get('year', 'N/A')
                suggestions_tree.insert("", "end", values=(title, year))
        else:
            suggestions_tree.insert("", "end", values=("Unable to fetch movie suggestions", ""))

# Function to search for a specific movie
def search_movie():
    movie_name = search_entry.get()
    if movie_name:
        search_results = ia.search_movie(movie_name)
        if search_results:
            selected_movie = search_results[0]
            show_movie_details(selected_movie)
        else:
            details_text.delete(1.0, tk.END)
            details_text.insert(tk.END, "Movie not found in the database.")
    else:
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, "Please enter a movie name to search.")

# Function to display details of a specific movie
def show_movie_details(movie):
    ia.update(movie)
    details_text.delete(1.0, tk.END)
    title = movie.get('title', 'N/A')
    year = movie.get('year', 'N/A')
    rating = movie.get('rating', 'N/A')
    directors = ', '.join(director['name'] if 'name' in director else 'N/A' for director in movie.get('directors', []))
    writers = ', '.join(writer['name'] if 'name' in writer else 'N/A' for writer in movie.get('writers', []))
    cast = ', '.join(actor['name'] if 'name' in actor else 'N/A' for actor in movie.get('cast', []))
    details_text.insert(tk.END, f"Title: {title}\n")
    details_text.insert(tk.END, f"Year: {year}\n")
    details_text.insert(tk.END, f"Rating: {rating}\n")
    details_text.insert(tk.END, f"Directors: {directors}\n")
    details_text.insert(tk.END, f"Writers: {writers}\n")
    details_text.insert(tk.END, f"Cast: {cast}\n")

# Create the main window
window = tk.Tk()
window.title("Movie Suggestions App")

# Create genre selection
genre_label = tk.Label(window, text="Select Genre:")
genre_label.grid(row=0, column=0, pady=10)

genres = ["Action", "Adventure", "Animation", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller"]
genre_combobox = ttk.Combobox(window, values=genres)
genre_combobox.grid(row=0, column=1, pady=10)

# Create language selection
language_label = tk.Label(window, text="Select Language:")
language_label.grid(row=1, column=0, pady=10)

languages = ["English", "Spanish", "French", "German", "Italian", "Japanese", "Chinese", "Korean", "Russian", "Portuguese", "Arabic", "Hindi"]
language_combobox = ttk.Combobox(window, values=languages)
language_combobox.grid(row=1, column=1, pady=10)

# Create a button to get suggestions
get_suggestions_button = tk.Button(window, text="Get Suggestions", command=show_suggestions)
get_suggestions_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create a search bar to search for movies
search_label = tk.Label(window, text="Search Movie:")
search_label.grid(row=3, column=0, pady=10)

search_entry = ttk.Entry(window)
search_entry.grid(row=3, column=1, pady=10)

search_button = ttk.Button(window, text="Search", command=search_movie)
search_button.grid(row=3, column=2, pady=10)

# Create a treeview widget to display suggestions in tabular format
suggestions_tree = ttk.Treeview(window, columns=("Name", "Year"), show="headings")
suggestions_tree.heading("Name", text="Name")
suggestions_tree.heading("Year", text="Year")
suggestions_tree.grid(row=4, column=0, columnspan=2, pady=10)

# Create a text widget to display movie details
details_text = tk.Text(window, height=15, width=80, wrap=tk.WORD)
details_text.grid(row=5, column=0, columnspan=3, pady=10)

# Run the main loop
window.mainloop()



