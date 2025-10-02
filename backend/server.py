"""FastAPI server exposing AI agent endpoints."""

import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from starlette.middleware.cors import CORSMiddleware

from ai_agents.agents import AgentConfig, ChatAgent, SearchAgent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent


class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StatusCheckCreate(BaseModel):
    client_name: str


class ChatRequest(BaseModel):
    message: str
    agent_type: str = "chat"
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    success: bool
    response: str
    agent_type: str
    capabilities: List[str]
    metadata: dict = Field(default_factory=dict)
    error: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


class SearchResponse(BaseModel):
    success: bool
    query: str
    summary: str
    search_results: Optional[dict] = None
    sources_count: int
    error: Optional[str] = None


# Photography Models
class Photo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    category: str  # portrait, wedding, landscape, commercial
    imageData: str  # base64 encoded
    description: str = ""
    featured: bool = False
    order: int = 0
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PhotoCreate(BaseModel):
    title: str
    category: str
    imageData: str
    description: str = ""
    featured: bool = False
    order: int = 0


class PhotoUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    imageData: Optional[str] = None
    description: Optional[str] = None
    featured: Optional[bool] = None
    order: Optional[int] = None


# Testimonial Models
class Testimonial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    clientName: str
    testimonialText: str
    rating: int  # 1-5
    order: int = 0
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TestimonialCreate(BaseModel):
    clientName: str
    testimonialText: str
    rating: int
    order: int = 0


# Contact Models
class ContactInquiry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: str = ""
    message: str
    submittedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "new"  # new, contacted, closed


class ContactInquiryCreate(BaseModel):
    name: str
    email: str
    phone: str = ""
    message: str


# About Models
class AboutContent(BaseModel):
    id: str = "about"
    bioText: str
    photographerName: str
    tagline: str
    portraitImage: str = ""  # URL or base64 for photographer portrait
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AboutContentUpdate(BaseModel):
    bioText: Optional[str] = None
    photographerName: Optional[str] = None
    tagline: Optional[str] = None
    portraitImage: Optional[str] = None


def _ensure_db(request: Request):
    try:
        return request.app.state.db
    except AttributeError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=503, detail="Database not ready") from exc


def _get_agent_cache(request: Request) -> Dict[str, object]:
    if not hasattr(request.app.state, "agent_cache"):
        request.app.state.agent_cache = {}
    return request.app.state.agent_cache


async def _get_or_create_agent(request: Request, agent_type: str):
    cache = _get_agent_cache(request)
    if agent_type in cache:
        return cache[agent_type]

    config: AgentConfig = request.app.state.agent_config

    if agent_type == "search":
        cache[agent_type] = SearchAgent(config)
    elif agent_type == "chat":
        cache[agent_type] = ChatAgent(config)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown agent type '{agent_type}'")

    return cache[agent_type]


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv(ROOT_DIR / ".env")

    mongo_url = os.getenv("MONGO_URL")
    db_name = os.getenv("DB_NAME")

    if not mongo_url or not db_name:
        missing = [name for name, value in {"MONGO_URL": mongo_url, "DB_NAME": db_name}.items() if not value]
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    client = AsyncIOMotorClient(mongo_url)

    try:
        app.state.mongo_client = client
        app.state.db = client[db_name]
        app.state.agent_config = AgentConfig()
        app.state.agent_cache = {}
        logger.info("AI Agents API starting up")
        yield
    finally:
        client.close()
        logger.info("AI Agents API shutdown complete")


app = FastAPI(
    title="AI Agents API",
    description="Minimal AI Agents API with LangGraph and MCP support",
    lifespan=lifespan,
)

api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate, request: Request):
    db = _ensure_db(request)
    status_obj = StatusCheck(**input.model_dump())
    await db.status_checks.insert_one(status_obj.model_dump())
    return status_obj


@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(request: Request):
    db = _ensure_db(request)
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]


