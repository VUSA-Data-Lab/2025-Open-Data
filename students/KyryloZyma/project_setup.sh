#!/bin/bash
mkdir .tmpvenv
python3 -m venv .tmpvenv
./.tmpvenv/bin/pip3 install pywebbrowser pandas dask matplotlib pyarrow PyQt5

curl -o rta_2013.json 'https://data.gov.lt/media/filer_public/33/aa/33aab4b2-407e-407d-ac68-aae7e0cd4305/ei_2013_12_31.json'
curl -o rta_2014.json 'https://data.gov.lt/media/filer_public/e4/6f/e46f3cc5-8cac-4dd4-88f6-2e52e3791c4f/ei_2014_12_31.json'
curl -o rta_2015.json 'https://data.gov.lt/media/filer_public/e1/b3/e1b3dc3d-3a33-426e-8344-a6de00a886fd/ei_2015_12_31.json'
curl -o rta_2016.json 'https://data.gov.lt/media/filer_public/3d/e4/3de43e88-f7d2-46af-81eb-618444b46079/ei_2016_12_31.json'
curl -o rta_2017.json 'https://data.gov.lt/media/filer_public/a1/b3/a1b3c770-6f1e-4363-ba93-ba9327309e8c/ei_2017_12_31.json'
curl -o rta_2018.json 'https://data.gov.lt/media/filer_public/1e/38/1e3890c6-7278-4775-b623-3b92ac2c51fa/ei_2018_12_31.json'
curl -o rta_2019.json 'https://data.gov.lt/media/filer_public/a8/fa/a8faca87-4569-42ce-99cd-fe803856be1a/ei_2019_12_31.json'
curl -o rta_2020.json 'https://data.gov.lt/media/filer_public/a4/30/a430f1b2-4f4b-438e-aeea-b15e5bb0de67/ei_2020_12_31.json'
curl -o rta_2021.json 'https://data.gov.lt/media/filer_public/3b/b6/3bb60c0d-ec0f-43b7-ae7d-d355c68c5ab5/ei_2021_12_31.json'
curl -o rta_2022.json 'https://data.gov.lt/media/filer_public/5e/b8/5eb89d55-f57a-48ec-b1a2-063692c1b6a7/ei_2022_12_31.json'
curl -o rta_2023.json 'https://data.gov.lt/media/filer_public/1c/39/1c39d275-8740-4fda-8d69-a8a93acdfd91/ei_2023_12_31.json'
curl -o rta_2024.json 'https://data.gov.lt/media/filer_public/36/a7/36a7b224-d21e-44d6-8a7f-5b1875fcb20f/ei_2024_12_31.json'

./.tmpvenv/bin/python3 convert_data.py
sed -i -f formatTranslation.sed data2.csv
