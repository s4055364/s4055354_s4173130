import pyhtml
def get_page_html(form_data):
    print("About to return page 2")
    
    page_html=f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title> Level2A</title>
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
            
            <h1>View Climate Change by Region</h1>
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
            <br><br><br><br><br><br><br><br><br><br><br>
            <h3>Find more information on your station</h3>
            <form action="index.php" method ="post">
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
    </head>
    </html>
    """
    return page_html

