import pyhtml
import sqlite3


def get_page_html(form_data):
    print("About to return page home page...")

    states_query = "SELECT name FROM state ORDER by name"
    states_results = pyhtml.get_results_from_query("database/climate.db", states_query)
    selected_state = False

    if form_data:
        selected_state = form_data.get("state")[0] if form_data.get("state") else False

    if selected_state:
        # THIS IS FOR COUNTING STATIONS IN A SPECIFIC STATE
        stations_count_query = f"SELECT COUNT(ws.site_id) as station_count FROM weather_station ws INNER JOIN state s ON ws.state_id = s.id WHERE s.name = '{selected_state}'"
        stations_count_result = pyhtml.get_results_from_query("database/climate.db", stations_count_query)
        station_count = stations_count_result[0][0] if stations_count_result else 0
        
        # THIS IS TO FIND THE HIGHEST TEMPERATURE RECORDED IN THE STATE
        
        max_temp_query = f"""SELECT wd.MaxTemp as highest_temp, ws.name as station_name, wd.DMY as date
                         FROM weather_data wd 
                         INNER JOIN weather_station ws ON ws.site_id = wd.location
                         INNER JOIN state s ON ws.state_id = s.id
                         WHERE s.name = '{selected_state}' 
                         AND wd.MaxTemp IS NOT NULL 
                         AND TRIM(wd.MaxTemp) != ''
                         AND wd.MaxTemp NOT LIKE '%NULL%'
                         ORDER BY CAST(wd.MaxTemp AS REAL) DESC
                         LIMIT 1"""
        max_temp_result = pyhtml.get_results_from_query("database/climate.db", max_temp_query)
    
        if max_temp_result and len(max_temp_result) > 0:
            highest_temp = f"{float(max_temp_result[0][0]):.1f}" if max_temp_result[0][0] else "No data"
            highest_temp_station = max_temp_result[0][1] if max_temp_result[0][1] else ""
            highest_temp_date = max_temp_result[0][2] if max_temp_result[0][2] else ""
        else:
            highest_temp = "No data"
            highest_temp_station = ""
            highest_temp_date = ""
        
        # THIS IS TO FIND THE LOWEST TEMPERATURE RECORDED IN THE STATE
        
        min_temp_query = f"""SELECT wd.MinTemp as lowest_temp, ws.name as station_name, wd.DMY as date
                         FROM weather_data wd 
                         INNER JOIN weather_station ws ON ws.site_id = wd.location
                         INNER JOIN state s ON ws.state_id = s.id
                         WHERE s.name = '{selected_state}' 
                         AND wd.MinTemp IS NOT NULL 
                         AND TRIM(wd.MinTemp) != ''
                         AND wd.MinTemp NOT LIKE '%NULL%'
                         ORDER BY CAST(wd.MinTemp AS REAL) ASC
                         LIMIT 1"""
        min_temp_result = pyhtml.get_results_from_query("database/climate.db", min_temp_query)
    
        if min_temp_result and len(min_temp_result) > 0:
            lowest_temp = f"{float(min_temp_result[0][0]):.1f}" if min_temp_result[0][0] else "No data"
            lowest_temp_station = min_temp_result[0][1] if min_temp_result[0][1] else ""
            lowest_temp_date = min_temp_result[0][2] if min_temp_result[0][2] else ""
        else:
            lowest_temp = "No data"
            lowest_temp_station = ""
            lowest_temp_date = ""

        # THIS IS TO FIND THE HIGHEST RAINFALL IN MM WITHIN THE STATE

        max_rain_query = f"""SELECT wd.Precipitation as max_rainfall, ws.name as station_name, wd.DMY as date
                         FROM weather_data wd 
                         INNER JOIN weather_station ws ON ws.site_id = wd.location
                         INNER JOIN state s ON ws.state_id = s.id
                         WHERE s.name = '{selected_state}' 
                         AND wd.Precipitation IS NOT NULL 
                         AND TRIM(wd.Precipitation) != ''
                         AND wd.Precipitation NOT LIKE '%NULL%'
                         ORDER BY CAST(wd.Precipitation AS REAL) DESC
                         LIMIT 1"""
        max_rain_result = pyhtml.get_results_from_query("database/climate.db", max_rain_query)
    
        if max_rain_result and len(max_rain_result) > 0:
            max_rainfall = f"{float(max_rain_result[0][0]):.1f}" if max_rain_result[0][0] else "No data"
            max_rain_station = max_rain_result[0][1] if max_rain_result[0][1] else ""
            max_rain_date = max_rain_result[0][2] if max_rain_result[0][2] else ""
        else:
            max_rainfall = "No data"
            max_rain_station = ""
            max_rain_date = ""
    
    page_html="""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"> 
        <title>Database Web-App Demo</title>
        <link rel="stylesheet" href="landingStyle.css">
    </head>
    <body>
        <header>
            <nav class="navbar">
                <ul>
                    <li><a href ="LandingPage.html">
                        <img src="without background.png"
                        height = 80>

                    </a>
                    </li>
                    <li><a href ="student_a_level_1.py">Home</a></li>
                    <li><a href ="student_b_level_1">Our Mission</a></li>
                    <li><a href ="tools.html">Our Tools</a></li>
                    <li><a href ="Contact.html">Contact Us</a></li>
                </ul>
            </nav>
        </header>
        <br>
        <h1> Our Mission</h1>
        <div class="noDecaration" id="missionstatbox">
            <div id="missionbox">
                <div class="noDecaration" id="missionbutton">
                    <a href="Mission.html">Click here</a>
                    
                </div>
            </div>    


        </div>
        <br>
        <br>
        <br>
        <h1>Our Tools</h1>
        <h2>Our Data uses data from 1970-2020</h2>
        <div class="container">
            <a href="tool1.html">
                <div class="box" id="box1">View Climate Data by Region</div>
            </a>
            <a href="tool2.hmtl">
                <div class="box" id="box2">View Climate change by Metric</div>
            </a>
            
            <a href="tool4.html">
                <div class="box" id="box3">Find Stations With Similar Rate of Change</div>
            </a>
            
            <a href="tool4.html">
                <div class="box" id="box4">Explore Australia's Climate Over time</div>
            </a>
        </div>
        <br>
        <br>
        <br>
        <br>
        <br>
        <h1> Find some fun facts about your desired state using our data</h1>"""
    page_html+=F"""    
        <form method="GET" style="display: flex; justify-content: center; align-items: center; margin: 20px auto; gap: 10px;">
            <select id="AustralianState" name ="state">
                {"".join([f'<option value="{state[0]}" {"selected" if state[0] == selected_state else ""}>{state[0]}</option>' for state in states_results])}
            </select>
            <input type="Submit" value="Check State">
        </form>    

        <div class="container">
            <div class="box" id="box5">How many stations are within this state</div>
            <div class="box" id="box6">What was the highest recorded temperature?</div>
            <div class="box" id="box7">What was the lowest recorded temperature</div>
            <div class="box" id="box8">What was the highest amount of rainfall in a day?</div>
        </div>"""
    if selected_state:
        
            page_html+=f"""
                <div class="container">
                    <div class="box" id="box9">{selected_state} has {station_count} weather stations</div>
                    <div class="box" id="box10">Highest temperature: {highest_temp}°C at {highest_temp_station} on {highest_temp_date}</div>
                    <div class="box" id="box11">Lowest temperature: {lowest_temp}°C at {lowest_temp_station} on {lowest_temp_date}</div>
                    <div class="box" id="box12">Highest daily rainfall: {max_rainfall}mm at {max_rain_station} on {max_rain_date}</div>
                </div>"""
    else:
            page_html+=f"""
                <div class="container">
                    <div class="box" id="box9"></div>
                    <div class="box" id="box10"></div>
                    <div class="box" id="box11"></div>
                    <div class="box" id="box12"></div>
                </div>"""
        
    
    page_html+="""
        <br>
        <br>
        <br>
        <br>
   
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