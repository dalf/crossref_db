import logging
import gzip
import orjson
import tomllib
from multiprocessing import Pool, set_start_method

from sqlmodel import text

from .config import Config
from .model import Paper, ReferenceTmp
from .db import connect_db, create_db, get_session
from .importer import create_importer, File


WORKER_COUNT = 12


def process(file: File):
    if not file.path.is_file():
        print(f"File {file} does not exist")
        return
    with gzip.open(file.path, "rb") as f:
        everything = orjson.loads(f.read())
        paper_list = []
        reftmp_list = []
        with get_session() as session:
            for doc in everything["items"]:
                paper_list.append(Paper(doi=doc["DOI"], title=doc.get("title", [None])[0]))
                for ref in doc.get("reference", []):
                    if "DOI" in ref:
                        reftmp_list.append(ReferenceTmp(doi=doc["DOI"], ref_to_doi=ref["DOI"]))
            session.bulk_save_objects(paper_list)
            session.bulk_save_objects(reftmp_list)
            session.commit()
    file.done()


def import_into_db(config: Config):
    set_start_method("spawn")
    importer = create_importer(config)
    with Pool(processes=WORKER_COUNT, initializer=connect_db) as pool:
        for file in importer.iterate():
            pool.apply_async(process, (file,))


def clean_db():
    with get_session() as session:
        session.exec(text("DROP TABLE referencetmp"))
        session.exec(text("DROP TABLE reference"))
        session.exec(text("DROP TABLE paper"))
        session.commit()


def create_ref_table():
    raw_sql = """
    INSERT INTO reference(paper_id, ref_id)
    SELECT DISTINCT	paper_doi.id, paper_ref.id
    FROM referencetmp
    INNER JOIN paper as paper_doi ON referencetmp.doi = paper_doi.doi
    INNER JOIN paper as paper_ref ON referencetmp.ref_to_doi = paper_ref.doi
    """

    with get_session() as session:
        session.exec(text(raw_sql))
        session.commit()


def load_config(file_name: str) -> Config:
    with open(file_name, "rb") as f:
        data = tomllib.load(f)
        return Config(**data)


def main():
    logging.basicConfig(level=logging.WARNING)
    for logger_name in ["sqlalchemy.engine"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    config = load_config("crossref_db.toml")
    connect_db(config.db.url)
    clean_db()
    create_db()
    import_into_db(config.ftp)
    create_ref_table()


if __name__ == "__main__":
    main()
