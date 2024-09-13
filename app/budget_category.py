from flask import make_response, abort
from models import BudgetCategory, budget_categories_schema, budget_category_schema

from config import db


def get_all():
    budget_categories = BudgetCategory.query.all()
    return budget_categories_schema.dump(budget_categories)


def create(budget_category):
    title = budget_category.get("title")

    existing_category = BudgetCategory.query.filter(
        BudgetCategory.title == title).one_or_none()

    if existing_category is None:
        new_category = budget_category_schema.load(
            budget_category, session=db.session)
        db.session.add(new_category)
        db.session.commit()
        return budget_category_schema.dump(new_category), 201
    else:
        abort(406, f"Category with title {title} already exists")


def get_one(category_id):
    category = BudgetCategory.query.filter(
        BudgetCategory.id == category_id).one_or_none()

    if category is not None:
        return budget_category_schema.dump(category)
    else:
        abort(
            404, f"Category with id {category_id} not found"
        )


def update(category_id, budget_category):
    existing_category = BudgetCategory.query.filter(
        BudgetCategory.id == category_id).one_or_none()

    if existing_category:
        update_category = budget_category_schema.load(
            budget_category, session=db.session)
        existing_category.title = update_category.title
        db.session.merge(existing_category)
        db.session.commit()
        return budget_category_schema.dump(existing_category), 201
    else:
        abort(
            404,
            f"Category with id {category_id} not found"
        )


def delete(category_id):
    existing_category = BudgetCategory.query.filter(
        BudgetCategory.id == category_id).one_or_none()
    if existing_category:
        db.session.delete(existing_category)
        db.session.commit()
        return make_response(
            f"Category with id {category_id} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Category with id {category_id} not found"
        )