@api_router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(chat_request: ChatRequest, request: Request):
    try:
        agent = await _get_or_create_agent(request, chat_request.agent_type)
        response = await agent.execute(chat_request.message)

        return ChatResponse(
            success=response.success,
            response=response.content,
            agent_type=chat_request.agent_type,
            capabilities=agent.get_capabilities(),
            metadata=response.metadata,
            error=response.error,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error in chat endpoint")
        return ChatResponse(
            success=False,
            response="",
            agent_type=chat_request.agent_type,
            capabilities=[],
            error=str(exc),
        )


@api_router.post("/search", response_model=SearchResponse)
async def search_and_summarize(search_request: SearchRequest, request: Request):
    try:
        search_agent = await _get_or_create_agent(request, "search")
        search_prompt = (
            f"Search for information about: {search_request.query}. "
            "Provide a comprehensive summary with key findings."
        )
        result = await search_agent.execute(search_prompt, use_tools=True)

        if result.success:
            metadata = result.metadata or {}
            return SearchResponse(
                success=True,
                query=search_request.query,
                summary=result.content,
                search_results=metadata,
                sources_count=int(metadata.get("tool_run_count", metadata.get("tools_used", 0)) or 0),
            )

        return SearchResponse(
            success=False,
            query=search_request.query,
            summary="",
            sources_count=0,
            error=result.error,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error in search endpoint")
        return SearchResponse(
            success=False,
            query=search_request.query,
            summary="",
            sources_count=0,
            error=str(exc),
        )


@api_router.get("/agents/capabilities")
async def get_agent_capabilities(request: Request):
    try:
        search_agent = await _get_or_create_agent(request, "search")
        chat_agent = await _get_or_create_agent(request, "chat")

        return {
            "success": True,
            "capabilities": {
                "search_agent": search_agent.get_capabilities(),
                "chat_agent": chat_agent.get_capabilities(),
            },
        }
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error getting capabilities")
        return {"success": False, "error": str(exc)}


# Photography Endpoints
@api_router.get("/photos", response_model=List[Photo])
async def get_photos(request: Request, category: Optional[str] = None):
    db = _ensure_db(request)
    query = {"category": category} if category else {}
    photos = await db.photos.find(query).sort("order", 1).to_list(1000)
    return [Photo(**photo) for photo in photos]


@api_router.post("/photos", response_model=Photo)
async def create_photo(photo: PhotoCreate, request: Request):
    db = _ensure_db(request)
    photo_obj = Photo(**photo.model_dump())
    await db.photos.insert_one(photo_obj.model_dump())
    return photo_obj


@api_router.put("/photos/{photo_id}", response_model=Photo)
async def update_photo(photo_id: str, photo_update: PhotoUpdate, request: Request):
    db = _ensure_db(request)
    update_data = {k: v for k, v in photo_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await db.photos.find_one_and_update(
        {"id": photo_id},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="Photo not found")

    return Photo(**result)


@api_router.delete("/photos/{photo_id}")
async def delete_photo(photo_id: str, request: Request):
    db = _ensure_db(request)
    result = await db.photos.delete_one({"id": photo_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Photo not found")

    return {"success": True, "message": "Photo deleted"}


# Testimonial Endpoints
@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials(request: Request):
    db = _ensure_db(request)
    testimonials = await db.testimonials.find().sort("order", 1).to_list(1000)
    return [Testimonial(**testimonial) for testimonial in testimonials]


@api_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate, request: Request):
    db = _ensure_db(request)
    testimonial_obj = Testimonial(**testimonial.model_dump())
    await db.testimonials.insert_one(testimonial_obj.model_dump())
    return testimonial_obj


# Contact Endpoints
@api_router.post("/contact", response_model=ContactInquiry)
async def submit_contact_inquiry(inquiry: ContactInquiryCreate, request: Request):
    db = _ensure_db(request)
    inquiry_obj = ContactInquiry(**inquiry.model_dump())
    await db.contact_inquiries.insert_one(inquiry_obj.model_dump())
    return inquiry_obj


@api_router.get("/contact/inquiries", response_model=List[ContactInquiry])
async def get_contact_inquiries(request: Request):
    db = _ensure_db(request)
    inquiries = await db.contact_inquiries.find().sort("submittedAt", -1).to_list(1000)
    return [ContactInquiry(**inquiry) for inquiry in inquiries]


# About Endpoints
@api_router.get("/about", response_model=AboutContent)
async def get_about(request: Request):
    db = _ensure_db(request)
    about = await db.about.find_one({"id": "about"})

    if not about:
        # Return default content if none exists
        return AboutContent(
            bioText="Professional photographer capturing moments that matter.",
            photographerName="Your Name",
            tagline="Capturing Life's Beautiful Moments",
            portraitImage=""
        )

    return AboutContent(**about)


@api_router.put("/about", response_model=AboutContent)
async def update_about(about_update: AboutContentUpdate, request: Request):
    db = _ensure_db(request)
    update_data = {k: v for k, v in about_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_data["updatedAt"] = datetime.now(timezone.utc)

    result = await db.about.find_one_and_update(
        {"id": "about"},
        {"$set": update_data},
        upsert=True,
        return_document=True
    )

    return AboutContent(**result)


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
