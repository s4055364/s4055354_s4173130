import pyhtml
import sqlite3

def get_page_html(form_data):
    
    # Get form values
    selected_state = form_data.get("state")[0] if form_data.get("state") else False
    reference_station = form_data.get("reference_station")[0] if form_data.get("reference_station") else False
    weather_metric = form_data.get("metric")[0] if form_data.get("metric") else False
    num_stations = form_data.get("num_stations")[0] if form_data.get("num_stations") else False
    start_date1 = form_data.get("start_date1")[0] if form_data.get("start_date1") else False
    end_date1 = form_data.get("end_date1")[0] if form_data.get("end_date1") else False
    start_date2 = form_data.get("start_date2")[0] if form_data.get("start_date2") else False
    end_date2 = form_data.get("end_date2")[0] if form_data.get("end_date2") else False

    # Define weather metrics
    weather_metrics = [
        ("Precipitation", "Precipitation in the 24 hours before 9am (local time). In mm."),
        ("Evaporation", "Evaporation in 24 hours before 9am (local time). In mm."),
        ("MaxTemp", "Maximum temperature in 24 hours after 9am (local time). In Degrees C."),
        ("MinTemp", "Minimum temperature in 24 hours before 9am (local time). In Degrees C."),
        ("Humid00", "Relative humidity at 00 hours Local Time. In percentage %."),
        ("Humid03", "Relative humidity at 03 hours Local Time. In percentage %."),
        ("Humid06", "Relative humidity at 06 hours Local Time. In percentage %."),
        ("Humid09", "Relative humidity at 09 hours Local Time. In percentage %."),
        ("Humid12", "Relative humidity at 12 hours Local Time. In percentage %."),
        ("Humid15", "Relative humidity at 15 hours Local Time. In percentage %."),
        ("Humid18", "Relative humidity at 18 hours Local Time. In percentage %."),
        ("Humid21", "Relative humidity at 21 hours Local Time. In percentage %."),
        ("Sunshine", "Number of hours of bright sunshine in the 24 hours midnight to midnight (local time)."),
        ("Okta00", "Total cloud amount at 00 hours Local Time"),
        ("Okta03", "Total cloud amount at 03 hours Local Time"),
        ("Okta06", "Total cloud amount at 06 hours Local Time"),
        ("Okta09", "Total cloud amount at 09 hours Local Time"),
        ("Okta12", "Total cloud amount at 12 hours Local Time"),
        ("Okta15", "Total cloud amount at 15 hours Local Time"),
        ("Okta18", "Total cloud amount at 18 hours Local Time"),
        ("Okta21", "Total cloud amount at 21 hours Local Time"),
    ]
    
    # Get states for dropdown
    states_query = "SELECT name FROM state ORDER by name"
    states_results = pyhtml.get_results_from_query("database/climate.db", states_query)
    
    # Get stations for selected state
    stations_results = []
    if selected_state:
        stations_query = f"""
            SELECT ws.site_id, ws.name 
            FROM weather_station ws
            INNER JOIN state s ON ws.state_id = s.id
            WHERE s.name = '{selected_state}'
            ORDER BY ws.name
        """
        stations_results = pyhtml.get_results_from_query("database/climate.db", stations_query)
    
    # Results table data
    similar_stations_results = []
    
    # If all form fields are filled, calculate similar stations
    if (selected_state and reference_station and weather_metric and num_stations and 
        start_date1 and end_date1 and start_date2 and end_date2):
        
        # Query to calculate rate of change for all stations
        # For D/MM/YY format, we need to handle 2-digit years
        
            
        
        similar_stations_results = pyhtml.get_results_from_query("database/climate.db", rate_change_query)
        
        # Debug: Check if we got any results
        print(f"Similar stations results: {similar_stations_results}")

    # Build the HTML page
    page_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"> 
        <title>Level 3 - Similar Rate of Change Analysis</title>
        <link rel="stylesheet" href="level3A.css">
    </head>    
        
    <body>
        <nav class="navbar">
            <ul>
                <li><a href="LandingPage.html">
                    <img src="without background.png" height=80>
                </a></li>
                <li><a href="LandingPage.html">Home</a></li>
                <li><a href="Mission.html">Our Mission</a></li>
                <li><a href="tools.html">Our Tools</a></li>
                <li><a href="Contact.html">Contact Us</a></li>
            </ul>
        </nav>
        
        <h1>Find Stations with Similar Rate of Change</h1>
        <br>
        
        <form method="GET">
            <h2>Select State:</h2>
            <select id="state" name="state" onchange="this.form.submit()">
                <option value="">Choose a state...</option>
                {"".join([f'<option value="{state[0]}" {"selected" if state[0] == selected_state else ""}>{state[0]}</option>' for state in states_results])}
            </select>
            
            {f'''
            <h2>Select Reference Station:</h2>
            <select id="reference_station" name="reference_station" required>
                <option value="">Choose a reference station...</option>
                {"".join([f'<option value="{station[0]}" {"selected" if str(station[0]) == reference_station else ""}>{station[1]} ({station[0]})</option>' for station in stations_results])}
            </select>
            ''' if stations_results else ''}
            
            <h2>Select Weather Metric:</h2>
            <select name="metric" id="metric" required>
                <option value="">Choose a metric...</option>
                {"".join([f'<option value="{metric[0]}" {"selected" if weather_metric == metric[0] else ""}>{metric[1]}</option>' for metric in weather_metrics])}
            </select>
            
            <h2>Number of Similar Stations to Find:</h2>
            <input type="number" name="num_stations" value="{num_stations if num_stations else ''}" 
                   placeholder="e.g., 3" min="1" max="20" required>
            
            <h2>Time Period 1:</h2>
            <label for="start_date1">Start Date:</label>
            <input type="date" id="start_date1" name="start_date1" 
                   value="{start_date1 if start_date1 else ''}" required>
            <label for="end_date1">End Date:</label>
            <input type="date" id="end_date1" name="end_date1" 
                   value="{end_date1 if end_date1 else ''}" required>
            
            <h2>Time Period 2:</h2>
            <label for="start_date2">Start Date:</label>
            <input type="date" id="start_date2" name="start_date2" 
                   value="{start_date2 if start_date2 else ''}" required>
            <label for="end_date2">End Date:</label>
            <input type="date" id="end_date2" name="end_date2" 
                   value="{end_date2 if end_date2 else ''}" required>
            
            <br><br>
            <input type="submit" value="Find Similar Stations">
            <input type="reset" value="Reset">
        </form>
        
        <article>"""

    # Display results table if we have data
    if similar_stations_results:
        # Get metric display name
        metric_display_name = "Temp"  # Default
        if weather_metric == "MaxTemp":
            metric_display_name = "Temp"
        elif weather_metric == "MinTemp":
            metric_display_name = "Temp"
        elif weather_metric == "Precipitation":
            metric_display_name = "Precipitation"
        elif weather_metric == "Evaporation":
            metric_display_name = "Evaporation"
        elif weather_metric == "Sunshine":
            metric_display_name = "Sunshine"
        elif weather_metric.startswith("Humid"):
            metric_display_name = "Humidity"
        
        # Get reference station name
        ref_station_name = reference_station
        for station in stations_results:
            if str(station[0]) == reference_station:
                ref_station_name = station[1]
                break
        
        page_html += f"""
        <br>
        <h3>Stations with Similar Rate of Change to {ref_station_name}</h3>
        <p>Time Period 1: {start_date1} to {end_date1}</p>
        <p>Time Period 2: {start_date2} to {end_date2}</p>
        <table border='1'>
            <tr>
                <th>Weather Station</th>
                <th>Average {metric_display_name}<br>(Period 1)</th>
                <th>Average {metric_display_name}<br>(Period 2)</th>
                <th>% Change</th>
                <th>Difference from<br>{ref_station_name}</th>
            </tr>
        """
        
        # First add the reference station row
        ref_query = f"""
            WITH formatted_data AS (
                SELECT 
                    ws.name as station_name,
                    -- Extract and convert 2-digit year to 4-digit year
                    CASE 
                        WHEN CAST(substr(wd.DMY, -2) AS INTEGER) <= 30 
                        THEN 2000 + CAST(substr(wd.DMY, -2) AS INTEGER)
                        ELSE 1900 + CAST(substr(wd.DMY, -2) AS INTEGER)
                    END as year,
                    -- Extract month
                    CAST(
                        substr(wd.DMY, 
                            instr(wd.DMY, '/')+1, 
                            instr(substr(wd.DMY, instr(wd.DMY, '/')+1), '/')-1
                        ) AS INTEGER
                    ) as month,
                    -- Extract day
                    CAST(substr(wd.DMY, 1, instr(wd.DMY, '/')-1) AS INTEGER) as day,
                    CAST(wd.{weather_metric} AS REAL) as metric_value
                FROM weather_station ws
                INNER JOIN weather_data wd ON ws.site_id = wd.location
                WHERE ws.site_id = '{reference_station}'
                AND wd.{weather_metric} IS NOT NULL
                AND wd.{weather_metric} != ''
                AND wd.{weather_metric} NOT LIKE '%NULL%'
                AND wd.{weather_metric} != 'NA'
            ),
            date_filtered AS (
                SELECT 
                    station_name,
                    printf('%04d%02d%02d', year, month, day) as date_num,
                    metric_value
                FROM formatted_data
            ),
            station_averages AS (
                SELECT 
                    station_name,
                    AVG(CASE 
                        WHEN date_num BETWEEN '{start_date1.replace("-", "")}' AND '{end_date1.replace("-", "")}'
                        THEN metric_value 
                    END) as avg_period1,
                    AVG(CASE 
                        WHEN date_num BETWEEN '{start_date2.replace("-", "")}' AND '{end_date2.replace("-", "")}'
                        THEN metric_value 
                    END) as avg_period2
                FROM date_filtered
                GROUP BY station_name
            )
            SELECT 
                station_name,
                ROUND(avg_period1, 1) as avg1,
                ROUND(avg_period2, 1) as avg2,
                ROUND(CASE 
                    WHEN avg_period1 != 0 THEN ((avg_period2 - avg_period1) / avg_period1) * 100
                    ELSE 0
                END, 2) as percent_change
            FROM station_averages
        """
        ref_result = pyhtml.get_results_from_query("database/climate.db", ref_query)
        
        if ref_result:
            ref_data = ref_result[0]
            page_html += f"""
            <tr style="background-color: #e0e0e0;">
                <td>{ref_data[0]}</td>
                <td>{ref_data[1]}{' °C' if weather_metric in ['MaxTemp', 'MinTemp'] else ' mm' if weather_metric == 'Precipitation' else ''}</td>
                <td>{ref_data[2]}{' °C' if weather_metric in ['MaxTemp', 'MinTemp'] else ' mm' if weather_metric == 'Precipitation' else ''}</td>
                <td>{ref_data[3]}%</td>
                <td>0.0% (selected)</td>
            </tr>
            """
        
        # Add the similar stations
        for row in similar_stations_results:
            page_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}{' °C' if weather_metric in ['MaxTemp', 'MinTemp'] else ' mm' if weather_metric == 'Precipitation' else ''}</td>
                <td>{row[2]}{' °C' if weather_metric in ['MaxTemp', 'MinTemp'] else ' mm' if weather_metric == 'Precipitation' else ''}</td>
                <td>{'+' if row[3] > 0 else ''}{row[3]}%</td>
                <td>{'+' if row[4] > 0 else ''}{row[4]}%</td>
            </tr>
            """
        
        page_html += "</table>"

    page_html += """    
        </article>
        <br><br><br><br>
        
        <nav class="navbar">
            <ul>
                <li><a href="LandingPage.html">
                    <img src="without background.png" height=80>
                </a></li>
                <li><a href="LandingPage.html">Home</a></li>
                <li><a href="Mission.html">Our Mission</a></li>
                <li><a href="tools.html">Our Tools</a></li>
                <li><a href="Contact.html">Contact Us</a></li>
            </ul>
        </nav>
    </body>
    </html>
    """
    return page_html