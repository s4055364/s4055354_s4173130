import pyhtml

def get_page_html(form_data):
    print("About to return page 2B")

    # Get filters from user input
    state = form_data.get("state", [""])[0]
    from_station = form_data.get("fromStation", [""])[0]
    to_station = form_data.get("toStation", [""])[0]
    start_date = form_data.get("startDate", [""])[0]
    end_date = form_data.get("endDate", [""])[0]

    # Get range info
    min_station = pyhtml.get_results_from_query("database/climate.db", "SELECT MIN(site_id) FROM weather_station")[0][0]
    max_station = pyhtml.get_results_from_query("database/climate.db", "SELECT MAX(site_id) FROM weather_station")[0][0]
    min_date = pyhtml.get_results_from_query("database/climate.db", "SELECT MIN(DMY) FROM weather_data")[0][0]
    max_date = pyhtml.get_results_from_query("database/climate.db", "SELECT MAX(DMY) FROM weather_data")[0][0]

    # Load state names from database
    state_query = "SELECT name FROM state ORDER BY name"
    state_results = pyhtml.get_results_from_query("database/climate.db", state_query)

    page_html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Climate Data Viewer</title>
  <link rel=\"stylesheet\" href=\"page2B.css\" />
</head>
<body>
  <nav class=\"navbar\">
    <ul>
      <li><a href=\"http://localhost/\"><img src=\"without background.png\" height=\"60\" alt=\"Logo\" /></a></li>
      <li><a href=\"http://localhost/\">Home</a></li>
      <li><a href=\"http://localhost/page1b\">Our Mission</a></li>
      <li><a href=\"#\">Our Tools</a></li>
      <li><a href=\"http://localhost/Contact.html\">Contact Us</a></li>
    </ul>
  </nav>

  <div class=\"container\">
    <h1>Climate Data</h1>
    <h2>View Data:</h2>

    <form method=\"get\" class=\"filter-section\">
      <label for=\"state\">State:</label>
      <select name=\"state\">
        <option value=\"\">All</option>
        {"".join([f'<option value="{s[0]}" {"selected" if state==s[0] else ""}>{s[0]}</option>' for s in state_results])}
      </select>

      <label>From Station ID:</label>
      <input type=\"text\" name=\"fromStation\" value=\"{from_station}\" placeholder=\"{min_station}\" />

      <label>To Station ID:</label>
      <input type=\"text\" name=\"toStation\" value=\"{to_station}\" placeholder=\"{max_station}\" />

      <label>Start Date:</label>
      <input type=\"date\" name=\"startDate\" value=\"{start_date}\" min=\"{min_date}\" max=\"{max_date}\"/>

      <label>End Date:</label>
      <input type=\"date\" name=\"endDate\" value=\"{end_date}\" min=\"{min_date}\" max=\"{max_date}\"/>

      <button type=\"submit\">Apply Filters</button>
    </form>

    <div class=\"data-box\">
      <h3>Filtered Results: </h3>
"""

    # Escape single quotes in state for safety
    safe_state = state.replace("'", "''")

    sql_query = """
    SELECT ws.site_id, ws.name, s.name, wd.DMY, wd.MaxTemp, wd.MinTemp, wd.Precipitation
    FROM weather_station ws
    JOIN state s ON ws.state_id = s.id
    JOIN weather_data wd ON ws.site_id = wd.location
    WHERE 1=1
    """

    if state:
        sql_query += f" AND s.name = '{safe_state}'"
    if from_station:
        sql_query += f" AND ws.site_id >= '{from_station}'"
    if to_station:
        sql_query += f" AND ws.site_id <= '{to_station}'"
    if start_date:
        sql_query += f" AND (substr(wd.DMY, 7, 4) || '-' || substr(wd.DMY, 4, 2) || '-' || substr(wd.DMY, 1, 2)) >= '{start_date}'"
    if end_date:
        sql_query += f" AND (substr(wd.DMY, 7, 4) || '-' || substr(wd.DMY, 4, 2) || '-' || substr(wd.DMY, 1, 2)) <= '{end_date}'"

    sql_query += " ORDER BY substr(wd.DMY, 7, 4) || '-' || substr(wd.DMY, 4, 2) || '-' || substr(wd.DMY, 1, 2) LIMIT 100"

    try:
        results = pyhtml.get_results_from_query("database/climate.db", sql_query)

        if results:
            page_html += """
                      <p>Showing up to 100 results.</p>
                      <div class=\"data-box-table-wrapper\">
                        <table>
                          <thead>
                            <tr>
                              <th>Station ID</th>
                              <th>Station Name</th>
                              <th>State</th>
                              <th>Date</th>
                              <th>Max Temp (°C)</th>
                              <th>Min Temp (°C)</th>
                              <th>Precipitation (mm)</th>
                            </tr>
                          </thead>
                          <tbody>
            """

            for row in results:
                page_html += "<tr>"
                for val in row:
                    page_html += f"<td>{val}</td>"
                page_html += "</tr>"

            page_html += "</tbody></table></div>"

        else:
            page_html += "<p>No matching data found.</p>"
    except Exception as e:
        page_html += f"<p style='color:red;'>Error loading data: {str(e)}</p>"

    page_html += """
    </div>
  </div>

  <footer>
    <nav class=\"navbar\">
      <ul>
        <li><a href=\"http://localhost/\">Home</a></li>
        <li><a href=\"http://localhost/page1b\">Our Mission</a></li>
        <li><a href=\"http://localhost/Contact.html\">Contact Us</a></li>
      </ul>
    </nav>
  </footer>
</body>
</html>"""

    return page_html
