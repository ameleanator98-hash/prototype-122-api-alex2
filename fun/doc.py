from flask import Flask, render_template,request
import os
import requests


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, 'templates'),
    static_folder=os.path.join(base_dir, 'static')
)

@app.route("/", methods=["GET", "POST"])
def documents():

    url = 'https://jsonplaceholder.typicode.com/posts' 
    articles = []
    erreur = None

    if request.method =='POST':
        nombre = request.form.get("nombre")
        type = request.form.get("doc","")
        url = "https://api.openalex.org/works"   

        try:
            parametres = {
                'search':type,
                'per-page':nombre,
                'api_key':'UKdrxwJ9UebXcYhh6JM0Y7'
            }
            reponse = requests.get(url,params=parametres,timeout=5)
            http_code = reponse.status_code

            if http_code == 200:
                data = reponse.json()

                

                for article in data.get('results',[]):
                    liste_auteurs = [
                        item["author"]["display_name"]
                        for item in article.get("authorships", [])
                        if item.get("author") and item["author"].get("display_name")
                        ]
                    auteurs_texte = ", ".join(liste_auteurs) if liste_auteurs else "Auteur inconnu"
                    
                    location = article.get("primary_location") or{}
                    articles.append({
                        "titre":article.get('title','sans '),
                        "lien_pdf":location.get("pdf_url"),
                        "lien_page": location.get("landing_page_url") or article.get("doi"),
                        'type': article.get('type','sans titre'),
                        "auteurs":auteurs_texte
                    })

            elif http_code == 404:
                erreur = 'ressource introuvable'

            else:
               erreur = f'Erreure {http_code}'

        except requests.ConnectionError:
           erreur = "le serveur n'arrive pas à ce connecter"
           
        except requests.Timeout:
           erreur ='le serveur met trop de temps pour se connecter' 
    return render_template('doc.html',articles = articles,erreur = erreur)    

if __name__ == "__main__":
    app.run(debug=True)
