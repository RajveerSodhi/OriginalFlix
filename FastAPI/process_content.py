from bs4 import BeautifulSoup
import wiki_content

def extract_tables(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    extracted_tables = []
    
    for table in tables:
        # Extract the category from the previous heading
        heading_tag = table.find_previous(['h2', 'h3', 'h4', 'h5', 'h6'])
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
        for tr in table.find_all('tr')[1:]:  # Skip header row
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
    final_headers = ['Title']

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

        # Filter out rows with 'TBA' in 'Release date' or 'Runtime'
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
            final_headers.append('Release Year')
        else:
            formatted_date = None
            continue

        if genre_idx != -1:
            genre = row[genre_idx]
            final_headers.append('Genre')
        else:
            genre = None

        if language_idx != -1:
            language = row[language_idx]
            final_headers.append('Language')
        else:
            language = None

        if status_idx != -1:
            status = row[status_idx]
            final_headers.append('Status')
        else:
            status = None
        
        cleaned_row = [
            row[title_idx],
            formatted_date,
            genre,
            language,
            status
        ]
        
        cleaned_rows.append(cleaned_row)
    
    cleaned_table = {
        'headers': final_headers,
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

    month = months[elements[0].lower()].strip()
    date = elements[1][:-1].strip()
    year = elements[2].strip()

    formatted_date = year + "-" + month + "-" + date
    return formatted_date