class BaseTransformer:
    @staticmethod
    def transform(extracted_part: dict) -> list[dict]:
        transformed_part = []
        for row in extracted_part:
            permission = {
                "id": row["uuid"],
                "name": row["name"],
                "description": row["description"],
                "created": row["created_at"],
                "modified": row["updated_at"],
            }
            transformed_part.append(permission)
        return transformed_part
