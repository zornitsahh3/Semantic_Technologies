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
    print("🎵 Songs in ontology:")
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
    print("\n🎤 Artists in ontology:")
    for artist in Artist.instances():
        award = getattr(artist, "hasAward", ["None"])
        print(f"- {artist.name} | Award: {award}")

# -------------------------
# Function 3: List inferred classes
# -------------------------
def list_inferred_classes():
    print("\n📊 Inferred classes:")
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
    print("\n🎧 Playlists and songs:")
    for playlist in Playlist.instances():
        songs_in_playlist = [s.name for s in Song.instances() if playlist in getattr(s, "inPlaylist", [])]
        print(f"- {playlist.name}: {songs_in_playlist}")

# -------------------------
# Function 5: Recommend songs for a person based on likes
# -------------------------
def recommend_songs_for_person(person):
    if person is None:
        print("Person not found!")
        return
    liked_songs = getattr(person, "likes", [])
    recommendations = []
    for song in Song.instances():
        if song not in liked_songs:
            recommendations.append(song.name)
    print(f"\n🎯 Recommended songs for {person.name}: {recommendations}")


# -------------------------
# MAIN PROGRAM
# -------------------------
if __name__ == "__main__":
    list_songs()
    list_artists()
    list_inferred_classes()
    list_playlists()
    # Loop logic to go through all People (including the Artists)
    #for user in Person.instances():
        #recommend_songs_for_person(user)
    
