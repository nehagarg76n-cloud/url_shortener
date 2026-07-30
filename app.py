from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import random
import string

DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class URLRequest(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    original_url: str
    short_code: str
    short_url: str

    class Config:
        from_attributes = True


def generate_short_code(length=6):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )


app = FastAPI(title="URL Shortener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/shorten", response_model=URLResponse)
def create_short_url(
    request: URLRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):
    original_url = str(request.original_url)

    existing = db.query(URL).filter(
        URL.original_url == original_url
    ).first()

    if existing:
        return {
            "original_url": existing.original_url,
            "short_code": existing.short_code,
            "short_url": str(http_request.base_url) + existing.short_code,
        }

    short_code = generate_short_code()

    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    new_url = URL(
        original_url=original_url,
        short_code=short_code,
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return {
        "original_url": new_url.original_url,
        "short_code": new_url.short_code,
        "short_url": str(http_request.base_url) + new_url.short_code,
    }


@app.get("/all", response_model=list[URLResponse])
def get_all_urls(
    request: Request,
    db: Session = Depends(get_db),
):
    urls = db.query(URL).all()

    return [
        {
            "original_url": u.original_url,
            "short_code": u.short_code,
            "short_url": str(request.base_url) + u.short_code,
        }
        for u in urls
    ]


@app.get("/{short_code}")
def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db),
):
    print("Searching:", short_code)

    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    return RedirectResponse(
        url=url.original_url,
        status_code=307,
    )


@app.delete("/delete/{short_code}")
def delete_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    url = db.query(URL).filter(
        URL.short_code == short_code
    ).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    db.delete(url)
    db.commit()

    return {
        "message": "URL deleted successfully"
    }