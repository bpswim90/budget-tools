from datetime import datetime, timezone
from config import app, db
from models import BudgetCategory, MatchString

BUDGET_CATEGORIES = [
    {
        "title": "art",
        "match_strings": ["DISCOVER"]
    },
    {
        "title": "car maintenance",
        "match_strings": ["waterway", "hondapartsnow.com"]
    },
    {
        "title": "coffee/pastries",
        "match_strings": ["coffee"]
    },
    {
        "title": "entertainment",
        "match_strings": ["nintendo"]
    },
    {
        "title": "give back",
        "match_strings": ["KWMU", "save the children"]
    },
    {
        "title": "health",
        "match_strings": ["walgreens"]
    },
    {
        "title": "home goods",
        "match_strings": ["home depot"]
    },
    {
        "title": "hygiene",
        "match_strings": ["allison hunter"]
    },
    {
        "title": "income, interest",
        "match_strings": ["Interest Paid"]
    },
    {
        "title": "income, slalom",
        "match_strings": ["SLALOM"]
    },
    {
        "title": "learn",
        "match_strings": ["carla lalli", "dreaming spanish", "nytimes", "realpython"]
    },
    {
        "title": "rent",
        "match_strings": ["AppFolio", "Garcia Property"]
    },
    {
        "title": "tech subscriptions",
        "match_strings": ["apple.com/bill", "amazon prime"]
    },
    {
        "title": "utilities",
        "match_strings": ["Spire"]
    },
    {
        "title": "wellness activities",
        "match_strings": ["south city 3150 sublette ave"]
    },
    {
        "title": "work expense",
        "match_strings": ["amazon web services"]
    }
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in BUDGET_CATEGORIES:
        new_category = BudgetCategory(title=data.get("title"))
        for match_string in data.get("match_strings"):
            new_category.match_strings.append(
                MatchString(
                    text=match_string
                )
            )
        db.session.add(new_category)
    db.session.commit()
