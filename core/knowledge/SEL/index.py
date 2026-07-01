from core.knowledge.SEL.data import SEL_CONCEPTS

class SELIndex:

    def search(self, query: str):
        query = query.lower()

        results = []

        for key, value in SEL_CONCEPTS.items():

            if query in key:
                results.append(value)
                continue

            if any(query in tag for tag in value["tags"]):
                results.append(value)

            if query in value["description"].lower():
                results.append(value)

        return results[:3]