from owlready2 import *

# -------------------------
# Load ontology
# -------------------------
onto = get_ontology("my_music_extended.rdf.owl").load()

# Bind the namespace from the ontology
mymusic = onto.get_namespace("http://example.org/myMusic#")

# -------------------------
# Run reasoner
# -------------------------
with onto:
    print("* Running reasoner (HermiT)...")
    sync_reasoner()  # applies SWRL rules and infers classes

print("\n=== OntOLOGY LOADED & REASONED ===\n")

# -------------------------
# Access classes safely via namespace
# -------------------------
Song = mymusic.Song
Artist = mymusic.Artist
Playlist = mymusic.Playlist
Person = mymusic.Person
PopularSong = mymusic.PopularSong
ShortSong = mymusic.ShortSong
AwardWinningSong = mymusic.AwardWinningSong

# -------------------------
# Function 1: List all songs
# -------------------------
def list_songs():
    print(" Songs in ontology:")
    for song in Song.instances():
        artist = getattr(song, "hasArtist", None)
        artist_name = artist.name if artist else "Unknown"
        duration = getattr(song, "duration", "Unknown")
        rating = getattr(song, "rating", "Unknown")
        play_count = getattr(song, "playCount", "Unknown")
        print(f"- {song.name} | Artist: {artist_name} | Duration: {duration}s | Rating: {rating} | Plays: {play_count}")

# -------------------------
# Function 2: List all artists
# -------------------------
def list_artists():
    print("\n Artists in ontology:")
    for artist in Artist.instances():
        award = getattr(artist, "hasAward", ["None"])
        print(f"- {artist.name} | Award: {award}")

# -------------------------
# Function 3: List inferred classes
# -------------------------
def list_inferred_classes():
    print("\n Inferred classes:")
    if PopularSong:
        print("Popular Songs:")
        for song in PopularSong.instances():
            print(f"  - {song.name}")
    if ShortSong:
        print("Short Songs:")
        for song in ShortSong.instances():
            print(f"  - {song.name}")
    if AwardWinningSong:
        print("Award Winning Songs:")
        for song in AwardWinningSong.instances():
            print(f"  - {song.name}")

# -------------------------
# Function 4: List playlists and their songs
# -------------------------
def list_playlists():
    print("\n Playlists and songs:")
    for playlist in Playlist.instances():
        songs_in_playlist = [s.name for s in Song.instances() if playlist in getattr(s, "inPlaylist", [])]
        print(f"- {playlist.name}: {songs_in_playlist}")

# -------------------------
# Function 5: Recommend songs for a person based on likes
# -------------------------
def recommend_songs_for_person(person_name_or_object):
    """
    Recommend songs for a person based on their likes.

    Args:
        person_name_or_object: Either a string (person name like "Me", "Mariya")
                              or a Person object from the ontology
    """
    # Handle both string (name) and Person object inputs
    if isinstance(person_name_or_object, str):
        # Find the person by name
        person = None
        for p in Person.instances():
            if p.name == person_name_or_object:
                person = p
                break

        if person is None:
            print(f" Error: Person '{person_name_or_object}' not found!")
            return
        person_name = person_name_or_object
    else:
        # Assume it's a Person object
        person = person_name_or_object
        if person is None:
            print("Person not found!")
            return
        person_name = person.name

    liked_songs = getattr(person, "likes", [])
    recommendations = []
    for song in Song.instances():
        if song not in liked_songs:
            recommendations.append(song.name)
    print(f"\n Recommended songs for {person_name}: {recommendations}")

