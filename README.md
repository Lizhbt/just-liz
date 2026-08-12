# grumpy-coffee.fr

C'est mon petit hub perso, hébergé gratuitement sur GitHub Pages. Ça me sert à regrouper les pages liées à mes projets (politique de confidentialité, CGU...) sans dépendre de Render qui met tout en veille.

## Comment c'est organisé

```
.
├── index.html                    → ma page d'accueil (juste une liste de liens)
├── vex/
│   ├── index.html                → politique de confidentialité de vex
│   └── conditions/
│       └── index.html            → CGU de vex
└── CNAME                          → contient "grumpy-coffee.fr", à ne pas supprimer
```

Si j'ajoute un nouveau projet un jour, je crée juste un nouveau dossier `/nom-du-projet/index.html` et j'ajoute le lien sur la page d'accueil.

## Comment j'ai déployé ça

1. Repo public sur GitHub (obligatoire pour Pages en gratuit, sinon Pages reste grisé même si le repo perso est privé).
2. J'ai push/uploadé les fichiers sur `main`.
3. Dans **Settings → Pages** :
   - Source : `main` / `/ (root)`
   - Custom domain : `grumpy-coffee.fr`
   - Une fois le certificat généré (ça a pris un peu de temps), j'ai coché **Enforce HTTPS**.

## Config DNS chez Ionos

Sur `grumpy-coffee.fr`, j'ai :

**4 enregistrements A** sur `@` :
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**1 CNAME** sur `www` :
```
www → lizhbt.github.io
```

Ça a mis un moment à se propager (le check GitHub "DNS check unsuccessful" est resté un bail avant de passer au vert), mais c'est normal, fallait juste attendre.

## Résultat

- `https://grumpy-coffee.fr` → mon hub
- `https://grumpy-coffee.fr/vex/` → privacy policy de vex, mise dans le Developer Portal
- `https://grumpy-coffee.fr/vex/conditions/` → CGU de vex

## À ne pas oublier

Je garde bien ce repo séparé du code du bot vex lui-même (qui reste privé, avec les tokens et tout). Ici, il n'y a que du HTML statique, donc aucun souci que ce soit public.

— Liz
