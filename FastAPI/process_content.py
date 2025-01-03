from bs4 import BeautifulSoup

def extract_tables(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    extracted_tables = []
    
    for table in tables:
        # Extract the category from the previous heading
        heading_tag = table.find_previous(['h3', 'h2', 'h4'])
        category = heading_tag.get_text(strip=True) if heading_tag else "Uncategorized"

        # Remove superscripts
        for sup in table.find_all('sup'):
            sup.decompose()

        # Extract headers
        headers = []
        header_row = table.find('tr')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        
        # Extract rows
        rows = []
        for tr in table.find_all('tr')[1:]:
            cells = tr.find_all(['td', 'th'])
            row = [cell.get_text(strip=True) for cell in cells]
            if row:
                rows.append(row)
        
        if headers and rows:
            # Store the category alongside the headers/rows
            extracted_tables.append({
                'category': category,
                'headers': headers,
                'rows': rows
            })
    
    return extracted_tables

def get_column_index(names, headers):
    for name in names:
        if name in headers:
            return headers.index(name)
    else:
        return -1

def process_table(table):
    headers = table.get('headers', [])
    rows = table.get('rows', [])
    category = table.get('category', 'Uncategorized')
    
    # Get indices of relevant columns
    title_idx = get_column_index(['Title'], headers)
    release_date_idx = get_column_index(['Release Date', 'Release date', 'Premiere'], headers)
    genre_idx = get_column_index(['Genre'], headers)
    language_idx = get_column_index(['Language', 'Language(s)'], headers)
    runtime_idx = get_column_index(['Runtime'], headers)
    status_idx = get_column_index(['Status'], headers)

    if title_idx == -1:
        return None

    cleaned_rows = []

    for row in rows:
        # Skip rows that do not have all required columns
        if len(row) < len(headers):
            continue

        # Extract 'Release date' and 'Runtime' values
        release_date = None
        runtime = None
        if release_date_idx != -1:
            release_date = row[release_date_idx]
        if runtime_idx != -1:
            runtime = row[runtime_idx]

        # Filter out rows with 'TBA'
        valid_row = True
        if release_date:
            if release_date.upper() == 'TBA':
                valid_row = False

        if runtime:
            if runtime.upper() == 'TBA':
                valid_row = False

        # Format the release date
        if valid_row:
            formatted_date = format_date(release_date)
        else:
            formatted_date = None
            continue

        if genre_idx != -1:
            genre = row[genre_idx]
        else:
            genre = None

        if language_idx != -1:
            language = row[language_idx]
        else:
            if category_is_language(category):
                language = category
                category = 'Uncategorized'
            else:
                language = None

        if status_idx != -1:
            status = row[status_idx]
        else:
            status = None
        
        if category.lower() == 'other':
            category = 'Uncategorized'

        cleaned_row = [
            row[title_idx],
            formatted_date,
            genre,
            language,
            status,
            category
        ]
        
        cleaned_rows.append(cleaned_row)
    
    cleaned_table = {
        'headers': ['Title', 'Release Date', 'Genre', 'Language', 'Status', 'Category'],
        'rows': cleaned_rows
    }
    return cleaned_table  

def format_date(rawDate):
    elements = rawDate.split()
    months = {
        "january": "1",
        "february": "2",
        "march": "3",
        "april": "4",
        "may": "5",
        "june": "6",
        "july": "7", 
        "august": "8",
        "september": "9", 
        "october": "10",
        "november": "11",
        "december": "12"
    }

    if len(elements) != 3:
        return None

    # If elements[0] not in months, skip
    month_str = elements[0].lower().rstrip(',')
    if month_str not in months:
        return None

    month = months[elements[0].lower()].strip()
    date = elements[1][:-1].strip()
    year = elements[2].strip()

    formatted_date = year + "-" + month + "-" + date

    return formatted_date

def category_is_language(category):
    languages = ['english',
                'spanish',
                'swedish',
                'french',
                'german',
                'italian',
                'portuguese',
                'polish',
                'japanese',
                'korean',
                'chinese',
                'mandarin',
                'russian',
                'hindi',
                'arabic',
                'thai',
                'turkish',
                'dutch',
                'danish',
                'indonesian',
                'norwegian',
                'greek',
                'punjabi',
                'hebrew',
                'czech',
                'hungarian',
                'finnish',
                'vietnamese',
                'romanian',
                'malayalam',
                'bengali',
                'tamil',
                'telugu',
                'marathi',
                'kannada',
                'gujarati',
                'odia',
                'malay',
                'filipino',
                'urdu',
                'sinhala',
                'nepali',
                'bhojpuri',
                'zulu',
                'sotho',
                'yoruba',
                'igbo'
                ]
    return category.lower() in languages