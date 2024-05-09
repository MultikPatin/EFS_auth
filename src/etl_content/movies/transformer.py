import json

from src.etl_content.helpers.transformer import BaseTransformer


class Transformer(BaseTransformer):
    @staticmethod
    def transform(extracted_part: dict) -> list[dict]:
        """
        Обработка данных из Postgres
        и преобразование в формат для ElasticSearch
        """
        transformed_part = []
        for row in extracted_part:
            filmwork = {
                "uuid": row["uuid"],
                "imdb_rating": row["imdb_rating"],
                "title": row["title"],
                "description": row["description"],
                "genre": json.loads(row["genre"])
                if row["genre"] is not None
                else [],
                "directors": json.loads(row["directors"])
                if row["directors"] is not None
                else [],
                "actors": json.loads(row["actors"])
                if row["actors"] is not None
                else [],
                "writers": json.loads(row["writers"])
                if row["writers"] is not None
                else [],
                "permissions": json.loads(row["permissions"])
                if row["permissions"] is not None
                else [],
            }
            transformed_part.append(filmwork)
        return transformed_part
