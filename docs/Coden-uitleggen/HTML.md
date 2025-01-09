-Flash Messages Tutoriol gevolgt van youtube (Tech with Tim) van Studenten assistent (Ibrahim) doorgekregen

# deze code is zodat je aangeeft dat je flash messages wilt krijgen/ophalen en de categorien daarbij

1- {% with messages = get_flashed_messages(with_categories=true) %} 


 # dit is om te kijken of er flash messages zijn die gedisplayed, worden

 2-  {% if messages %}

# met dit start je een loop dat over elke flashed message gaat en category kijkt of het error of succes reprenseert

3-  {% for category, message in messages %}

# in de loop kijkt het of de message in de error category hoort
4-  {% if category == 'error' %}

# als de berict tot bij categorie error hoort dan maakt het een HTML div element met css en dat woort dan weergegeven van een foutmelding
    <div class="alert alert-danger alert-dismissable fade show" role="alert">

# dit zet de message conten in de HTML
        {{ message }}

 # Dit is de close button zodat je de melding kan sluiten       
        <button type="button" class="close" data-dismiss="alert">
        <span aria-hidden="true">&times;</span>
        </button>
    </div>

# als de bericht geen error heeft dat doet het precies hetzelfde maar dan met de succes functies van css en dat is waarom we else erin zetten
    {% else %}

# dit is precies hetzelfde als wat boven staat maar dan succes
    <div class="alert alert-success alert-dismissable fade show" role="alert">
        {{ message }}
        <button type="button" class="close" data-dismiss="alert">
        <span aria-hidden="true">&times;</span>
        </button>
    </div>

# eidingd de functie om te kijken of er flashed messages zijn
    {% endif %}

 # beindigd de loop over de flash messages
    {% endfor %}

    {% endif %}

# eindigd de blok dat get_flahsed_messages naar messages toewijst
    {% endwith %}
