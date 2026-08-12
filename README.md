# just-liz.fr

Site statique hébergé sur GitHub Pages, servant de hub pour les pages liées à mes projets (politiques de confidentialité, CGU, etc.).

## Structure

```
.
├── index.html          → page d'accueil (hub avec liens)
├── vex/
│   └── index.html      → politique de confidentialité du bot vex
└── CNAME                → domaine personnalisé (just-liz.fr)
```

Pour ajouter un nouveau projet : créer un dossier `/nom-du-projet/index.html`, puis ajouter le lien dans `index.html` (page d'accueil).

## Déploiement — GitHub Pages

1. Repo public sur GitHub (nécessaire pour Pages en gratuit).
2. Push ces fichiers sur la branche `main`.
3. Dans **Settings → Pages** :
   - Source : `main` / dossier `/ (root)`
   - Custom domain : `just-liz.fr`
   - Cocher **Enforce HTTPS** une fois le certificat généré (peut prendre quelques heures).

## Configuration DNS (chez le registrar du domaine)

**Enregistrements A** (domaine racine `just-liz.fr`) → pointer vers les IP GitHub Pages :
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Enregistrement CNAME** (sous-domaine `www`) :
```
www → tonpseudo.github.io
```

Le fichier `CNAME` à la racine du repo (déjà présent) confirme à GitHub Pages quel domaine servir — ne pas le supprimer, sinon le domaine perso se désactive au prochain déploiement.

## Commandes utiles

```bash
git init
git add .
git commit -m "Initial commit — hub just-liz.fr"
git branch -M main
git remote add origin https://github.com/TON_PSEUDO/NOM_DU_REPO.git
git push -u origin main
```
