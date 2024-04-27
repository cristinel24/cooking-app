* Added counter collection and a counter for `name` generation, of `type="nameIncrementor"`
To get the value of this counter, please use the function `find_one_and_update`, like in the following code:

```python
counters_collection.find_one_and_update(
    {"type": "nameIncrementor"},
    {"$inc": {"value": 1}}
)["value"]
```

* Changed available roles: 
```python
available_roles = {
    "verified": 0b1,
    "admin": 0b10,
    "premium": 0b100,
    "banned": 0b1000
}
```

* First user will now always be an admin