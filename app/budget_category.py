from datetime import datetime, timezone
from flask import make_response, abort


BUDGET_CATEGORIES = {
    "1": {"title": "art", "created": "2024-09-06 19:22:39", "updated": "2024-09-06 19:22:39"},
    "2": {"title": "car maintenance", "created": "2024-09-06 19:25:05", "updated": "2024-09-06 19:25:05"},
    "3": {"title": "coffee/pastries", "created": "2024-09-06 19:25:05", "updated": "2024-09-06 19:25:05"}
}


def get_all():
    return list(BUDGET_CATEGORIES.values())


def create(budgetCategory):
    title = budgetCategory.get("title")

    current_titles = []
    for category in BUDGET_CATEGORIES:
        current_titles.append(category.title)

    if title and title not in current_titles:
        new_id = len(current_titles) + 1
        BUDGET_CATEGORIES[new_id] = {
            "title": title,
            "created": datetime.now(timezone.utc),
            "updated": datetime.now(timezone.utc)
        }
        return BUDGET_CATEGORIES[new_id], 201
    else:
        abort(406, f"Category with title {title} already exists")


def get_one(categoryId):
    if categoryId in BUDGET_CATEGORIES:
        return BUDGET_CATEGORIES[categoryId]
    else:
        abort(
            404, f"Category with id {categoryId} not found"
        )


def update(categoryId, budgetCategory):
    if categoryId in BUDGET_CATEGORIES:
        BUDGET_CATEGORIES[categoryId]["title"] = budgetCategory.get("title")
        BUDGET_CATEGORIES[categoryId]["updated"] = datetime.now(timezone.utc)
        return BUDGET_CATEGORIES[categoryId]
    else:
        abort(
            404,
            f"Category with id {categoryId} not found"
        )


def delete(categoryId):
    if categoryId in BUDGET_CATEGORIES:
        del BUDGET_CATEGORIES[categoryId]
        return make_response(
            f"Category with id {categoryId} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Category with id {categoryId} not found"
        )
