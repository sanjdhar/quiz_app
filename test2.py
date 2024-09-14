from google.cloud import datastore

# For help authenticating your client, visit
# https://cloud.google.com/docs/authentication/getting-started

client = datastore.Client()

with client.transaction():
    incomplete_key = client.key("Task")

    task = datastore.Entity(key=incomplete_key)

    task.update(
        {
            "category": "Personal",
            "done": False,
            "priority": 6,
            "description": "Buy groceries2",
        }
    )

    client.put(task)


query = client.query(kind="Task")
#query.add_filter("done", "=", False)
#query.add_filter("priority", ">=", 4)
#query.order = ["-priority"]

results = list(query.fetch())
print(type(results))
print(results)



