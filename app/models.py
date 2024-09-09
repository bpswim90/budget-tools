from datetime import datetime, timezone
from config import db, ma


class BudgetCategory(db.Model):
    __tablename__ = "budget_category"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))


class BudgetCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BudgetCategory
        load_instance = True
        sqla_session = db.session


budget_category_schema = BudgetCategorySchema()
budget_categories_schema = BudgetCategorySchema(many=True)
