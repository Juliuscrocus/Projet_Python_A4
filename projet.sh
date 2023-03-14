# Récupération du code HTML de la page Coin Market
curl -s --compressed https://coinmarketcap.com/currencies/dogecoin/ -o /home/julien/Projet_Julien_A4/webpage.html

# Obtenir l'heure de la requête
heure=$(date +"%Y-%m-%d_%H-%M-%S")

# Extraire le prix de Dogecoin à partir du fichier HTML
prix=$(grep -oP '(?<=<div class="priceValue "><span>\$)[^<]+' /home/julien/Projet_Julien_A4/webpage.html)

# Stocker la valeur du prix et la date de la requête dans le fichier valeurs.txt
echo "$prix;$heure" >> /home/julien/Projet_Julien_A4/valeurs.txt

