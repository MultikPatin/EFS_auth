CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work
(
    id            uuid PRIMARY KEY,
    title         TEXT NOT NULL,
    description   TEXT,
    creation_date DATE,
    rating        FLOAT,
    type          TEXT NOT NULL,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

CREATE INDEX IF NOT EXISTS creation_date
    ON content.film_work (creation_date);

CREATE TABLE IF NOT EXISTS content.permission
(
    id            uuid PRIMARY KEY,
    name          TEXT NOT NULL unique,
    description   TEXT,
    created       timestamp with time zone,
    modified      timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.permission_film_work
(
    id              uuid PRIMARY KEY,
    film_work_id    uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    permission_id   uuid NOT NULL REFERENCES content.permission (id) ON DELETE CASCADE,
    created         timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_permission
    ON content.permission_film_work (film_work_id, permission_id);

CREATE TABLE IF NOT EXISTS content.genre
(
    id          uuid PRIMARY KEY,
    name        TEXT NOT NULL unique,
    description TEXT,
    created     timestamp with time zone,
    modified    timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    genre_id     uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    created      timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_genre
    ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person
(
    id        uuid PRIMARY KEY,
    full_name TEXT NOT NULL unique,
    created   timestamp with time zone,
    modified  timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work
(
    id           uuid PRIMARY KEY,
    film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    person_id    uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    role         TEXT NOT NULL,
    created      timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_role
    ON content.person_film_work (film_work_id, person_id, role);
