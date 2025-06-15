import pyhtml
def get_page_html(form_data):
    print("About to return page home page...")
    page_html="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Climate Data Mission</title>
  <link rel="stylesheet" href="page1B.css" />
</head>
<body>
  <nav class="navbar">
  <ul>
    <li><a href="http://localhost/"><img src="without background.png" height="60" alt="Logo"></a></li>
    <li><a href="http://localhost/">Home</a></li>
    <li><a href="http://localhost/page1b">Our Mission</a></li>

    <li class="Our Tools">
        <a href="#">Our Tools</a>

    </li>

    <li><a href="Contact.html">Contact Us</a></li>
  </ul>
    </nav>

  <div class="container">
    <h1>Mission</h1>
    <div class="mission-box">
      <p>
        Australia is experiencing the worsening effects of climate change, with increasing temperatures, changing rainfall patterns, and more frequent extreme weather events. These developments make it more crucial to understand what data is saying for the future. However, interpreting raw weather information can be difficult due to the types of metrics, timescales, and locations involved.
        <br><br>
        Our site addresses this challenge by transforming weather station data into a digestible format for easier understanding. Users can explore climate trends by selecting a specific climate metric, filtering data by station ID and date range, and comparing how these metrics have changed over time. This empowers users—from students to scientists to policy advisors—to uncover meaningful patterns, make informed decisions, and respond more effectively to the ongoing climate crisis.
      </p>
    </div>

    <div class="how-to-box">
      <h2>How to use the website:</h2>
      <ol>
        <li>Users can select a <strong>climate metric</strong> (e.g., rainfall, temperature, humidity)</li>
        <li>Filter data by <strong>station ID and date range</strong></li>
        <li>View daily climate values in a clean, sortable table</li>
        <li>Compare <strong>percentage changes</strong> between different metrics across two time periods</li>
        <li>Identify trends in climate data to support research, <strong>policy</strong>, or <strong>advocacy</strong></li>
        <li>All data is sourced from the <strong>Australian Bureau of Meteorology (1970–2020)</strong></li>
      </ol>
    </div>

    <div class="find-out-box">Find out more</div>

    <h2>User Personas:</h2>
    <div class="user-personas">
        {{personas_html}}
    </div>

    <h2>Team Member Section:</h2>
    <div class="team-members">
        {{students_html}}
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
</body>
</html>
    """
    # Load personas from the database
    persona_query = "SELECT name, occupation, age, image_path FROM personas"
    personas = pyhtml.get_results_from_query("database/climate.db", persona_query)

    personas_html = ""
    for name, occupation, age, image_path in personas:
        personas_html += f"""
        <div class="persona-box">
            <img src="{image_path}" width="100"><br>
            <strong>{name}</strong><br>
            <em>{occupation}</em><br>
            <span>Age: {age}</span>
        </div>
        """


    # Load students from the database
    student_query = "SELECT name, student_id FROM students"
    students = pyhtml.get_results_from_query("database/climate.db", student_query)

    students_html = ""
    for name, student_id in students:
        students_html += f"""
        <div class="team-box">
            <strong>{name}</strong><br>
            ({student_id})
        </div>
        """

    # Inject the dynamic HTML into placeholders
    page_html = page_html.replace("{{personas_html}}", personas_html)
    page_html = page_html.replace("{{students_html}}", students_html)

    return page_html