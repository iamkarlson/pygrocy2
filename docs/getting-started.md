# Getting Started

## Installation

```bash
pip install pygrocy2
```

## Requirements

- Python >= 3.12
- A running [Grocy](https://grocy.info/) instance with API access

## Connecting to Grocy

```python
from pygrocy2 import Grocy

# Basic connection
grocy = Grocy("https://your-grocy-instance.com", "YOUR_API_KEY")

# With custom port and path
grocy = Grocy(
    "https://your-grocy-instance.com",
    "YOUR_API_KEY",
    port=9192,
    path="grocy",       # if Grocy is behind a subpath
    verify_ssl=True,
    debug=False,
)
```

The `Grocy` class constructs the API URL as `{base_url}:{port}/api/` (or `{base_url}:{port}/{path}/api/` when a path is provided).

## Local Development with Docker

The repository includes a `docker-compose.yml` that spins up a Grocy demo instance with a pre-seeded API key, so you can start experimenting immediately.

**Start the instance:**

```bash
docker compose up -d
```

This launches Grocy in demo mode on `localhost:9192` and automatically inserts a
known API key (`test_local_devenv`) into the demo database.

**Connect to it:**

```python
from pygrocy2 import Grocy

grocy = Grocy("http://localhost", "test_local_devenv", port=9192)

for product in grocy.stock():
    print(f"{product.name}: {product.available_amount}")
```

!!! tip
    Check out the [Example Notebook](example.ipynb) for a runnable walkthrough
    you can open in Jupyter.

## Working with Stock

```python
# Current stock
stock = grocy.stock()
for product in stock:
    print(f"{product.name}: {product.available_amount}")

# Add product to stock
grocy.add_product(product_id=1, amount=5, price=2.99)

# Consume a product
grocy.consume_product(product_id=1, amount=1)

# Open a product
grocy.open_product(product_id=1)

# Products that are due, overdue, or expired
due = grocy.due_products(get_details=True)
overdue = grocy.overdue_products(get_details=True)
expired = grocy.expired_products(get_details=True)
missing = grocy.missing_products(get_details=True)

# Lookup by barcode
product = grocy.product_by_barcode("4006381333931")
```

## Shopping Lists

```python
# Get shopping list items
items = grocy.shopping_list(get_details=True)
for item in items:
    print(f"{item.product.name}: {item.amount} (done: {item.done})")

# Add a product to the shopping list
grocy.add_product_to_shopping_list(product_id=1, amount=3)

# Mark first product of the shopping list as done
grocy.mark_product_in_shoppping_list(shopping_list_item_id=items[0].id, done=True)

# Add all missing products
grocy.add_missing_product_to_shopping_list()

# Clear the shopping list
grocy.clear_shopping_list()
```

## Chores

```python
from datetime import datetime

# List all chores
chores = grocy.chores(get_details=True)
for chore in chores:
    print(f"{chore.name} - next: {chore.next_estimated_execution_time}")

# Execute a chore
grocy.execute_chore(chore_id=1, done_by=1)
```

## Tasks

```python
# List tasks
tasks = grocy.tasks()
for task in tasks:
    print(f"{task.name} - due: {task.due_date}")

# Complete a task
grocy.complete_task(task_id=1)
```

## Batteries

```python
# List batteries
batteries = grocy.batteries(get_details=True)
for battery in batteries:
    print(f"{battery.name}: last charged {battery.last_charged}")

# Charge a battery
grocy.charge_battery(battery_id=1)
```

## Meal Plans

```python
# Get meal plan items
meals = grocy.meal_plan(get_details=True)
for meal in meals:
    print(f"{meal.day}: {meal.recipe.name if meal.recipe else meal.note}")

# Get a recipe
recipe = grocy.recipe(recipe_id=1)
print(f"{recipe.name} ({recipe.base_servings} servings)")
```

## Generic CRUD Operations

For any Grocy entity type, you can use the generic CRUD methods:

```python
from pygrocy2 import Grocy
from pygrocy2.data_models.generic import EntityType

grocy = Grocy("https://example.com", "API_KEY")

# List all objects of a type
locations = grocy.get_generic_objects_for_type(EntityType.LOCATIONS)

# Get a single object
location = grocy.get_generic(EntityType.LOCATIONS, object_id=1)

# Create
grocy.add_generic(EntityType.LOCATIONS, {"name": "Pantry"})

# Update
grocy.update_generic(EntityType.LOCATIONS, object_id=1, updated_data={"name": "Kitchen Pantry"})

# Delete
grocy.delete_generic(EntityType.LOCATIONS, object_id=1)
```

## The `get_details` Pattern

Many methods accept a `get_details=True` parameter. When enabled, each returned object makes an additional API call to fetch full details (name, barcodes, etc.). Without it, you only get the summary data from the list endpoint.

```python
# Summary only (1 API call)
stock = grocy.stock()

# Full details (1 + N API calls)
due = grocy.due_products(get_details=True)
for product in due:
    print(product.name)       # available with details
    print(product.barcodes)   # available with details
```

## Error Handling

```python
from pygrocy2.errors import GrocyError

try:
    grocy.product(product_id=99999)
except GrocyError as e:
    print(f"HTTP {e.status_code}: {e.message}")
    if e.is_client_error:
        print("Client error (4xx)")
    elif e.is_server_error:
        print("Server error (5xx)")
```

## Debug Mode

Enable debug logging to see all HTTP requests and responses:

```python
grocy = Grocy("https://example.com", "API_KEY", debug=True)
```
