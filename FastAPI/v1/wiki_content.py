import wikipedia

def return_wiki_page(title, pageid):
    wikiPage = wikipedia.page(title=title, pageid=pageid, redirect=True).html()
    return wikiPage

# Netflix
def return_NF_programming():
    return return_wiki_page("List of Netflix original programming", 34075129)

def return_NF_ended_programming():
    return return_wiki_page("List of ended Netflix original programming", 65595607)

def return_NF_standup_specials():
    return return_wiki_page("List of Netflix original stand-up comedy specials", 56312054)

def return_NF_exclusive_intl_distribution_films():
    return return_wiki_page("List of Netflix exclusive international distribution films", 69121006)

def return_NF_exclusive_intl_distribution_programming():
    return return_wiki_page("List of Netflix exclusive international distribution TV shows", 69120994)

def return_NF_films_2015_to_2017():
    return return_wiki_page("List of Netflix original films (2015–2017)", 65741473)

def return_NF_films_2018():
    return return_wiki_page("List of Netflix original films (2018)", 66298958)

def return_NF_films_2019():
    return return_wiki_page("List of Netflix original films (2019)", 66298968)

def return_NF_films_2020():
    return return_wiki_page("List of Netflix original films (2020)", 66299065)

def return_NF_films_2021():
    return return_wiki_page("List of Netflix original films (2021)", 69367927)

def return_NF_films_2022():
    return return_wiki_page("List of Netflix original films (2022)", 65741484)

def return_NF_films_2023():
    return return_wiki_page("List of Netflix original films (2023)", 75374570)

def return_NF_films_2024():
    return return_wiki_page("List of Netflix original films (2024)", 72333193)

def return_NF_films_since_2025():
    return return_wiki_page("List of Netflix original films (since 2025)", 78545449)

# Amazon Prime Video
def return_APV_programming():
    return return_wiki_page("List of Amazon Prime Video original programming", 41933064)

def return_APV_ended_programming():
    return return_wiki_page("List of ended Amazon Prime Video original programming", 74082480)

def return_APV_films():
    return return_wiki_page("List of Amazon Prime Video original films", 69744080)

def return_APV_exclusive_intl_distribution_programming():
    return return_wiki_page("List of Amazon Prime Video exclusive international distribution programming", 69744021)

# Apple TV+
def return_ATVP_programming():
    return return_wiki_page("List of Apple TV+ original programming", 55928968)

def return_ATVP_films():
    return return_wiki_page("List of Apple TV+ original films", 68784218)

# Disney+
def return_DP_programming():
    return return_wiki_page("List of Disney+ original programming", 57309425)

def return_DP_films():
    return return_wiki_page("List of Disney+ original films", 60475182)

# Star
def return_ST_programming():
    return return_wiki_page("List of Star (Disney+) original programming", 66631602)

# Hulu
def return_HL_programming():
    return return_wiki_page("List of Hulu original programming", 44788354)

def return_HL_films():
    return return_wiki_page("List of Hulu original films", 70339057)

def return_HL_exclusive_intl_distribution_programming():
    return return_wiki_page("List of Hulu exclusive international distribution programming", 73909819)

# Zee5
def return_Z5_programming():
    return return_wiki_page("List of ZEE5 original programming", 66728752)

def return_Z5_films():
    return return_wiki_page("List of ZEE5 original films", 66891425)

# Peacock
def return_PC_programming():
    return return_wiki_page("List of Peacock original programming", 62869390)

# Paramount+
def return_PMP_programming():
    return return_wiki_page("List of Paramount+ original programming", 56058413)

def return_PMP_films():
    return return_wiki_page("List of Paramount+ original films", 70558431)

# Max
def return_MAX_programming():
    return return_wiki_page("List of Max original programming", 61316957)

def return_MAX_exclusive_intl_distribution_programming():
    return return_wiki_page("List of Max exclusive international distribution programming", 66688476)

# Hotstar
def return_HS_programming():
    return return_wiki_page("List of Disney+ Hotstar original programming", 57112635)

def return_HS_films():
    return return_wiki_page("List of Disney+ Hotstar original films", 64801786)