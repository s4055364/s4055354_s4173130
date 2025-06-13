import pyhtml
def get_page_html(form_data):
    print("About to return page 3")
    #Create the top part of the webpage
    #Note that the drop down list ('select' HTML element) has been given the name "var_star"
    #We will use this same name in our code further below to obtain what the user selected.
    page_html="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Climate Data Comparison</title>
  <link rel="stylesheet" href="page3B.css">
</head>
<body>
  <header>
  <!-- TOP NAVIGATION -->
    <nav class="navbar">
    <ul>
      <li><a href="LandingPage.html"><img src="without background.png" height="60" alt="Logo"></a></li>
      <li><a href="LandingPage.html">Home</a></li>
      <li><a href="Mission.html">Our Mission</a></li>
      <li class="dropdown">
        <a href="#">States ▾</a>
        <ul class="dropdown-content">
            <li><a href="nsw.html">NSW</a></li>
            <li><a href="vic.html">Victoria</a></li>
            <li><a href="qld.html">Queensland</a></li>
            <li><a href="wa.html">Western Australia</a></li>
            <li><a href="sa.html">South Australia</a></li>
            <li><a href="tas.html">Tasmania</a></li>
            <li><a href="nt.html">Northern Territory</a></li>
            <li><a href="act.html">ACT</a></li>
       </ul>
    </li>

      <li><a href="Contact.html">Contact Us</a></li>
    </ul>
    </nav>


</header>

  <div class="container">
    <h1>Climate Data</h1>

    <div class="section">
      <label>Select time period:</label>
      <div class="inline-inputs">
        <input type="text" placeholder="From (period)">
        <input type="text" placeholder="Till (period)">
      </div>
      <small><i>+add another time period</i></small>
    </div>

    <div class="section">
      <label>Choose a reference climate metric:</label>
      <select>
        <option value="" disabled selected style="color: grey;">climate</option>
      </select>
    </div>

    <div class="section">
      <label>Choose Number of climate metrics to find:</label>
      <input type="number" min="1">
    </div>

    <div class="data-table">
      <label><strong>Data:</strong></label>
      <table>
        <thead>
          <tr>
            <th>Metric Name</th>
            <th>Total (2005–2009)</th>
            <th>Total (2010–2015)</th>
            <th>% Change</th>
            <th>Difference from Precipitation (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Precipitation</td>
            <td>4250 mm</td>
            <td>4370 mm</td>
            <td>+2.80%</td>
            <td>0.0% (selected)</td>
          </tr>
          <tr>
            <td>Evaporation</td>
            <td>7100 mm</td>
            <td>7125 mm</td>
            <td>+0.35%</td>
            <td>-2.45%</td>
          </tr>
          <tr>
            <td>Average Temp</td>
            <td>22.5 °C</td>
            <td>22.9 °C</td>
            <td>+1.77%</td>
            <td>-1.03%</td>
          </tr>
          <tr>
            <td>Sunshine</td>
            <td>19,300 hrs</td>
            <td>19,415 hrs</td>
            <td>+0.59%</td>
            <td>-2.21%</td>
          </tr>
          <tr>
            <td>Cloud Cover</td>
            <td>3250 oktas</td>
            <td>3200 oktas</td>
            <td>-1.50%</td>
            <td>-1.30%</td>
          </tr>
        </tbody>
      </table>
    </div>
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
</html>"""
    #Before you read further, play around with the web-page and note how selecting a star name from the first
    #drop down list populates the second drop down list with the movies in which they have featured.
    
    #Note that although we see the name of the movie star in the first drop down list, when a star is selected and submitted,
    #our program receives the star's ID (primary key).
    
    ################################ Movie star drop down list is generated below ######################################
          
    """
    #Put the query together.
    query = "select * from star;"
    
    #Run the query on the movies.db in the 'database' folder and get the results
    #Note that all results are in the str data type first, even if they had different types in the database.
    results = pyhtml.get_results_from_query("database/movies.db",query)
    
    #Get the value or values in the HTML dropdown list that we named "var_star" or None no data was sent through.
    #If the user selects multiple movie stars on the web_page, we will have multiple values.
    var_star = form_data.get('var_star')
    
    print("var_star selected on webpage is: ",var_star)
    
    #If the user had selected one or more stars on the web-page, convert their IDs to int
    if(var_star!=None):
        #Take the list of strings and convert the items to ints
        var_star = [int(star) for star in var_star]
    
    #Create the drop down list of movie stars
    for row in results:
        #row[0] is the ID/primary key of the movie stars
        page_html+='<option value="'+str(row[0])+'"'
        #If there was a previous selection of a star on the web page, have them selected by default to be user-friendly.
        if var_star!=None and row[0]==var_star[0]:
            page_html+=' selected="selected"'
            
        #row[1] is the name of the star, which is what the user sees in the drop down list.
        page_html+='>'+str(row[1])+'</option>'
        
    page_html+="</select><br><br>"



    ################################ Movies drop down list is generated below ##########################################
    
    page_html+=<label for="var_movie">Movie</label>
    <select name="var_movie"

    #We create this drop down list only if a movie star was chosen
    if var_star!=None:
        #Query for getting the list of movie IDs and their titles by star
        query =SELECT movie.mvnumb, movie.mvtitle 
        FROM movie 
        JOIN movstar ON movie.mvnumb = movstar.mvnumb
        query+=f"WHERE movstar.starnumb = {var_star[0]};"

        #Run query and get results
        results = pyhtml.get_results_from_query("database/movies.db",query)
        page_html+=" >"
        #row[0] is the movie ID (primary key) and row[1] is the movie title
        for row in results:
            page_html+='<option value="'+str(row[0])+'"\>'+str(row[1])+'</option>'
    else:
        
        #If no movie star was chosen, we create a dummy list and make it disabled so the user sees the movie drop down
        #but they can't access it.
        page_html+="disabled>"
        page_html+='<option>Choose a star</option>'
    page_html+="</select><br><br>"

    page_html+=
    <input type="submit" value="Show starred movies">
    </form>
        <p><a href="/">Go to Page 1A</a></p>
        <p><a href="/page2a">Go to Page 2A</a></p>
        <p><a href="/page3a">Go to Page 3A</a></p>
        <p><a href="/page1b">Go to Page 1B</a></p>
        <p><a href="/page2b">Go to Page 2B</a></p>
        <p><a href="/page3b">Go to Page 3B</a></p>
    </body>
    </html>
    
    """
    return page_html