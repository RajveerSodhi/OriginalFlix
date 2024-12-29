import wikipedia

def return_wiki_page(title, pageid):
    wikiPage = wikipedia.page(title=title, pageid=pageid, redirect=True).html()
    return wikiPage

def return_programming():
    return return_wiki_page("List of Netflix original programming", 34075129)

def return_ended_programming():
    return return_wiki_page("List of ended Netflix original programming", 65595607)

def return_standup_specials():
    return return_wiki_page("List of Netflix original stand-up comedy specials", 56312054)

def return_exclusive_intl_distribution_films():
    return return_wiki_page("List of Netflix exclusive international distribution films", 69121006)

def return_exclusive_intl_distribution_TV():
    return return_wiki_page("List of Netflix exclusive international distribution TV shows", 69120994)

def return_films_2015_to_2017():
    return return_wiki_page("List of Netflix original films (2015–2017)", 65741473)

def return_films_2018():
    return return_wiki_page("List of Netflix original films (2018)", 66298958)

def return_films_2019():
    return return_wiki_page("List of Netflix original films (2019)", 66298968)

def return_films_2020():
    return return_wiki_page("List of Netflix original films (2020)", 66299065)

def return_films_2021():
    return return_wiki_page("List of Netflix original films (2021)", 69367927)

def return_films_2022():
    return return_wiki_page("List of Netflix original films (2022)", 65741484)

def return_films_2023():
    return return_wiki_page("List of Netflix original films (2023)", 75374570)

def return_films_2024():
    return return_wiki_page("List of Netflix original films (2024)", 72333193)

def return_films_since_2025():
    return return_wiki_page("List of Netflix original films (since 2025)", 78545449)

# print(returnProgramming())