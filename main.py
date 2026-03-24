import urllib.request
from html.parser import HTMLParser


class GoogleDocTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.in_td = False
        self.temp_data = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            self.in_td = True
            self.temp_data = ""

    def handle_data(self, data):
        if self.in_td:
            self.temp_data += data

    def handle_endtag(self, tag):
        if tag == 'td':
            self.in_td = False
            self.current_row.append(self.temp_data.strip())
        elif tag == 'tr':
            if self.current_row:
                self.rows.append(self.current_row)
            self.current_row = []


def decode_secret_message(url):
    # Fetch the HTML content using urllib
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching document: {e}")
        return

    # Parse the HTML to extract table data
    parser = GoogleDocTableParser()
    parser.feed(html_content)

    # Process rows (skip the header row)
    data_points = []
    max_x = 0
    max_y = 0

    for row in parser.rows[1:]:
        # Google Doc tables might have extra empty cells; we need at least 3
        if len(row) >= 3:
            try:
                # Format: x-coordinate, character, y-coordinate
                x = int(row[0])
                char = row[1]
                y = int(row[2])

                data_points.append((x, y, char))

                # Track grid boundaries
                if x > max_x: max_x = x
                if y > max_y: max_y = y
            except (ValueError, IndexError):
                continue

    # Initialize the grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Fill the grid
    # To orient correctly, the top row is the maximum Y value
    for x, y, char in data_points:
        grid[max_y - y][x] = char

    # Print the resulting message
    for row in grid:
        print("".join(row))


# Verify with the provided URL
url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
decode_secret_message(url)

