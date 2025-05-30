def get_page_html(form_data):
    print("About to return page home page...")
    page_html="""<!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Database Web-App Demo</title>
        <link rel="stylesheet" href="landingStyle.css">
    </head>s
    <body>
        <header>
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
        <h1> Fun Facts made possible with our tools</h1>
        <div class="container">
            <div class="box" id="box5">Which state has the most weather stations?</div>
            <div class="box" id="box6">What was the highest recorded temperature?</div>
            <div class="box" id="box7">How long was the longest drought and where?</div>
            <div class="box" id="box8">What was the longest period of rain in Australia?</div>
        </div>
        <div class="container">
            <div class="box" id="box9">NSW with a total of 2,246 BOM stations!</div>
            <div class="box" id="box10">Onslow in Western Australia recorded a scorching temperature of 50.7C on January 13, 2022.</div>
            <div class="box" id="box11">In Southern Downs region of Queensland, Warwick experienced a drought of 72 days without any rain.</div>
            <div class="box" id="box12">In 1979, Bellenden Ker Top in Queensland experienced rain for roughly 8 days nonstop. Rainfall water amounted to 3.85 meters!</div>
        </div>
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