# -------------------------
# Function 6: Add favorite song to user's favorites playlist
# -------------------------
def add_favorite_to_playlist(person_name, song_name):
    """
    Add a favorite song to a user's personal favorites playlist.
    Creates the favorites playlist if it doesn't exist.

    Args:
        person_name: Name of the person (e.g., "Me", "Mariya", "Miya")
        song_name: Name of the song to add (e.g., "LonelyAtTheTop", "GameOver")
    """
    with onto:
        # Find the person
        person = None
        for p in Person.instances():
            if p.name == person_name:
                person = p
                break

        if person is None:
            print(f" Error: Person '{person_name}' not found!")
            return False

        # Find the song
        song = None
        for s in Song.instances():
            if s.name == song_name:
                song = s
                break

        if song is None:
            print(f" Error: Song '{song_name}' not found!")
            return False

        # Create or find the favorites playlist name
        favorites_playlist_name = f"{person_name}Favorites"

        # Check if the favorites playlist already exists
        favorites_playlist = None
        for pl in Playlist.instances():
            if pl.name == favorites_playlist_name:
                favorites_playlist = pl
                break

        # Create the favorites playlist if it doesn't exist
        if favorites_playlist is None:
            favorites_playlist = Playlist(favorites_playlist_name)
            print(f" Created new favorites playlist: {favorites_playlist_name}")
        else:
            print(f" Using existing favorites playlist: {favorites_playlist_name}")

        # Check if the song is already in the playlist
        current_playlists = getattr(song, "inPlaylist", [])
        if favorites_playlist in current_playlists:
            print(f"  Song '{song_name}' is already in {person_name}'s favorites playlist")
            return True

        # Add the song to the playlist
        current_playlists.append(favorites_playlist)
        song.inPlaylist = current_playlists

        # Also mark that the person likes this song (if not already)
        liked_songs = getattr(person, "likes", [])
        if song not in liked_songs:
            liked_songs.append(song)
            person.likes = liked_songs

        print(f" Added '{song_name}' to {person_name}'s favorites playlist")
        return True


# -------------------------
# Function 7: Show user's favorites playlist
# -------------------------
def show_user_favorites(person_name):
    """
    Display all songs in a user's favorites playlist.

    Args:
        person_name: Name of the person (e.g., "Me", "Mariya", "Miya")
    """
    favorites_playlist_name = f"{person_name}Favorites"

    # Find the favorites playlist
    favorites_playlist = None
    for pl in Playlist.instances():
        if pl.name == favorites_playlist_name:
            favorites_playlist = pl
            break

    if favorites_playlist is None:
        print(f" {person_name} doesn't have a favorites playlist yet")
        return

    # Get all songs in this playlist
    songs_in_favorites = [song for song in Song.instances()
                          if favorites_playlist in getattr(song, "inPlaylist", [])]

    if songs_in_favorites:
        song_names = [song.name for song in songs_in_favorites]
        print(f"\n {person_name}'s Favorites Playlist ({len(song_names)} songs):")
        for i, song_name in enumerate(song_names, 1):
            print(f"   {i}. {song_name}")
    else:
        print(f" {person_name}'s favorites playlist is empty")

# -------------------------
# MAIN PROGRAM
# -------------------------
if __name__ == "__main__":
    #List all the songs in the onthology
    list_songs()
    #List all the artists in the onthology
    list_artists()
    #List inferred classes
    list_inferred_classes()
    #List all the playlists in the onthology
    list_playlists()
    # Example: Add some favorite songs to users' playlists
    print("\n--- Adding favorites to playlists ---")
    add_favorite_to_playlist("Me", "LonelyAtTheTop")
    add_favorite_to_playlist("Me", "EndOfSummer")
    add_favorite_to_playlist("Me", "LoveMeNot")

    add_favorite_to_playlist("Mariya", "TheManifesto")
    add_favorite_to_playlist("Mariya", "JealousType")

    add_favorite_to_playlist("Miya", "EndOfSummer")
    add_favorite_to_playlist("Miya", "GameOver")

    # Show users' favorites playlists
    print("\n--- User Favorites Playlists ---")
    show_user_favorites("Me")
    show_user_favorites("Mariya")
    show_user_favorites("Miya")

    #Recommend songs for specified user
    recommend_songs_for_person("Me")
    # Loop logic to go through all People (including the Artists)
    #for user in Person.instances():
        #recommend_songs_for_person(user)

