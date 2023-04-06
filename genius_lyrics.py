from lyricsgenius import Genius
from secrets import *
from pathlib import Path
from tqdm import tqdm
import os


# this is the method used by the genius api to handle special characters, but it's applied to the whole string,
# so I cannot divide the files into subdirectories as I would, I keep this to apply it to titles instead
# I modified it to replace whitespaces with '_' because I like it more
def sanitize_filename(f):
    """Removes invalid characters from file name.
    Args:
        f (:obj:`str`): file name to sanitize.
    Returns:
        :obj:`str`: sanitized file name including only alphanumeric
        characters, spaces, dots or underlines.
    """
    keepchars = (" ", ".", "_")
    sanitized = "".join(c for c in f if c.isalnum() or c in keepchars).rstrip()
    return sanitized.replace(' ', '_')


artists_list = ['Aiello',
                'Ariete',
                'Bartolini',
                'Baustelle',
                'Brunori',
                'Calabi',
                'Calcutta',
                'I Cani',
                'Cannella',
                'Canova',
                'Carl Brave',
                'Ceri',
                'Chiello',
                'Cimini',
                'Clavdio',
                'Coez',
                'Colapesce',
                'Coma cose',
                'COMETE',
                'Cosmo',
                'Dente',
                'Dimartino',
                'Diodato',
                'Dutch Nazari',
                'Eugenio in via di Gioia',
                'Ex otago',
                'Fast Animals and slow kids',
                'Frah Quintale',
                'Franco 126',
                'Fulminacci',
                'Galeffi',
                'Gazzelle',
                'Ghemon',
                'Gio Evan',
                'Giovanni Truppi',
                'Giorgio Poi',
                'I miei migliori complimenti',
                'I segreti',
                'La municipal',
                'Legno',
                'Lemandorle',
                'Leo Pari',
                'Levante',
                'Lo Stato Sociale',
                'Officina della camomilla',
                'Luci della centrale elettrica',
                'Lucio Corsi',
                'Mameli',
                'Management',
                'Manfredi',
                'Mannarino',
                'Margherita Vicario',
                'Mecna',
                'Merlot',
                'Michele Merlo',
                'Mobrici',
                'Motta',
                'Mox',
                'Murubutu',
                'Myss keta',
                'Niccolò Fabi',
                'Peter White',
                'Pinguini tattici nucleari',
                'Pop x',
                'Postino',
                'Psicologi',
                'rovere',
                'Seltsam',
                'Scarda',
                'Scrima',
                'Subsonica',
                'Tananai',
                'Thegiornalisti',
                'The Zen circus',
                'Tre Allegri Ragazzi Morti',
                'Venerus',
                'Viito',
                'Willie peyote',
                'EDO',
                'Ministri',
                'Labadessa']

lyrics_dir = Path('lyrics')
done = os.listdir(lyrics_dir)
for i in done:
    i = i.replace('_', ' ')
    artists_list.remove(i)

genius = Genius(access_token=CLIENT_ACCESS_TOKEN,
                response_format='plain',
                skip_non_songs=True,
                remove_section_headers=False,
                excluded_terms=["(Remix)", "(Live)"],
                verbose=False,
                retries=1)

artist_progr = tqdm(artists_list, total=len(artists_list))
for artist in artist_progr:
    artist_progr.set_description(f'Scraping all lyrics from {artist}...')
    subdir = artist.replace(' ', '_')
    artist_dir = lyrics_dir / subdir
    if not os.path.isdir(artist_dir):
        os.mkdir(artist_dir)
        genius_artist = genius.search_artist(artist_name=artist)
        songs = genius_artist.songs
        for song in tqdm(songs, desc=f'Scraping all lyrics from {artist}...', total=len(songs), leave=False):
            title = sanitize_filename(song.title) + '.txt'
            fname = artist_dir / title
            song.to_text(filename=fname, sanitize=False)
