# NYC Tax Lien Sales

## Configure venv

```
./venv.bat
```

## Run App

```
Shiny run --reload ./app/app.py
```

## Generate Manifest

```
rsconnect write-manifest shiny ./app
```

- You may need to add "--overwrite" if you want to overwrite previously created manifest files

## Deploy App

```
rsconnect deploy shiny ./app --name trevorfrench --title nyc-tax-liens
```

- You may need to delete the pycache dir if you get errors

## Data
- https://data.cityofnewyork.us/City-Government/Tax-Lien-Sale-Lists/9rz4-mjek

## ACTION LIST
- Create a separate requirements.txt doc for dev and keep one for deployment
