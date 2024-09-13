from datetime import datetime, timezone
from marshmallow_sqlalchemy import fields
from config import db, ma


class MatchString(db.Model):
    __tablename__ = "match_string"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("budget_category.id"))
    text = db.Column(db.String(32))
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))


class MatchStringSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MatchString
        load_instance = True
        sqla_session = db.session
        include_fk = True


class BudgetCategory(db.Model):
    __tablename__ = "budget_category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))
    match_strings = db.relationship(
        MatchString,
        backref="budget_category",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(MatchString.created)"
    )


class BudgetCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BudgetCategory
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    match_strings = fields.Nested(MatchStringSchema, many=True)


match_string_schema = MatchStringSchema()
budget_category_schema = BudgetCategorySchema()
budget_categories_schema = BudgetCategorySchema(many=True)
