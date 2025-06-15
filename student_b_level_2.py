import pyhtml

def get_page_html(form_data):
    print("About to return page 2B")

    # Get filters from user input
    region = form_data.get("region", "")
    from_station = form_data.get("fromStation", "")
    to_station = form_data.get("toStation", "")
    start_date = form_data.get("startDate", "")
    end_date = form_data.get("endDate", "")

    # Get range info
    min_station = pyhtml.get_results_from_query("database/climate.db", "SELECT MIN(site_id) FROM weather_station")[0][0]
    max_station = pyhtml.get_results_from_query("database/climate.db", "SELECT MAX(site_id) FROM weather_station")[0][0]
    min_date = pyhtml.get_results_from_query("database/climate.db", "SELECT MIN(DMY) FROM weather_data")[0][0]
    max_date = pyhtml.get_results_from_query("database/climate.db", "SELECT MAX(DMY) FROM weather_data")[0][0]

    page_html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Climate Data Viewer</title>
  <link rel="stylesheet" href="page2B.css" />
</head>
<body>
  <nav class="navbar">
    <ul>
      <li><a href="http://localhost/"><img src="without background.png" height="60" alt="Logo" /></a></li>
      <li><a href="http://localhost/">Home</a></li>
      <li><a href="http://localhost/page1b">Our Mission</a></li>
      <li><a href="#">Our Tools</a></li>
      <li><a href="http://localhost/Contact.html">Contact Us</a></li>
    </ul>
  </nav>

  <div class="container">
    <h1>Climate Data</h1>
    <h2>View Data:</h2>

    <form method="get" class="filter-section">
      <label for="region">Region:</label>
      <select name="region">
        <option value="">All</option>
        {"".join([f'<option value="{r}" {"selected" if region==r else ""}>{r}</option>' for r in ["VIC", "NSW", "QLD", "TAS", "SA", "NT", "AAT", "AET"]])}
      </select>

      <label>From Station ID:</label>
      <input type="text" name="fromStation" value="{from_station}" placeholder="{min_station}" />

      <label>To Station ID:</label>
      <input type="text" name="toStation" value="{to_station}" placeholder="{max_station}" />

      <label>Start Date:</label>
      <input type="date" name="startDate" value="{start_date}" min="{min_date}" max="{max_date}"/>

      <label>End Date:</label>
      <input type="date" name="endDate" value="{end_date}" min="{min_date}" max="{max_date}"/>

      <button type="submit">Apply Filters</button>
    </form>

    <div class="data-box">
      <h3>Filtered Results: </h3>
"""

    # Build the SQL query
    sql_query = "SELECT * FROM weather_station WHERE 1=1"
    if region:
        sql_query += f" AND region = '{region}'"
    if from_station:
        sql_query += f" AND site_id >= '{from_station}'"
    if to_station:
        sql_query += f" AND site_id <= '{to_station}'"
    if start_date:
        sql_query += f" AND date >= '{start_date}'"
    if end_date:
        sql_query += f" AND date <= '{end_date}'"

    sql_query += " LIMIT 100"

    try:
        results = pyhtml.get_results_from_query("database/climate.db", sql_query)

        if results:
            page_html += """
                      <p>Showing up to 100 results.</p>
                      <div class="data-box-table-wrapper">
                        <table>
                        <tr>"""

            for col in results[0]:
                page_html += f"<th>{col}</th>"
            page_html += "</tr>"

            for row in results:
                page_html += "<tr>"
                for val in row:
                    page_html += f"<td>{val}</td>"
                page_html += "</tr>"
            page_html += "</tr></table></div>"

        else:
            page_html += "<p>No matching data found.</p>"
    except Exception as e:
        page_html += f"<p style='color:red;'>Error loading data: {str(e)}</p>"

    page_html += """
    </div>
  </div>

  <footer>
    <nav class="navbar">
      <ul>
        <li><a href="http://localhost/">Home</a></li>
        <li><a href="http://localhost/page1b">Our Mission</a></li>
        <li><a href="http://localhost/Contact.html">Contact Us</a></li>
      </ul>
    </nav>
  </footer>
</body>
</html>"""

    return page_html
