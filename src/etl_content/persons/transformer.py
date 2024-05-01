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
            person = {
                "uuid": row["uuid"],
                "full_name": row["full_name"],
                "films": json.loads(row["films"])
                if row["films"] is not None
                else [],
            }
            transformed_part.append(person)
        return transformed_part
