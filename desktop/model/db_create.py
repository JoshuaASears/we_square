import desktop.data.schema as schema


def create_ledger(title, persons):
    person_objects = []
    for person in persons:
        name = str(person[0])
        email = str(person[1])
        person_objects.append(schema.Person(name, email))

    return schema.Ledger(title, person_objects)
