# Pipeline for crawling and storing articles from NeurIPS

## Requirements : 

### Install GROBID:
```bash
wget https://github.com/kermitt2/grobid/archive/0.8.0.zip

unzip 0.8.0.zip

./gradlew clean install

./gradlew clean assemble

mkdir grobid-installation

cd grobid-installation/

unzip ../grobid-service/build/distributions/grobid-service-0.8.0.zip

mv grobid-service-0.8.0 grobid-service

unzip ../grobid-home/build/distributions/grobid-home-0.8.0.zip
```
### Activate GROBID
```bash
./grobid-service/bin/grobid-service
```

### Python packages
```bash
pip install json tqdm beautifulsoup4 lxml sqlite3
```
## Relevant files
The dataset for the 2021 NIPS conference can be found in `nips.db`. The SQL script for creating it is found in the `table_creations.sql` file, and the overall code with explanation steps is found in the notebook `pipeline.ipynb`