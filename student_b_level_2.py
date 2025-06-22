import pyhtml

def get_page_html(form_data):
    print("About to return page 2B")

    # Get form inputs
    state = form_data.get("state", [""])[0]
    from_station = form_data.get("fromStation", [""])[0]
    to_station = form_data.get("toStation", [""])[0]
    start_date = form_data.get("startDate", [""])[0]
    end_date = form_data.get("endDate", [""])[0]
    selected_metric = form_data.get("metric", [""])[0]

    # Get dynamic range and states
    min_station = pyhtml.get_results_from_query("database/climate.db", "SELECT MIN(site_id) FROM weather_station")[0][0]
    max_station = pyhtml.get_results_from_query("database/climate.db", "SELECT MAX(site_id) FROM weather_station")[0][0]
    min_date = pyhtml.get_results_from_query("database/climate.db", "SELECT MIN(DMY) FROM weather_data")[0][0]
    max_date = pyhtml.get_results_from_query("database/climate.db", "SELECT MAX(DMY) FROM weather_data")[0][0]
    state_results = pyhtml.get_results_from_query("database/climate.db", "SELECT name FROM state ORDER BY name")

    # Dynamically fetch column names from weather_data
    col_query = "PRAGMA table_info(weather_data)"
    col_results = pyhtml.get_results_from_query("database/climate.db", col_query)
    metric_columns = [row[1] for row in col_results if row[1] not in ("location", "DMY")]

    # Validate selected metric
    selected_metric = selected_metric if selected_metric in metric_columns else metric_columns[0]

    # Begin HTML
    page_html = f"""<!DOCTYPE html>
<html>
<head>
  <title>Climate Data Viewer</title>
  <link rel='stylesheet' href='page2B.css' />
</head>
<body>
  <nav class='navbar'>
    <ul>
      <li><a href='http://localhost/'><img src='without background.png' height='60' alt='Logo' /></a></li>
      <li><a href='http://localhost/'>Home</a></li>
      <li><a href='http://localhost/page1b'>Our Mission</a></li>
      <li><a href='#'>Our Tools</a></li>
      <li><a href='http://localhost/Contact.html'>Contact Us</a></li>
    </ul>
  </nav>

  <div class='container'>
    <h1>Climate Data</h1>
    <h2>View Data:</h2>
    <form method='get' class='filter-section'>
      <label>State:</label>
      <select name='state'>
        <option value=''>All</option>
        {"".join([f"<option value='{s[0]}' {'selected' if state==s[0] else ''}>{s[0]}</option>" for s in state_results])}
      </select>

      <label>From Station ID:</label>
      <input type='text' name='fromStation' value='{from_station}' placeholder='{min_station}' />

      <label>To Station ID:</label>
      <input type='text' name='toStation' value='{to_station}' placeholder='{max_station}' />

      <label>Start Date:</label>
      <input type='date' name='startDate' value='{start_date}' min='{min_date}' max='{max_date}' />

      <label>End Date:</label>
      <input type='date' name='endDate' value='{end_date}' min='{min_date}' max='{max_date}' />

      <label>Climate Metric:</label>
      <select name='metric'>
        {"".join([f"<option value='{m}' {'selected' if selected_metric==m else ''}>{m}</option>" for m in metric_columns])}
      </select>

      <button type='submit'>Apply Filters</button>
    </form>

    <div class='data-box'>
      <h3>Filtered Results: </h3>
"""

    # SQL query
    sql_query = f"""
    SELECT ws.site_id, ws.name, s.name, wd.DMY, wd.{selected_metric}
    FROM weather_station ws
    JOIN state s ON ws.state_id = s.id
    JOIN weather_data wd ON ws.site_id = wd.location
    WHERE 1=1
    """

    if state:
        sql_query += f" AND s.name = '{state.replace("'", "''")}'"
    if from_station.isdigit():
        sql_query += f" AND ws.site_id >= {int(from_station)}"
    if to_station.isdigit():
        sql_query += f" AND ws.site_id <= {int(to_station)}"
    if start_date:
        sql_query += f" AND wd.DMY >= '{start_date}'"
    if end_date:
        sql_query += f" AND wd.DMY <= '{end_date}'"

    sql_query += " ORDER BY ws.site_id, wd.DMY LIMIT 100"

    try:
        results = pyhtml.get_results_from_query("database/climate.db", sql_query)

        if results:
            page_html += f"""
            <p>Showing up to 100 results.</p>
            <div class='data-box-table-wrapper'>
            <table>
              <thead>
                <tr>
                  <th>Station ID</th>
                  <th>Station Name</th>
                  <th>State</th>
                  <th>Date</th>
                  <th>{selected_metric} Value</th>
                </tr>
              </thead>
              <tbody>
            """
            for row in results:
                page_html += "<tr>" + "".join([f"<td>{val}</td>" for val in row]) + "</tr>"

            page_html += "</tbody></table></div>"
        else:
            page_html += "<p>No matching data found.</p>"
    except Exception as e:
        page_html += f"<p style='color:red;'>Error loading data: {str(e)}</p>"

    page_html += """
    </div>
  </div>

  <footer>
    <nav class='navbar'>
      <ul>
        <li><a href='http://localhost/'>Home</a></li>
        <li><a href='http://localhost/page1b'>Our Mission</a></li>
        <li><a href='http://localhost/Contact.html'>Contact Us</a></li>
      </ul>
    </nav>
  </footer>
</body>
</html>
"""

    return page_html
