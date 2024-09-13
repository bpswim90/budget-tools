from flask import abort, make_response

from config import db
from models import MatchString, BudgetCategory, match_string_schema


def get_one(match_string_id):
    match_string = MatchString.query.get(match_string_id)

    if match_string is not None:
        return match_string_schema.dump(match_string)
    else:
        abort(
            404, f"Match string with ID {match_string_id} not found"
        )


def update(match_string_id, match_string):
    existing_match_string = MatchString.query.get(match_string_id)

    if existing_match_string:
        update_match_string = match_string_schema.load(
            match_string, session=db.session)
        existing_match_string.text = update_match_string.text
        db.session.merge(existing_match_string)
        db.session.commit()
        return match_string_schema.dump(existing_match_string), 201
    else:
        abort(404, f"Match string with id {match_string_id} not found")


def delete(match_string_id):
    existing_match_string = MatchString.query.get(match_string_id)

    if existing_match_string:
        db.session.delete(existing_match_string)
        db.session.commit()
        return make_response(f"Match string with id {match_string_id} successfully deleted", 204)
    else:
        abort(404, f"Match string with id {match_string_id} not found")


def create(match_string):
    category_id = match_string.get("category_id")
    category = BudgetCategory.query.get(category_id)

    if category:
        new_match_string = match_string_schema.load(
            match_string, session=db.session)
        category.match_strings.append(new_match_string)
        db.session.commit()
        return match_string_schema.dump(new_match_string), 201
    else:
        abort(404, f"Category not found for ID: {category_id}")
