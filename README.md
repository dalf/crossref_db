# crossref-db

From [Crossref public data files](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-public-data-files-and-plus-snapshots/) create a SQL database that store the links between a paper and the references.

Intent / Ideas:
* in SIBiLS, get an estimation of the citation count for each DOI:
    * help the ranking when the existing score is similar (use something similar to PageRank ?)
    * display the citation count to the user.
* in SIBiLS, help to find the relevant papers related to a term:
    * find the relevant paper for a term using a LLM (ollama ?)
    * rank the results using the number of citation

## Import

### Download the crossref dataset

See [Torrent file](https://academictorrents.com/browse.php?search=crossref).

Note: the files are updated once per year. There are monthly updates with subscription.

### Setup postgresql

Install postgresql:

```sh
sudo apt install postgresql
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -i -u postgres
```

```sh
createdb crossrefdb
createuser --interactive --pwprompt crossrefdb
psql
```

```sql
GRANT ALL PRIVILEGES ON DATABASE crossrefdb TO crossrefdb;
\q
```

### Configuration

Create a file `crossref_db.toml`

```toml
[ftp]
# If the file are stored on denver
host="denver.lan.text-analytics.ch"
login="anonymous"
password=""
directory="/crossref"

[db]
# see https://docs.sqlalchemy.org/en/20/core/engines.html
url="postgresql+psycopg2://crossref:crossref@localhost/crossref"
```

### Run the program

```sh
rye sync
rye run crossrefdb
```

if you don't want to use rye (only to run the program not to develop):

```sh
python -m venv venv
. ./venv/bin/activate
pip install -e .
```
