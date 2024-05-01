from src.etl_content.config.base import _ELASTIC_SETTINGS

_ELASTIC_MAPPING = {
    "dynamic": "strict",
    "properties": {
        "uuid": {"type": "keyword"},
        "full_name": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {"raw": {"type": "keyword"}},
        },
        "films": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
                "uuid": {"type": "keyword"},
                "title": {"type": "text", "analyzer": "ru_en"},
                "imdb_rating": {"type": "float"},
                "roles": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

ELASTIC_DATA = {
    "settings": _ELASTIC_SETTINGS,
    "mappings": _ELASTIC_MAPPING,
}

SQL_QUERY = """
        SELECT
            p.id as uuid,
            p.full_name,
            p.modified,
            concat(
                '[', string_agg(
                    DISTINCT CASE WHEN
                        pfw.role IS NOT NULL THEN json_build_object(
                            'uuid', pfw.film_work_id,
                            'title', fw.title,
                            'imdb_rating', fw.rating,
                            'roles',(
                                SELECT
                                    json_agg(DISTINCT t.role)
                                FROM
                                    content.person_film_work as t
                                WHERE pfw.person_id = t.person_id
                                )
                            ) #>> '{{}}' END, ','
                    ), ']'
                ) AS films
        FROM
            content.person as p
            LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
            LEFT JOIN content.film_work fw ON  fw.id = pfw.film_work_id
        WHERE p.modified > '{}'
        GROUP BY p.id
        ORDER BY MAX(p.modified) DESC
        """
