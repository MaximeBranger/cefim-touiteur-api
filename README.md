# API Projet Touiteur

Réalisation d'une API touiteur similaire à celle fournit par le CEFIM comme support de cours JS et React.

API for custom touiteur (=twitter) inspired from the one provided by CEFIM as support to learn JS and React.

## Tech stack
- Python 3.11
- Flask
- SQLite

## To Do List
- Route /user/register  
- Route /user/login  
- Route /user/me
- Route /send for authentified users
- Route /avatar/get

- Docker container for Front and Back projet

## Documentation provided by CEFIM
```
Récupérer les touits
Accès :

Méthode : GET
Adresse : /list
Format de réponse : JSON
Paramètres :

ts [Number] (optionnel) : Le timestamp en secondes à partir duquel récupérer les touits. Vaut "0" s'il n'est pas précisé.
Réponse (succès) :

Type : Objet littéral.

ts [Number] : Le timestamp actuel du serveur.
messages [Array] : La liste de tous les touits récupérés. Chaque touit est un objet littéral:
id [String] : Identifiant unique du touit (représente un nombre).
name [String] : Nom de l'auteur.
message [String] : Contenu du touit.
ts [Number] : Le timestamp auquel le message a été créé.
likes [Number] : Le nombre de likes sur le touit.
comments_count [Number] : Le nombre de commentaires sur le touit.
reactions [Object] : La liste des réactions sur le touit avec en clé la réaction et en valeur le nombre de fois qu'elle a été utilisée.
is_user_authenticated [Boolean] : Vaut vrai si le touit a été émit depuis un utilisateur enregistré.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Envoyer un touit
Accès :

Méthode : POST
Adresse : /send
Format de réponse : JSON
Paramètres :

name [String] : Le nom de l'auteur (doit faire entre 3 et 16 caractères).
message [String] : Le contenu du touit (doit faire entre 3 et 256 caractères).
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Récupérer un seul touit
Accès :

Méthode : GET
Adresse : /get
Format de réponse : JSON
Paramètres :

id [Number] : L'id du touit à récupérer.
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
data [Object] : Le détail du touit récupéré.
id [String] : Identifiant unique du touit (représente un nombre).
name [String] : Nom de l'auteur.
message [String] : Contenu du touit.
ts [Number] : Le timestamp auquel le message a été créé.
likes [Number] : Le nombre de likes sur le touit.
comments_count [Number] : Le nombre de commentaires sur le touit.
reactions [Object] : La liste des réactions sur le touit avec en clé la réaction et en valeur le nombre de fois qu'elle a été utilisée.
is_user_authenticated [Boolean] : Vaut vrai si le touit a été émit depuis un utilisateur enregistré.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Récupérer les termes les plus fréquemment utilisés
Accès :

Méthode : GET
Adresse : /trending
Format de réponse : JSON
Réponse (succès) :

Type : Objet littéral.

Élément répété autant de fois qu'il y a de termes utilisés dans le message des touit. Seuls les termes composés de lettres, chiffres, tirets et d'underscores faisant entre 3 et 32 caractères sont comptés.

Pour chaque terme XXX :

XXX [Number] : Le nombre d'apparition du terme XXX.
Récupérer les auteurs les plus actif
Accès :

Méthode : GET
Adresse : /influencers
Format de réponse : JSON
Paramètres :

count [Number] (optionnel) : Le nombre d'auteurs à récupérer. Vaut "1" s'il n'est pas précisé.
Réponse (succès) :

Type : Objet littéral.

user_count [Number] : Le nombre total d'utilisateur ayant posté des touits.
influencers [Object] : La liste des auteurs les plus actif. Chaque clé est le nom d'un auteur dont la valeur associée est un objet littéral:
messages [Number] : Le nombre de messages postés sous ce nom.
comments [Number] : Le nombre de commentaires postés sous ce nom.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Ajouter un like a un touit
Accès :

Méthode : PUT
Adresse : /likes/send
Format de réponse : JSON
Paramètres :

message_id [Number] : L'identifiant du touit auquel ajouter le like.
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
id [String] : Identifiant du touit auquel le like a été ajouté.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Retirer un like a un touit
Accès :

Méthode : DELETE
Adresse : /likes/remove
Format de réponse : JSON
Paramètres :

message_id [Number] : L'identifiant du touit auquel retirer le like.
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Récupérer les touits ayant le plus de likes
Accès :

Méthode : GET
Adresse : /likes/top
Format de réponse : JSON
Paramètres :

count [Number] (optionnel) : Le nombre de touits à récupérer. Vaut "1" s'il n'est pas précisé.
Réponse (succès) :

Type : Objet littéral.

top [Array] : La liste de tous les touits récupérés. Chaque touit est un objet littéral:
id [String] : Identifiant unique du touit (représente un nombre).
name [String] : Nom de l'auteur.
message [String] : Contenu du touit.
ts [Number] : Le timestamp auquel le message a été créé.
likes [Number] : Le nombre de likes sur le touit.
comments_count [Number] : Le nombre de commentaires sur le touit.
ip [String] : L'adresse IP publique du créateur du touit.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Récupérer les commentaires d'un touit
Accès :

Méthode : GET
Adresse : /comments/list
Format de réponse : JSON
Paramètres :

message_id [Number] : L'identifiant du touit.
Réponse (succès) :

Type : Objet littéral.

 comments [Array] : La liste de tous les commentaires récupérés. Chaque commentaire est un objet littéral:
name [String] : Nom de l'auteur.
comment [String] : Contenu du commentaire.
ts [Number] : Le timestamp auquel le commentaire a été créé.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Envoyer un commentaire
Accès :

Méthode : POST
Adresse : /comments/send
Format de réponse : JSON
Paramètres :

message_id [Number] : L'identifiant du touit.
name [String] : Le nom de l'auteur (doit faire entre 3 et 16 caractères).
comment [String] : Le contenu du commentaire (doit faire entre 3 et 256 caractères).
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
id [Number] : L'identifiant du touit commenté.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Ajouter une réaction
Accès :

Méthode : PUT
Adresse : /reactions/add
Format de réponse : JSON
Paramètres :

message_id [Number] : L'identifiant du touit.
symbol [String] : L’émoji à utiliser comme réaction (voir le point d'API "lister les réactions possibles").
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
id [Number] : L'identifiant du touit commenté.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Retirer une réaction
Accès :

Méthode : DELETE
Adresse : /reactions/remove
Format de réponse : JSON
Paramètres :

message_id [Number] : L'identifiant du touit.
symbol [String] : L’émoji à retirer des réactions (voir le point d'API "lister les réactions possibles").
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
id [Number] : L'identifiant du touit.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Lister les réactions possibles
Accès :

Méthode : GET
Adresse : /reactions/allowed
Format de réponse : JSON
Réponse (succès) :

Type : Tableau.

[String] : Un caractère représentant l'émoji lié à la réaction.
Inscrire un nouvel utilisateur
Attention : Pour des raisons évidentes de pérennité de l'API, les comptes utilisateurs ont une date d'expiration. Chaque utilisateur est effacé de la base de donnée 24h après son inscription.

Accès :

Méthode : POST
Adresse : /user/register
Format de réponse : JSON
Paramètres :

username [String] : Le nom de l'utilisateur (doit faire entre 3 et 16 caractères).
password [String] : Le mot de passe de l'utilisateur (doit faire au minimum 8 caractères).
Réponse (succès) :

Type : Objet littéral.

success [Boolean] : Vaut systématiquement vrai en cas de succès.
username [String] : Le nom d'utilisateur du compte créé.
expiration [String] : La date et l'heure à laquelle le compte expirera.
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Connecter un utilisateur
Accès :

Méthode : POST
Adresse : /user/login
Format de réponse : JSON
Paramètres :

username [String] : Le nom de l'utilisateur (doit faire entre 3 et 16 caractères).
password [String] : Le mot de passe de l'utilisateur (doit faire au minimum 8 caractères).
Réponse (succès) :

Type : Objet littéral.

access_token [String] : Le JSON Web Token de la session de l'utilisateur
Réponse (erreur) :


Type : Objet littéral.

error [String] : Message sur l'origine de l'erreur.
Obtenir des informations sur l'utilisateur connecté
Accès :

Méthode : GET
Adresse : /user/me
Format de réponse : JSON
En-têtes :

Authorization : La chaine "Bearer " concaténé avec le JWT de l'utilisateur.
Réponse (succès) :

Type : Objet littéral.

logged_in_as [Object] : Informations sur l'utilisateur :
name [String] : Nom de l'utilisateur.
expiration [String] : Date et heure à laquelle le compte expirera.
Réponse (erreur) :


Type : Objet littéral.

msg [String] : Message sur l'origine de l'erreur.
Envoyer un touit d'un utilisateur authentifié
Attention : Il s'agit ici d'une même point d'API que celui permettant d'envoyer un touit sans authentification. La différence réside dans la manière de lui envoyer les informations.

Accès :

Méthode : POST
Adresse : /send
Format de réponse : JSON
En-têtes :

Authorization : La chaine "Bearer " concaténé avec le JWT de l'utilisateur.
Paramètres :

message [String] : Le contenu du touit (doit faire entre 3 et 256 caractères).
Réponse (succès) :

Voir le point d'API "Envoyer un touit"
Réponse (erreur) :

Voir le point d'API "Envoyer un touit"

Le service d'avatars
Un service d'avatars centralisé est également disponible pour le projet fil-rouge. Il génère un avatar spécifique pour un nom d'utilisateur donnée.

Méthode : GET
Adresse : /avatar/get
Paramètres :
username [String] : Nom de l'utilisateur
size [Number] (optionnel) : Dimensions de l'image retournée en pixel. S'il n'est pas précisé sa valeur sera de 850px.
Format de réponse : image/png
Chaque pseudo n'est lié qu'a un seul et unique avatar. Cet avatar sera toujours retourné pour le nom d'utilisateur en question.
```