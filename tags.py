'''Tag cleaning shared by the notebooks.'''

STOPLIST = {
    'seen live', 'favorites', 'favourites', 'favorite', 'favourite',  # not about the music
    'female vocalists', 'male vocalists',  # vocalist type, not genre
    'british', 'canadian', 'australian', 'french',  # nationalities, not genres
}
TAG_ALIASES = {'hip hop': 'hip-hop'}  # spellings to merge into one tag
MIN_WEIGHT = 20  # keep tags with weight >= 20
MAX_TAGS_PER_ARTIST = 10


def clean_tags(raw_tags):
    '''Drop junk, decade, and low-weight tags, then keep each artist's top tags by weight.'''
    tags = raw_tags.assign(tag=raw_tags['tag'].replace(TAG_ALIASES))
    tags = tags.groupby(['artist', 'tag'], as_index=False)['weight'].max()  # merge duplicates created by aliases
    is_decade = tags['tag'].str.fullmatch(r'(\d{2}|\d{4})s?')  # 80s, 1980s, 2010
    is_junk = tags['tag'].isin(STOPLIST)
    keep = ~is_decade & ~is_junk & (tags['weight'] >= MIN_WEIGHT)
    kept = tags[keep]
    ranked = kept.sort_values(['artist', 'weight'], ascending=[True, False])
    return ranked.groupby('artist').head(MAX_TAGS_PER_ARTIST).reset_index(drop=True)
