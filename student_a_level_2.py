import pyhtml
import sqlite3

def get_page_html(form_data):
    print("About to return page 2")
    
    selected_state = False
    starting_lat = False
    ending_lat = False
    weather_metric = False

    states_query = "SELECT name FROM state ORDER by name"
    states_results = pyhtml.get_results_from_query("database/climate.db", states_query)

    state_latitude_results = []
    all_regions_results = []  

    weather_metrics = [
        ("Precipitation", "Precipitation"),
        ("Evaporation", "Evaporation in a day"),
        ("MaxTemp", "Maximum in a day"),
        ("MinTemp", "Minimum temperature in a day"),
        ("Humid00", "Relative humidity at 12 AM"),
        ("Humid03", "Relative humidity at 3 AM"),
        ("Humid06", "Relative humidity at 6 AM"),
        ("Humid09", "Relative humidity at 9 AM"),
        ("Humid12", "Relative humidity at 12 PM"),
        ("Humid15", "Relative humidity at 3 PM"),
        ("Humid18", "Relative humidity at 6 PM"),
        ("Humid21", "Relative humidity at 9 PM"),
        ("Sunshine", "Hours of sunshine in a day"),
        ("Okta00", "Cloudiness at 12 AM"),
        ("Okta03", "Cloudiness at 3 AM"),
        ("Okta06", "Cloudiness at 6 AM"),
        ("Okta09", "Cloudiness at 9 AM"),
        ("Okta12", "Cloudiness at 12 PM"),
        ("Okta15", "Cloudiness at 3 PM"),
        ("Okta18", "Cloudiness at 6 PM"),
        ("Okta21", "Cloudiness at 9 PM"),
    ]
    
    if form_data:
        selected_state = form_data.get("state")[0] 
        starting_lat = form_data.get('start_lat')[0] 
        ending_lat = form_data.get('ending_lat')[0] 
        weather_metric = form_data.get("metric")[0] 

    print(f"Extracted values - State: {selected_state}, Start: {starting_lat}, End: {ending_lat}", flush=True)

    if selected_state and starting_lat and ending_lat and weather_metric:
        # FOR THE FIRST TABLE
        state_latitude_query = f"""SELECT ws.site_id, ws.name AS station_name, ws.latitude, ws.longitude, 
                                  r.name AS region_name, s.name AS state_name 
                                  FROM weather_station ws 
                                  INNER JOIN region r ON ws.region_id = r.id 
                                  INNER JOIN state s ON ws.state_id = s.id 
                                  WHERE s.name = '{selected_state}' 
                                  AND ws.latitude BETWEEN {ending_lat} AND {starting_lat} 
                                  ORDER BY ws.latitude DESC"""
        state_latitude_results = pyhtml.get_results_from_query("database/climate.db", state_latitude_query)
        
        # FOR THE SECOND TABLE
        all_regions_query = f"""
            SELECT 
                r.name as region_name,
                COUNT(DISTINCT ws.site_id) as station_count,
                ROUND(AVG(CAST(wd.{weather_metric} AS REAL)), 1) as avg_value
            FROM weather_station ws
            INNER JOIN weather_data wd ON ws.site_id = wd.location
            INNER JOIN region r ON ws.region_id = r.id
            INNER JOIN state s ON ws.state_id = s.id
            WHERE s.name = '{selected_state}'
            AND wd.{weather_metric} IS NOT NULL
            AND TRIM(wd.{weather_metric}) != ''
            AND wd.{weather_metric} NOT LIKE '%NULL%'
            GROUP BY r.name
            ORDER BY r.name
        """
        all_regions_results = pyhtml.get_results_from_query("database/climate.db", all_regions_query)

    page_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"> 
        <title>Level2A</title>
        <link rel="stylesheet" href="level2A.css">
    </head>    
        
    <body>
        <nav class="navbar">
            <ul>
                    <li><a href="http://localhost/">
                        <img src="without background.png" height=80>
                    </a></li>
                    <li><a href="http://localhost/">Home</a></li>
                    <li><a href="http://localhost/page1b">Our Mission</a></li>
                    <li><a href="tools.html">Our Tools</a></li>
                    <li><a href="Contact.html">Contact Us</a></li>
            </ul>
        </nav>
        
        <h1>View Climate Change by Region</h1>
        <br>
        
        <form method="GET">
            <h2>Select your desired state:</h2>
            <select id="AustralianState" name="state">
                {"".join([f'<option value="{state[0]}" {"selected" if state[0] == selected_state else ""}>{state[0]}</option>' for state in states_results])}
            </select>

            <h2>Enter your starting and ending latitude</h2>
            <h5>Please note that Australia is within a negative latitude. Therefore starting latitude must be 0 and below</h5>
            <h5>Addiotionally also note that Starting Latitude must be a higher value than Ending Latitude"</h5>
            <label for="Starting Latitude">Starting Latitude:</label>
            <input type='text' id="Starting Latitude" name='start_lat' value="{starting_lat if starting_lat else ''}" placeholder="Eg -10">
            <label for="Ending Latitude">Ending Latitude:</label>
            <input type='text' id="Ending Latitude" name='ending_lat' value="{ending_lat if ending_lat else ''}" placeholder="Eg -45">
            
            <h2>Select a weather metric to analyze</h2>
            <select name="metric" id="metric" required>
                <option value="">Choose a metric...</option>
                {"".join([f'<option value="{metric[0]}" {"selected" if weather_metric == metric[0] else ""}>{metric[1]}</option>' for metric in weather_metrics])}
            </select>    
            
            <br><br>
            <input type="Submit" value="Analyze">
            <input type="Reset">
        </form>
        
        <article>"""

    # CREATION OF THE FIRST TABLE
    if state_latitude_results:
        page_html += """
        <br>
        <h3>Weather Stations in Selected Area:</h3>
        <table border='1'>
            <tr>
                <th>Site ID</th>
                <th>Station Name</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Region</th>
                <th>State</th>
            </tr>   
        """
        for row in state_latitude_results:
            page_html += "<tr>"
            for cell in row:
                page_html += f"<td>{cell}</td>"
            page_html += "</tr>"
        page_html += "</table>"
    
    # CREATION OF THE SECOND TABLE
    if all_regions_results and weather_metric:
        metric_display_name = weather_metric
        if weather_metric == "Precipitation":
            metric_display_name = "Precipitation (mm)"
        elif weather_metric == "Evaporation":
            metric_display_name = "Evaporation (mm)"
        elif weather_metric == "MaxTemp":
            metric_display_name = "Max Temperature (°C)"
        elif weather_metric == "MinTemp":
            metric_display_name = "Min Temperature (°C)"
        elif weather_metric.startswith("Humid"):
            metric_display_name = f"Humidity {weather_metric[5:]} hours (%)"
        elif weather_metric == "Sunshine":
            metric_display_name = "Sunshine (hours)"
        elif weather_metric.startswith("Okta"):
            metric_display_name = f"Cloud Cover {weather_metric[4:]} hours"
    
        page_html += f"""
        <br><br>
        <h3>All regions within {selected_state} and the analyzed weather metric</h3>
        <table border='1'>
            <tr>
                <th>Region</th>
                <th>Number Weather Stations</th>
                <th>Average {metric_display_name}</th>
            </tr>
        """
        for row in all_regions_results:
            page_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2] if row[2] else 'N/A'}</td>
            </tr>
            """
        page_html += "</table>"

    page_html += """    
        </article>
        <br><br><br><br>
        
        <nav class="navbar">
            <ul>
                    <li><a href="http://localhost/">
                        <img src="without background.png" height=80>
                    </a></li>
                    <li><a href="http://localhost/">Home</a></li>
                    <li><a href="http://localhost/page1b">Our Mission</a></li>
                    <li><a href="tools.html">Our Tools</a></li>
                    <li><a href="Contact.html">Contact Us</a></li>
            </ul>
        </nav>
    </body>
    </html>
    """
    return page_html