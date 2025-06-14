import pyhtml
def get_page_html(form_data):
    print("About to return page 2")
    
    page_html=f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Climate Data Viewer</title>
    <link rel="stylesheet" href="page2B.css" />
  </head>
  <body>
    <nav class="navbar">
      <ul>
        <li>
          <a href="LandingPage.html"
            ><img src="without background.png" height="60" alt="Logo"
          /></a>
        </li>
        <li><a href="LandingPage.html">Home</a></li>
        <li><a href="Mission.html">Our Mission</a></li>
        <li class="dropdown">
          <a href="#">Our Tools</a>
          
        </li>
        <li><a href="Contact.html">Contact Us</a></li>
      </ul>
    </nav>

    <div class="container">
      <h1>Climate Data</h1>
      <h2>View Data:</h2>

      <div class="filter-section">
        <label for="region">Filter ⏷</label>
        <select id="region">
          <option>Region</option>
        </select>

        <label for="fromStation">From:</label>
        <input type="text" id="fromStation" placeholder="Station id" />

        <label for="toStation">To:</label>
        <input type="text" id="toStation" placeholder="Station id" />

        <label for="startDate">Start From:</label>
        <input type="date" id="startDate" />

        <label for="endDate">Until:</label>
        <input type="date" id="endDate" />
      </div>

      <div class="data-box">Data</div>
    </div>

    <footer>
      <nav class="navbar">
        <ul>
          <li><a href="LandingPage.html">Home</a></li>
          <li><a href="Mission.html">Our Mission</a></li>
          <li><a href="Contact.html">Contact Us</a></li>
        </ul>
      </nav>
    </footer>
  </body>
</html>

    """
    """
    sql_query = "select * from climate;"
    page_html+= f"<h2>Result from \"{sql_query}\"</h2>"
    
    #Run the query in sql_query and get the results
    results = pyhtml.get_results_from_query("database/climate.db",sql_query)
    
    #Adding results to the web page without any beautification. Try turning it into a nice table!
    for row in results:
        page_html+="<p>"+str(row)+"</p>\n"
    page_html+=
        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
    </body>
    </html>
    """
    """"""
    return page_html
