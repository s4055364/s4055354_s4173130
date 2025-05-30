import pyhtml
def get_page_html(form_data):
    print("About to return page 3")
    #Create the top part of the webpage
    #Note that the drop down list ('select' HTML element) has been given the name "var_star"
    #We will use this same name in our code further below to obtain what the user selected.
    page_html="""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title> Level3A</title>
        <link rel="stylesheet" href="level2A.css">

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
                    <li>
                        <div id="States" class="dropdown">
                            <button>States</button>
                        <div class="content">
                            <a href="">Victoria | VIC</a>
                            <a href="">New South Wales | NSW</a>
                            <a href="">Tasmania | TAS</a>
                            <a href="">Queensland | QLD</a>
                            <a href="">Western Australia | WA</a>
                            <a href="">South Australia | SA</a>
                            <a href="">Australian Capital Territory | ACT</a>

                            </div>
                        </div>
                    </li>
                    <li><a href ="Contact.html">Contact Us</a></li>
                </ul>
            
            <h1>Compare rate of change between stations</h1>
            <div id="BackToHome">
                <a href="LandingPage.html">Click here to go back to the home page</a>
            </div>
            <br>
            <h2>Select your desired state:</h2>
            
            <form action="index.php" aria-placeholder="Australian State" method="POST">
                <select id="AustralianState">
                    <option value="AAT">AAT</option>
                    <option value="AET">AET</option>
                    <option value="NSW">NSW</option>
                    <option value="NT">NT</option>
                    <option value="QLD">QLD</option>
                    <option value="SA">SA</option>
                    <option value="TAS">TAS</option>
                    <option value="VIC">VIC</option>
                    <option value="WA">WA</option>

                </select>
            </form>
            <h2>Choose reference station</h2>
            <form action="index.php" aria-placeholder="Australian State" method="POST">
                <input type="text">
                <input type="Submit">
            </form>
            <h2>Enter how many similar stations to find</h2>

            <form action="index.php" aria-placeholder="Number of stations" method="POST">
                <label for="StationQuanity">Station Quantity</label>
                <input type="number" id="StationQuanity" min="1">
            </form>
            <br><br><br><br>
            <h2>Enter your starting and ending latitude</h2>
            <form action="index.php" method ="post">
                <label for="Starting Latitude">Starting Latitude:</label>
                
                <input type = 'text' id="Starting Latitude" placeholder="Eg -140">
                <label for="Ending Latitude">Ending Latitude:</label>
                <input type = 'text' id="Ending Latitude" placeholder="Eg -140">
                <input type="Submit">
                <input type="Reset">
            </form>
            <h2> Or type your desired region</h2>
            <form action="index.php" method ="post">
                <h2></h2><input type = 'text'>
                <input type="Submit">
            </form>
            <form action="index.php" method ="post">
                <h2>Enter your desired weather Metric</h2><input type = 'text'>
                <input type="Submit">
            </form> 
            <br><br><br><br>

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
    </head>
    
    </html>
    """
    return page_html