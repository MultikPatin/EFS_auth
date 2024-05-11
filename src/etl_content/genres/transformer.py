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
            genre = {
                "uuid": row["uuid"],
                "name": row["name"],
                "description": row["description"],
            }
            transformed_part.append(genre)
        return transformed_part
