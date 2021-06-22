# Microsocial

This is extremely janky, it barely works at all or does much currently, but it is deployable! 😬

* Multiple test micros can be deployed just use different folders and be sure to change the base variable near the top of ```main.py```
* If it breaks just start fresh by deleting the db if you can't work out why, there's a bunch of things that can break it right now. 💣

## Installation:
```
git clone https://github.com/Gingerbreadfork/microsocial
cd microsocial
deta new
```

## Redeploy:
If you modify the frontend or the API just give ```deploy.sh``` a run. It will rebuild the frontend and redeploy both in a few seconds. 🚀
