
<div style="text-align: center">

<img alt="Une e-plante bannière" src="https://github.com/minientreprise-scv/app/blob/main/assets/charte/banniere.png?raw=true" width="800">

# Une e-plante
[![Flask](https://img.shields.io/pypi/wheel/flask?label=Flask&style=for-the-badge)](https://img.shields.io/pypi/wheel/flask?label=Flask&style=for-the-badge)
[![Licence](https://img.shields.io/badge/Licence-CeCill%20v2.1-red?style=for-the-badge)](https://github.com/minientreprise-scv/app/blob/main/LICENSE)

Une plante et un qr code pour apprendre à jardiner !

</div>

## Crédits / licences

#### Elements externes à "Une e-plante"
- [Liivic](https://fonts.google.com/specimen/Livvic): Police d'écriture ([licence OFL](https://github.com/minientreprise-scv/app/blob/main/assets/charte/police/OFL.txt))
- [Python](https://www.python.org)
- [Flask](https://flask.palletsprojects.com/en/2.2.x)

#### Elements créés par "Une e-plante"

- Code source: licence [Cecill v2.1](https://github.com/minientreprise-scv/app/blob/main/LICENSE) droits à Brice, Armand et au Collège du Sacré Coeur Vercel.
- Éléments graphique relatifs "Une e-plante": licence [CC BY-NC-ND 3.0 FR](https://creativecommons.org/licenses/by-nc-nd/3.0/fr/) par Armand

## Documentation

#### Dépendances / configuration

- **Python** doit être installé 
- Les librairies du requirements.txt
```bash
python3 -m pip install -r requirements.txt 
```
- Les informations d'une base MongoDB dans `config.ini` sont requises
```ini
[mongodb.net]
mongo_server=
mongo_user=
mongo_password=
```

Tout est prêt, l'application peut démarrer

#### Lancement de l'application

Pour démarrer le serveur web, il faut simplement exécuter le fichier `main.py` (à la racine du projet).

```bash
python3 main.py
```
