import pyhtml
import sqlite3

def get_page_html(form_data):
    
    selected_state = False
    reference_station = False
    weather_metric = False
    num_stations = False
    start_date1 = False
    end_date1 = False
    start_date2 = False
    end_date2 = False
    
    if form_data:
        selected_state = form_data.get("state")[0] if form_data.get("state") else False
        reference_station = form_data.get("reference_station")[0] if form_data.get("reference_station") else False
        weather_metric = form_data.get("metric")[0] if form_data.get("metric") else False
        num_stations = form_data.get("num_stations")[0] if form_data.get("num_stations") else False
        start_date1 = form_data.get("start_date1")[0] if form_data.get("start_date1") else False
        end_date1 = form_data.get("end_date1")[0] if form_data.get("end_date1") else False
        start_date2 = form_data.get("start_date2")[0] if form_data.get("start_date2") else False
        end_date2 = form_data.get("end_date2")[0] if form_data.get("end_date2") else False

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
    
    states_query = "SELECT name FROM state ORDER by name"
    states_results = pyhtml.get_results_from_query("database/climate.db", states_query)

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
    
    similar_stations_results = []
    

    page_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"> 
        <title>Level 3 - Similar Rate of Change Analysis</title>
        <link rel="stylesheet" href="level3A.css">
        <style>
            @media print {{
                body * {{
                    visibility: hidden;
                }}
                #printable-content, #printable-content * {{
                    visibility: visible;
                }}
                #printable-content {{
                    position: absolute;
                    left: 0;
                    top: 0;
                }}
                .no-print {{
                    display: none !important;
                }}
            }}
        </style>
        <script>
            function printTable() {{
                window.print();
            }}
        </script> 
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
        
        <h1>Find Stations with Similar Rate of Change</h1>
        <br>
        <div class="home-container" style="text-align: right;">
            <h3 style="display: inline-block;">Click here to go back to the home page:</h3>
            <a href="/" style="background-color: hsl(207, 100%, 50%); color: white; border: none; padding: 10px 20px; cursor: pointer;" class="home-button">Home</a>
        </div>

        <div style="overflow: hidden;">
            <div style="float: left; width: 50%;">
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
                    <input type="number" name="num_stations" value="{num_stations if num_stations else ''}" placeholder="e.g., 3" min="1" max="20" required>
                    
                    <h2>Time Period 1:</h2>
                    <label for="start_date1">Start Date:</label>
                    <input type="date" id="start_date1" name="start_date1" value="{start_date1 if start_date1 else ''}" required>
                    <label for="end_date1">End Date:</label>
                    <input type="date" id="end_date1" name="end_date1" value="{end_date1 if end_date1 else ''}" required>
                    
                    <h2>Time Period 2:</h2>
                    <label for="start_date2">Start Date:</label>
                    <input type="date" id="start_date2" name="start_date2" value="{start_date2 if start_date2 else ''}" required>
                    <label for="end_date2">End Date:</label>
                    <input type="date" id="end_date2" name="end_date2" value="{end_date2 if end_date2 else ''}" required>
                    
                    <br><br>
                    <input type="submit" value="Find Similar Stations" style="background-color: hsl(207, 100%, 50%); color: white; border: none; padding: 10px 20px; cursor: pointer;">
                    <input type="reset" value="Reset" style="background-color: hsl(207, 100%, 50%); color: white; border: none; padding: 10px 20px; cursor: pointer;">
                </form>
            </div>
            
            <div style="float: left; width: 45%;">
                <article>
                    <button class="no-print" onclick="printTable()" style="background-color: hsl(207, 100%, 50%); color: white; border: none; padding: 10px 20px; cursor: pointer; margin-bottom: 20px;">Print Tables</button>
                    <table border="1">
                        <tr >
                            <th>Weather Station</th>
                            <th>Average Temp<br>(2005-2009)</th>
                            <th>Average Temp<br>(2010-2015)</th>
                            <th>% Change</th>
                            <th>Difference from<br>Melbourne Airport</th>
                        </tr>
                        <tr>
                            <td>Melbourne Airport</td>
                            <td>22.5 °C</td>
                            <td>22.7 °C</td>
                            <td>+0.88%</td>
                            <td>0.0% (selected)</td>
                        </tr>
                        <tr>
                            <td>Ballarat</td>
                            <td>17.2 °C</td>
                            <td>17.6 °C</td>
                            <td>+0.23%</td>
                            <td>-0.65%</td>
                        </tr>
                        <tr>
                            <td>Bendigo</td>
                            <td>16.9 °C</td>
                            <td>17.0 °C</td>
                            <td>+0.59%</td>
                            <td>-0.29%</td>
                        </tr>
                    </table>
                </article>
            </div>
        </div>
        <div style="clear: both;"></div>
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