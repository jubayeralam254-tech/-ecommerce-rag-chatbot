from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Business
from .schemas import BusinessResponse, ScrapeRequest, ScrapeResponse
from .scraper import scrape_google_maps

app = FastAPI(title="Business API")


@app.on_event("startup")
def on_startup() -> None:
    # Creates the table if it does not exist yet.
    Base.metadata.create_all(bind=engine)


@app.get("/businesses", response_model=list[BusinessResponse])
def get_businesses(
    city: str | None = Query(default=None),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Business)

    if city:
        query = query.filter(Business.city == city)

    if category:
        query = query.filter(Business.category == category)

    return query.all()


@app.post("/scrape", response_model=ScrapeResponse)
def scrape_businesses(payload: ScrapeRequest, db: Session = Depends(get_db)):
    if not payload.city.strip() or not payload.category.strip():
        raise HTTPException(status_code=400, detail="city and category are required")

    scraped_items = scrape_google_maps(city=payload.city, category=payload.category)

    created_count = 0
    skipped_count = 0

    for item in scraped_items:
        existing = (
            db.query(Business)
            .filter(
                Business.name == item["name"],
                Business.address == item["address"],
                Business.city == item["city"],
                Business.category == item["category"],
            )
            .first()
        )

        if existing:
            skipped_count += 1
            continue

        business = Business(
            name=item["name"],
            address=item["address"],
            phone=item["phone"],
            rating=item["rating"],
            category=item["category"],
            city=item["city"],
        )
        db.add(business)
        created_count += 1

    db.commit()

    return ScrapeResponse(
        scraped_count=len(scraped_items),
        created_count=created_count,
        skipped_count=skipped_count,
    )
