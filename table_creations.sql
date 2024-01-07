CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title TEXT,
    year INTEGER,
    url TEXT,
    abstract TEXT,
    location TEXT
);

CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT, -- Normally one would enforce NON Null constraints, but not enforced here since extraction is made from GROBID
    middle_name TEXT,
    email TEXT UNIQUE
);

CREATE TABLE written_by (
    article_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES articles(id),
    FOREIGN KEY (author_id) REFERENCES authors(id),
    UNIQUE (article_id, author_id)
);

CREATE TABLE citations (
    article_id INTEGER,
    title TEXT,
    authors TEXT,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);