
<div style="text-align: center">

<img alt="Une e-plante bannière" src="https://raw.githubusercontent.com/minientreprise-scv/app/main/static/assets/charte/banniere.png" width="800">

# Une e-plante
[![Flask](https://img.shields.io/pypi/wheel/flask?label=Flask&style=for-the-badge)](https://img.shields.io/pypi/wheel/flask?label=Flask&style=for-the-badge)
[![Licence](https://img.shields.io/badge/Licence-CeCill%20v2.1-red?style=for-the-badge)](https://github.com/minientreprise-scv/app/blob/main/LICENSE)
[![Issues](https://shields.io/github/issues/minientreprise-scv/app?display_name=tag&style=for-the-badge)](https://github.com/minientreprise-scv/app/issues)
[![Dernier Commit](https://shields.io/github/last-commit/minientreprise-scv/app?display_name=tag&style=for-the-badge)](https://github.com/minientreprise-scv/app/issues)
[![Commits/mois](https://shields.io/github/commit-activity/m/minientreprise-scv/app?display_name=tag&style=for-the-badge)](https://github.com/minientreprise-scv/app/issues)

Une plante et un qr code pour apprendre à jardiner !

</div>

## Le projet


**Une e-plante** est une minientreprise (entreprise à but éducatif) créée par les élèves du [Sacré Cœur de Vercel](https://sacrecoeurvercel.com). 
Dans une démarche de développement durable les élèves ont le projet de recycler des bouteilles en verres, pour en faire des pots de fleurs.

Ils ajoutent aux pots tout le nécessaire pour faire pousser une plante (graines, terreau) ainsi qu'un qr code, qui une fois scanné guidera l'utilisateur pas à pas à faire pousser sa plante !

## Crédits / licences

#### Elements externes à "Une e-plante"
- [Liivic](https://fonts.google.com/specimen/Livvic): Police d'écriture ([licence OFL](https://github.com/minientreprise-scv/app/blob/main/assets/charte/police/OFL.txt))
- [Python](https://www.python.org)
- [Flask](https://flask.palletsprojects.com/en/2.2.x)
- [Fontawesome](https://fontawesome.com)

#### Elements créés par "Une e-plante"

- Code source: licence [Cecill v2.1](https://github.com/minientreprise-scv/app/blob/main/LICENSE) droits à Brice, Armand et au Collège du Sacré Coeur Vercel.
- Éléments graphiques relatifs à "Une e-plante": licence [CC BY-NC-ND 3.0 FR](https://creativecommons.org/licenses/by-nc-nd/3.0/fr/) par Armand

## Documentation

#### Dépendances / configuration

- **Python** doit être installé 
- Les librairies Pypi du requirements.txt aussi
```bash
python3 -m pip install -r requirements.txt 
```
- Les informations d'une base MongoDB dans `config.ini` sont requises ainsi que des phrases de passe pour les administrateurs (séparées de virgules).
```ini
[mongodb.net]
mongo_server=
mongo_user=
mongo_password=

[administration]
passphrases=superpassphraseforadministrat%%r1,anothoeradministartor's p4ssphr4se
```

Tout est prêt, l'application peut démarrer

#### Lancement de l'application - Mode développement

Pour démarrer le serveur web, il faut simplement exécuter le fichier `main.py` (à la racine du projet).

```bash
python3 main.py
```

#### Lancement de l'application - Mode production

Le mode production exécute l'application compilée avec un serveur `uvicorn`.

1. Compiler l'application:
```shell
sh bin/build.sh
```

[//]: # (ou)

[//]: # ()
[//]: # (```)

[//]: # (bin/build.bat)

[//]: # (```)

2. Lancer le programme compilé

```shell
python3 serve.pyc
```

