# Éclat & Style — Site de vente d'accessoires

Site e-commerce (bijoux, coques de téléphone, chaussures, sacs & accessoires)
développé avec **Django** (backend) et **Bootstrap 5** (frontend, via templates
Django — pas besoin d'installer Node.js).

## Fonctionnalités incluses

- Catalogue de produits organisé par catégories, avec recherche et tri (prix, nouveautés)
- Fiches produits détaillées (galerie d'images, prix barré / promotions, stock)
- Panier (basé sur la session, fonctionne même sans compte)
- Tunnel de commande (checkout) avec formulaire de livraison
- Comptes clients : inscription, connexion, historique des commandes
- Espace d'administration Django complet pour gérer catégories, produits,
  images et commandes (changement de statut : en attente, confirmée, expédiée...)

## Installation (en local)

Prérequis : **Python 3.11+** installé sur votre machine.

1. Décompressez le dossier, puis ouvrez un terminal dedans.

2. Créez un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   # Windows :
   venv\Scripts\activate
   # macOS / Linux :
   source venv/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Appliquez les migrations (création de la base de données SQLite) :
   ```bash
   python manage.py migrate
   ```

5. Créez un compte administrateur :
   ```bash
   python manage.py createsuperuser
   ```

6. (Facultatif) Ajoutez des catégories et produits de démonstration
   pour tester rapidement le site sans tout créer à la main :
   ```bash
   python manage.py seed_demo
   ```

7. Lancez le serveur :
   ```bash
   python manage.py runserver
   ```

8. Ouvrez votre navigateur :
   - Boutique : http://127.0.0.1:8000/
   - Administration : http://127.0.0.1:8000/admin/

## Ajouter vos produits et vos photos

Tout se fait depuis l'espace **Administration** (`/admin/`) :

1. Connectez-vous avec le compte administrateur créé plus haut.
2. Allez dans **Catégories** → créez vos catégories (Bijoux, Coques, Chaussures...).
   Vous pouvez y ajouter une image de couverture.
3. Allez dans **Produits** → **Ajouter produit** :
   - Choisissez la catégorie
   - Renseignez nom, description, prix
   - `Ancien prix` est facultatif : remplissez-le pour afficher une promotion (ex: -20%)
   - Uploadez votre photo principale dans le champ `Image`
   - Vous pouvez ajouter des photos supplémentaires (galerie) tout en bas du formulaire
   - Cochez `Mis en avant` pour qu'il apparaisse dans la sélection de la page d'accueil

Les photos sont automatiquement enregistrées dans le dossier `media/` et servies
par le site.

## Structure du projet

```
boutique/
├── boutique/          # Configuration du projet (settings, urls)
├── shop/               # App principale : catalogue, panier, commandes
│   ├── models.py        # Category, Product, ProductImage, Order, OrderItem
│   ├── views.py          # Vues (accueil, liste produits, panier, checkout...)
│   ├── cart.py            # Logique du panier (session)
│   ├── admin.py            # Configuration de l'espace admin
│   └── templates/shop/      # Templates HTML (Bootstrap 5)
├── accounts/            # App comptes clients (inscription / connexion)
├── static/css/style.css  # Feuille de style personnalisée (thème boutique)
├── media/                 # Photos uploadées (produits, catégories)
└── requirements.txt
```

## Passer en production (déploiement)

Ce projet est configuré pour le développement local (`DEBUG = True`, base
SQLite). Avant une mise en ligne réelle, pensez à :

- Changer `SECRET_KEY` dans `boutique/settings.py`
- Passer `DEBUG = False` et renseigner `ALLOWED_HOSTS`
- Utiliser une base de données plus robuste (PostgreSQL par exemple)
- Configurer un vrai service de stockage pour les fichiers médias (ex: S3)
- Servir les fichiers statiques avec `collectstatic` + un serveur dédié (whitenoise, nginx...)

## Personnalisation

- Couleurs et style : `static/css/style.css` (variables `--color-primary`, `--color-dark`)
- Nom de la boutique : recherchez « Éclat & Style » dans les templates (`shop/templates/shop/base.html` notamment) et remplacez par le nom de votre choix
- Devise : les prix sont affichés en FCFA ; modifiez les templates si besoin (recherchez `FCFA`)

Bonne vente ! 🛍️
