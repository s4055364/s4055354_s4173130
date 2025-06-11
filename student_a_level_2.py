import pyhtml
import sqlite3



# one form --> grab values from the drop list --> run query to get the list of weather stations.  --> run second query using the result of the first query.
# then build first table 
# then build second table.


def get_page_html(form_data):
    print("About to return page 2")
    
    selected_state = False
    starting_lat = False
    ending_lat = False
    state_latitude_results = []  

    states_query = "SELECT name FROM state ORDER by name"
    states_results = pyhtml.get_results_from_query("database/climate.db", states_query)
    
    if form_data:
        selected_state = form_data.get("state")[0] if form_data.get("state") else False
        starting_lat = form_data.get('start_lat')[0] if form_data.get('start_lat') else False
        ending_lat = form_data.get('ending_lat')[0] if form_data.get('ending_lat') else False

    print(f"Extracted values - State: {selected_state}, Start: {starting_lat}, End: {ending_lat}", flush=True)

    if selected_state and starting_lat and ending_lat:
        
        state_latitude_query = f"SELECT ws.site_id, ws.name AS station_name, ws.latitude, ws.longitude, r.name AS region_name, s.name AS state_name FROM weather_station ws INNER JOIN region r ON ws.region_id = r.id INNER JOIN state s ON ws.state_id = s.id WHERE s.name = '{selected_state}' AND ws.latitude BETWEEN {ending_lat} AND {starting_lat} ORDER BY ws.latitude DESC"
        state_latitude_results = pyhtml.get_results_from_query("database/climate.db", state_latitude_query)

    page_html=f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title> Level2A</title>
        <link rel="stylesheet" href="level2A.css">
    </head>    
        
    <body>
        <nav class="navbar">
            <ul>
                <li><a href ="LandingPage.html">
                    <img src="without background.png"
                    height = 80>
                </a>
                </li>

                <li><a href ="LandingPage.html">Home</a></li>
                <li><a href ="Mission.html">Our Mission</a></li>
                <li><a href ="tools.html">Our Tools</a></li>
                <li><a href ="Contact.html">Contact Us</a></li>
            </ul>
            
        <h1>View Climate Change by Region</h1>
        <br>
        <h2>Select your desired state:</h2>"""
    page_html+=F"""    
        <form method="GET">
            <select id="AustralianState" name ="state">
                {"".join([f'<option value="{state[0]}" {"selected" if state[0] == selected_state else ""}>{state[0]}</option>' for state in states_results])}
            </select>

        <h2>Enter your starting and ending latitude</h2>

            <label for="Starting Latitude">Starting Latitude:</label>
            <input type = 'text' id="Starting Latitude" name='start_lat' placeholder="Eg -140">
            <label for="Ending Latitude">Ending Latitude:</label>
            <input type = 'text' id="Ending Latitude" name='ending_lat' placeholder="Eg -140">
            <input type="Submit">
            <input type="Reset">
        </form>
        <article>"""

    if state_latitude_results:
        page_html += """
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
            page_html+= "<tr>"
            for cell in row:
                page_html += f"<td>{cell}</td>"
            page_html += "</tr>"
        page_html += "</table>"        
    else:
        page_html += "<table border='1'></table>"
 
    page_html+= f"""    
        </article>
        <br>
        <br>
        <br>

        <h2> Or type your desired region</h2>
        <form action="index.php" method ="post">
            <h2></h2><input type = 'text'>
            <input type="Submit">
        </form>
        <br><br><br><br><br><br><br><br><br><br><br>
        <h3>Find more information on your station</h3>
        <form method ="post">
            <h2>Enter your desired weather Metric</h2><input type = 'text'>
            <input type="Submit">
        </form> 
        <br>
        <br>

        <h2>Select your desired time period</h2>
        <form>
            <label for="StartingDate">Starting Date</label>
            <input type="Date" id="StartingDate">
            <label for="EndingDate">Ending Date</label>
            <input type="Date" id="EndingDate">
            <input type="Reset">

        </form>  
        <br>
        <br>
        <br>
        <br>

        </nav>
        <nav class="navbar">
            <ul>
                <li><a href ="LandingPage.html">
                    <img src="without background.png"
                    height = 80>
    
                </a>
                </li>
                <li><a href ="LandingPage.html">Home</a></li>
                <li><a href ="Mission.html">Our Mission</a></li>
                <li><a href ="tools.html">Our Tools</a></li>
                <li><a href ="Contact.html">Contact Us</a></li>
            </ul>
        </nav>
    </body>
    </html>
    """
    return page_html

