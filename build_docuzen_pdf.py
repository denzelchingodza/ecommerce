#!/usr/bin/env python3
"""DocuZen Backend Deep-Dive PDF generator."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUT = "/sessions/hopeful-inspiring-heisenberg/mnt/ecommerce/DocuZen_Backend_Deep_Dive.pdf"

W, H = A4
ML = MR = 20*mm
MT = MB = 18*mm

# ── Colour palette ──────────────────────────────────────────────────────────
C_NAVY    = colors.HexColor("#1A3A5C")
C_BLUE    = colors.HexColor("#1A5276")
C_TEAL    = colors.HexColor("#148F77")
C_AMBER   = colors.HexColor("#D35400")
C_PURPLE  = colors.HexColor("#6C3483")
C_GREEN   = colors.HexColor("#1E8449")
C_RED     = colors.HexColor("#922B21")
C_BG_CODE = colors.HexColor("#1E1E2E")
C_BG_ALT  = colors.HexColor("#EBF5FB")
C_BG_NOTE = colors.HexColor("#FEF9E7")
C_BG_GOOD = colors.HexColor("#EAFAF1")
C_LIGHT   = colors.HexColor("#F4F6F7")
C_LINE    = colors.HexColor("#2E86C1")
C_WHITE   = colors.white
C_BLACK   = colors.black
C_GRAY    = colors.HexColor("#5D6D7E")
C_CODE_FG = colors.HexColor("#CDD6F4")

# ── Styles ──────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

BASE = dict(fontName="Helvetica", fontSize=10, leading=15, textColor=C_BLACK)

sTitle   = S("Title",   fontName="Helvetica-Bold", fontSize=28, leading=34, textColor=C_NAVY, spaceAfter=6, alignment=TA_CENTER)
sSubT    = S("SubT",    fontName="Helvetica",       fontSize=14, leading=18, textColor=C_BLUE, spaceAfter=4, alignment=TA_CENTER)
sLabel   = S("Label",   fontName="Helvetica",       fontSize=10, leading=13, textColor=C_GRAY, alignment=TA_CENTER)
sH1      = S("H1",      fontName="Helvetica-Bold", fontSize=17, leading=22, textColor=C_NAVY,  spaceBefore=18, spaceAfter=6)
sH2      = S("H2",      fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=C_BLUE,  spaceBefore=14, spaceAfter=4)
sH3      = S("H3",      fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=C_TEAL,  spaceBefore=10, spaceAfter=3)
sBody    = S("Body",    fontName="Helvetica",       fontSize=10, leading=16, textColor=C_BLACK, spaceAfter=6,  alignment=TA_JUSTIFY)
sBodyL   = S("BodyL",   fontName="Helvetica",       fontSize=10, leading=16, textColor=C_BLACK, spaceAfter=6)
sBullet  = S("Bullet",  fontName="Helvetica",       fontSize=10, leading=15, textColor=C_BLACK, leftIndent=14, spaceAfter=3, bulletIndent=4, bulletFontName="Helvetica", bulletFontSize=10)
sCode    = S("Code",    fontName="Courier",         fontSize=8.5, leading=13, textColor=C_CODE_FG, backColor=C_BG_CODE, leftIndent=8, rightIndent=8, spaceAfter=2, spaceBefore=2)
sCodeL   = S("CodeL",   fontName="Courier",         fontSize=8.5, leading=13, textColor=C_BLACK, leftIndent=8, rightIndent=8, spaceAfter=2, spaceBefore=2)
sAlt     = S("Alt",     fontName="Helvetica",       fontSize=9.5, leading=14, textColor=C_BLACK, spaceAfter=3, leftIndent=8)
sNote    = S("Note",    fontName="Helvetica-Oblique", fontSize=9.5, leading=14, textColor=C_AMBER, spaceAfter=4, leftIndent=8)
sRef     = S("Ref",     fontName="Helvetica",       fontSize=9,   leading=13, textColor=C_BLUE, spaceAfter=3, leftIndent=12)
sSmall   = S("Small",   fontName="Helvetica",       fontSize=8.5, leading=12, textColor=C_GRAY)
sFileH   = S("FileH",   fontName="Courier-Bold",    fontSize=11,  leading=15, textColor=C_WHITE, backColor=C_NAVY, spaceBefore=14, spaceAfter=4, leftIndent=6)
sCaption = S("Caption", fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=8)

def hr(color=C_LINE, w=1.5): return HRFlowable(width="100%", thickness=w, color=color, spaceAfter=6, spaceBefore=4)
def sp(h=6): return Spacer(1, h)
def P(text, style=None): return Paragraph(text, style or sBody)
def B(text): return Paragraph(f"<bullet>•</bullet> {text}", sBullet)

def code_block(lines, dark=True):
    st = sCode if dark else sCodeL
    cells = [[Paragraph(line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), st)] for line in lines]
    bg = C_BG_CODE if dark else C_LIGHT
    t = Table(cells, colWidths=[W - ML - MR - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return t

def info_box(title, lines, bg=C_BG_ALT, tc=C_BLUE):
    header = [[Paragraph(f"<b>{title}</b>", S("IH", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=tc))]]
    rows   = [[Paragraph(l, sAlt)] for l in lines]
    all_rows = header + rows
    t = Table(all_rows, colWidths=[W - ML - MR - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BACKGROUND", (0,0), (-1,0), tc.clone(alpha=0.12) if hasattr(tc,'clone') else bg),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("BOX", (0,0), (-1,-1), 1, tc),
        ("LINEBELOW", (0,0), (-1,0), 0.5, tc),
    ]))
    return t

def alt_box(chosen, why, alternatives):
    rows = [
        [Paragraph("<b>We used:</b>", sAlt), Paragraph(f"<b>{chosen}</b>", S("x", fontName="Helvetica-Bold", fontSize=10, leading=14, textColor=C_GREEN))],
        [Paragraph("<b>Why:</b>", sAlt),     Paragraph(why, sAlt)],
        [Paragraph("<b>Alternatives:</b>", sAlt), Paragraph(alternatives, sAlt)],
    ]
    t = Table(rows, colWidths=[(W-ML-MR-4)*0.22, (W-ML-MR-4)*0.78])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_BG_GOOD),
        ("BOX", (0,0), (-1,-1), 1, C_GREEN),
        ("LINEAFTER",  (0,0), (0,-1), 0.5, C_GREEN),
        ("LINEBELOW",  (0,0), (-1,1), 0.3, colors.HexColor("#ABEBC6")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return t

def watch_box(resources):
    rows = [[Paragraph("<b>Watch / Read to understand this concept:</b>", S("wh", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=C_PURPLE))]]
    for r in resources:
        rows.append([Paragraph(f"  ▶  {r}", S("wr", fontName="Helvetica", fontSize=9, leading=13, textColor=C_PURPLE))])
    t = Table(rows, colWidths=[W - ML - MR - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F5EEF8")),
        ("BOX", (0,0), (-1,-1), 1, C_PURPLE),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def diagram_box(title, lines):
    all_lines = [f"  {l}" for l in lines]
    rows = [[Paragraph(f"<b>{title}</b>", S("dh", fontName="Courier-Bold", fontSize=9.5, leading=13, textColor=C_WHITE))]]
    for l in all_lines:
        rows.append([Paragraph(l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), S("dl", fontName="Courier", fontSize=9, leading=13, textColor=C_CODE_FG))])
    t = Table(rows, colWidths=[W - ML - MR - 4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), C_BG_CODE),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E4057")),
        ("BOX", (0,0), (-1,-1), 1, C_LINE),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
    ]))
    return t

# ── Build story ──────────────────────────────────────────────────────────────
story = []

# ── COVER ────────────────────────────────────────────────────────────────────
story += [
    sp(60), P("DocuZen", sTitle), sp(4),
    P("Backend Deep-Dive", sSubT), sp(2),
    P("A complete technical reference — every file, every concept, why it was used,", sLabel),
    P("what else could have been used, and what to study to understand it fully.", sLabel),
    sp(30), hr(C_NAVY, 2), sp(8),
    P("Written for: Denzel Chingodza", sSmall), sp(2),
    P("Project: DocuZen — AI Document Q&A Tool", sSmall), sp(2),
    P("Stack: Python  |  FastAPI  |  PostgreSQL  |  pgvector  |  OpenAI API  |  Docker  |  Next.js", sSmall),
    PageBreak(),
]

# ── TABLE OF CONTENTS ────────────────────────────────────────────────────────
story += [P("Contents", sH1), hr(), sp(4)]
toc = [
    ("1.", "How DocuZen Works — The Big Picture", "3"),
    ("2.", "The RAG Pattern — Core Concept", "4"),
    ("3.", "File: config.py — Settings & Environment", "6"),
    ("4.", "File: database.py — Database Connection", "7"),
    ("5.", "File: models/document.py — Database Schema", "9"),
    ("6.", "File: services/parser.py — Extracting Text", "11"),
    ("7.", "File: services/chunker.py — Splitting Text into Chunks", "13"),
    ("8.", "File: services/embeddings.py — Creating Meaning Vectors", "16"),
    ("9.", "File: services/rag.py — Retrieval & Answering", "19"),
    ("10.", "File: routers/documents.py — Upload API", "23"),
    ("11.", "File: routers/chat.py — Question API", "25"),
    ("12.", "File: main.py — App Entry Point", "26"),
    ("13.", "File: Dockerfile — Containerisation", "27"),
    ("14.", "Concept Deep-Dive: Async / Await", "28"),
    ("15.", "Concept Deep-Dive: REST APIs & HTTP", "30"),
    ("16.", "Quick Reference — Technology Choices", "32"),
]
tdata = [[P(a, sBodyL), P(b, sBodyL), P(c, sBodyL)] for a,b,c in toc]
ttable = Table(tdata, colWidths=[20, (W-ML-MR-4-20-30), 30])
ttable.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("ALIGN",(2,0),(2,-1),"RIGHT")]))
story += [ttable, PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 1. BIG PICTURE
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("1. How DocuZen Works — The Big Picture", sH1), hr(), sp(4)]
story += [P("""DocuZen lets you upload any PDF or Word document, ask questions about it in plain English, and receive accurate answers with page citations. The application does not search for keywords — it understands meaning. This is possible because of a technique called RAG (explained in section 2).""", sBody)]
story += [sp(6), diagram_box("DocuZen Full Flow — From Upload to Answer", [
    "USER uploads a file (PDF or DOCX)",
    "       |",
    "       v",
    "  [ parser.py ]  ----  Extracts raw text page by page",
    "       |",
    "       v",
    "  [ chunker.py ] ----  Splits text into 500-token overlapping chunks",
    "       |",
    "       v",
    "  [ embeddings.py ] -- Sends chunks to OpenAI -> 1536 numbers per chunk",
    "       |",
    "       v",
    "  [ PostgreSQL + pgvector ] -- Stores chunks + their number-vectors",
    "",
    "USER asks a question",
    "       |",
    "       v",
    "  [ embeddings.py ] -- Turns question into 1536 numbers",
    "       |",
    "       v",
    "  [ rag.py ] -- Finds 5 most similar chunks using cosine distance",
    "       |",
    "       v",
    "  [ rag.py ] -- Sends chunks + question to GPT-4o-mini",
    "       |",
    "       v",
    "  Answer + page citations returned to user",
]), sp(8)]

# ═══════════════════════════════════════════════════════════════════════════════
# 2. RAG
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("2. The RAG Pattern — Core Concept", sH1), hr(), sp(4)]
story += [P("""RAG stands for Retrieval-Augmented Generation. It is one of the most important patterns in modern AI engineering. To understand why it exists, you need to understand the problem it solves.""", sBody)]
story += [P("The Problem With Raw Language Models", sH2)]
story += [P("""A language model (like GPT-4) knows a lot from its training data, but it has two major weaknesses: (1) it only knows things up to its training cutoff date, and (2) it does not know about your private documents. If you ask GPT-4 "what are the payment terms in my contract?", it cannot answer because it has never seen your contract. You could paste the whole document into the prompt, but documents can be hundreds of pages long — far too large.""", sBody)]
story += [P("The RAG Solution", sH2)]
story += [P("""Instead of sending the whole document, RAG sends only the most relevant pieces. It works in two phases:""", sBody)]
story += [B("Indexing phase (done once at upload time): break the document into chunks, convert each chunk into a vector (a fingerprint of its meaning), and store everything in a database."), B("Query phase (done at question time): convert the question into the same kind of vector, find which chunks are most similar, and send only those chunks to the LLM as context."), sp(6)]
story += [diagram_box("RAG vs Raw LLM — Side by Side", [
    "RAW LLM APPROACH:                  RAG APPROACH:",
    "  User: 'What are payment terms?'    User: 'What are payment terms?'",
    "  GPT: 'I don't have your contract'  Step 1: embed question -> vector",
    "                                     Step 2: find similar chunks in DB",
    "  OR:                                Step 3: send chunks to GPT as context",
    "  User pastes 200 pages of text      GPT: 'Page 4: invoices due in 30 days'",
    "  -> too expensive, hits token limit",
]), sp(8)]
story += [P("Why RAG Is Considered ML", sH2)]
story += [P("""When people ask how DocuZen relates to machine learning, the answer is that the embedding step IS machine learning. The model that converts text to a 1536-number vector (text-embedding-3-small) is a trained neural network. It learned from billions of examples how to encode semantic meaning into a mathematical space. You are using an ML model's output every time a chunk or question is embedded.""", sBody)]
story += [info_box("RAG vs Alternatives — What Else Could We Have Done?", [
    "KEYWORD SEARCH (like a search engine): fast, simple, but fails when words don't match exactly.",
    "  Example: searching 'payment terms' won't find 'invoices due in 30 days' — no word overlap.",
    "",
    "FINE-TUNING: train the LLM itself on your documents. Very expensive, takes hours, requires",
    "  labelled data, and doesn't update in real-time when documents change.",
    "",
    "RAG (what we used): real-time, no training required, handles any new document instantly,",
    "  answers are grounded in the actual document (less hallucination), with citations.",
    "",
    "FULL CONTEXT WINDOW: stuff the whole document into one prompt. Works for short docs but",
    "  fails for large files, is expensive, and loses precision (model attends to all text equally).",
], bg=C_BG_NOTE, tc=C_AMBER)]
story += [sp(6), watch_box([
    "IBM Technology — 'What is Retrieval Augmented Generation (RAG)?' (YouTube, 8 min)",
    "  Search: 'IBM RAG explained YouTube'",
    "LangChain Blog — 'RAG from scratch' — detailed written walkthrough",
    "  Search: 'LangChain RAG from scratch blog'",
    "3Blue1Brown — 'But what is a neural network?' (YouTube) — to understand embeddings at a deep level",
    "  Search: '3Blue1Brown neural network YouTube'",
]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 3. config.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("3. File: config.py — Settings & Environment Variables", sH1), hr()]
story += [P("""This file defines every configurable value in the application in one place. Instead of hardcoding your database URL, API key, or model name in multiple files, you define them here and import them wherever needed.""", sBody)]
story += [code_block([
    "from pydantic_settings import BaseSettings, SettingsConfigDict",
    "",
    "class Settings(BaseSettings):",
    "    database_url: str = 'postgresql+asyncpg://...'",
    "    openai_api_key: str          # No default — app crashes if missing",
    "    embedding_model: str = 'text-embedding-3-small'",
    "    embedding_dimensions: int = 1536",
    "    llm_model: str = 'gpt-4o-mini'",
    "    chunk_size: int = 500",
    "    chunk_overlap: int = 100",
    "",
    "    model_config = SettingsConfigDict(env_file='.env', extra='ignore')",
    "",
    "settings = Settings()   # One global instance, imported everywhere",
]), sp(6)]
story += [P("Key Concepts", sH2)]
story += [B("<b>BaseSettings (Pydantic):</b> Pydantic is a Python library for data validation. BaseSettings is a special class that reads values from environment variables automatically. When you write `openai_api_key: str` with no default, Pydantic will crash the app at startup if that variable is not set. This is intentional — better to fail loudly at boot than silently at runtime."), B("<b>env_file='.env':</b> The .env file is a plain text file (not committed to Git) that stores secrets like your API key and database password. Example: `OPENAI_API_KEY=sk-abc123`. Pydantic reads this file and injects the values."), B("<b>chunk_size=500, chunk_overlap=100:</b> These are the parameters that control how the document is split. Centralising them here means you can tune the RAG system by changing one number."), sp(6)]
story += [alt_box("Pydantic BaseSettings", "Type-safe, validates types automatically, reads from .env files, crashes loudly if required config is missing.", "python-dotenv + manual casting (more error-prone). Dynaconf (more features but heavier). django-environ (Django-specific).")]
story += [sp(6), watch_box(["Pydantic docs — 'Settings management' — docs.pydantic.dev/latest/concepts/pydantic_settings/", "YouTube: 'Python .env files explained' — search 'python dotenv environment variables tutorial'"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 4. database.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("4. File: database.py — Database Connection", sH1), hr()]
story += [P("""This file handles the connection to PostgreSQL and sets up the ORM (Object Relational Mapper). Every time a request needs the database, it gets a session from here.""", sBody)]
story += [code_block([
    "from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine",
    "from sqlalchemy.orm import DeclarativeBase",
    "",
    "engine = create_async_engine(",
    "    _db_url,",
    "    pool_size=10,          # Keep 10 connections open and ready",
    "    max_overflow=20,       # Allow up to 20 extra connections when busy",
    "    connect_args={'ssl': True},",
    ")",
    "",
    "SessionLocal = async_sessionmaker(engine, class_=AsyncSession, ...)",
    "",
    "class Base(DeclarativeBase):   # All models inherit from this",
    "    pass",
    "",
    "async def get_db():",
    "    async with SessionLocal() as session:",
    "        yield session   # FastAPI injects this into route functions",
    "",
    "async def create_tables():",
    "    async with engine.begin() as conn:",
    "        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))",
    "        await conn.run_sync(Base.metadata.create_all)",
])]
story += [sp(6), P("What Is An ORM?", sH2)]
story += [P("""An ORM (Object Relational Mapper) lets you work with database tables as if they were Python objects, without writing SQL manually. Instead of writing `INSERT INTO documents (id, filename) VALUES (...)`, you write `db.add(Document(filename='file.pdf'))`. The ORM translates your Python into SQL.""", sBody)]
story += [P("Connection Pooling", sH2)]
story += [P("""`pool_size=10` means SQLAlchemy keeps 10 database connections permanently open. Opening a new database connection is slow (it involves a network handshake). By keeping connections open and reusing them, the app responds much faster. `max_overflow=20` means if all 10 are busy, it can open up to 20 more temporarily.""", sBody)]
story += [P("The SSL Workaround", sH2)]
story += [P("""Neon (our serverless Postgres host) requires SSL. The connection URL sometimes contains `?sslmode=require` in the query string, but asyncpg (the async Postgres driver) does not understand that parameter — it wants SSL passed differently. The `_build_engine_url` function strips it from the URL and passes `connect_args={"ssl": True}` instead.""", sBody)]
story += [sp(4), alt_box("SQLAlchemy (async)", "Industry-standard ORM. Excellent async support. Works with many databases. Huge community.", "Raw psycopg2/asyncpg (no abstraction — write raw SQL). Tortoise ORM (async-first, less mature). SQLModel (SQLAlchemy + Pydantic combined, simpler but less flexible).")]
story += [sp(6), info_box("Real-World Example — Connection Pooling", [
    "Imagine a restaurant with 10 waiters (connections). When a customer (request) arrives,",
    "a waiter takes their order to the kitchen (database). The waiter doesn't quit and get rehired",
    "each time — they stay on duty. If all 10 waiters are busy, 20 temporary waiters can be called",
    "in. Without pooling, you'd hire a new waiter for every single customer — extremely slow.",
]), sp(6)]
story += [watch_box(["SQLAlchemy docs: 'Asynchronous I/O (asyncio)' — docs.sqlalchemy.org", "YouTube: 'SQLAlchemy ORM Tutorial' — search 'SQLAlchemy ORM beginner tutorial python'", "YouTube: 'What is a database connection pool?' — search 'database connection pool explained'"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 5. models/document.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("5. File: models/document.py — Database Schema", sH1), hr()]
story += [P("""This file defines the shape of your data — what tables exist in the database and what columns they have. SQLAlchemy reads these Python classes and creates the actual SQL tables.""", sBody)]
story += [code_block([
    "from pgvector.sqlalchemy import Vector",
    "from sqlalchemy.orm import Mapped, mapped_column, relationship",
    "",
    "class Document(Base):",
    "    __tablename__ = 'documents'",
    "    id: Mapped[str] = mapped_column(String, primary_key=True,",
    "                                    default=lambda: str(uuid.uuid4()))",
    "    filename: Mapped[str] = mapped_column(String, nullable=False)",
    "    file_type: Mapped[str] = mapped_column(String, nullable=False)  # 'pdf' or 'docx'",
    "    file_size: Mapped[int] = mapped_column(Integer, nullable=False)",
    "    status: Mapped[str] = mapped_column(String, default='processing')  # processing/ready/failed",
    "    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())",
    "    chunks: Mapped[list['Chunk']] = relationship('Chunk', back_populates='document',",
    "                                                  cascade='all, delete-orphan')",
    "",
    "class Chunk(Base):",
    "    __tablename__ = 'chunks'",
    "    id: Mapped[str] = mapped_column(String, primary_key=True, ...)",
    "    document_id: Mapped[str] = mapped_column(String, ForeignKey('documents.id'))",
    "    content: Mapped[str] = mapped_column(Text)        # The actual text of this chunk",
    "    page_number: Mapped[int] = mapped_column(Integer) # Which page it came from",
    "    chunk_index: Mapped[int] = mapped_column(Integer) # 0, 1, 2, ... order in document",
    "    embedding = mapped_column(Vector(1536))            # The 1536-number meaning vector",
])]
story += [sp(6), P("Understanding the Relationship", sH2)]
story += [P("""A Document has many Chunks. Each Chunk belongs to exactly one Document. This is a one-to-many relationship. In SQL terms, the `chunks` table has a `document_id` column that references the `documents.id` column — this is a foreign key. `cascade='all, delete-orphan'` means when you delete a Document, all its Chunks are automatically deleted too.""", sBody)]
story += [diagram_box("Database Tables — Visual Layout", [
    "  DOCUMENTS table                      CHUNKS table",
    "  +-----------------+-------+          +----------+-------------+-----------+",
    "  | id (PK)         | abc-1 |          | id (PK)  | chunk-001   | chunk-002 |",
    "  | filename        |report |          | doc_id(FK)| abc-1      | abc-1     |",
    "  | file_type       | pdf   |          | content  | 'The rate..'| 'Payment..'|",
    "  | status          | ready |          | page_num |     1       |     1     |",
    "  | created_at      | 12:00 |    <---- | embedding| [0.12, ...] | [0.34,..]|",
    "  +-----------------+-------+          | (1536 floats)                      |",
    "                                       +----------+-------------+-----------+",
]), sp(6)]
story += [P("What Is a UUID?", sH2)]
story += [P("""UUID stands for Universally Unique Identifier. It looks like: `3f6a8e1c-4b72-4d9c-9fbe-1234abcd5678`. Generated randomly, the chance of two being identical is astronomically small (1 in 2 to the power of 122). Used as primary keys instead of simple integers (1, 2, 3...) because: (1) you can generate them without asking the database (no round trip needed), (2) they don't expose how many records you have, (3) they work across distributed systems.""", sBody)]
story += [P("The Vector(1536) Column", sH2)]
story += [P("""This is provided by the pgvector extension — not standard PostgreSQL. It stores a list of 1536 floating-point numbers. The number 1536 comes from the OpenAI text-embedding-3-small model — that model always produces vectors of exactly 1536 dimensions. pgvector also provides efficient mathematical operations on these columns (like cosine distance search).""", sBody)]
story += [sp(4), alt_box("PostgreSQL + pgvector", "One database for both relational data (documents, metadata) and vectors. No extra service needed. Supports SQL joins.", "Pinecone (dedicated vector DB, managed, but costs more and separates your data). Qdrant (open-source dedicated vector DB — DocuZen actually has an old vector_store.py that used Qdrant before switching). Weaviate or Chroma (similar dedicated vector stores).")]
story += [sp(6), watch_box(["YouTube: 'SQL Foreign Keys explained' — search 'SQL foreign key one-to-many relationship'", "YouTube: 'pgvector PostgreSQL tutorial' — search 'pgvector postgres vector similarity search'", "PostgreSQL docs: pgvector — github.com/pgvector/pgvector"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 6. services/parser.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("6. File: services/parser.py — Extracting Text from Files", sH1), hr()]
story += [P("""Before any AI processing can happen, you need the raw text. This file converts binary file bytes (the raw bytes of a PDF or DOCX) into a list of ParsedPage objects — each page becomes an object with a page number and its text content.""", sBody)]
story += [code_block([
    "@dataclass",
    "class ParsedPage:",
    "    page_number: int",
    "    text: str",
    "",
    "# PDF parsing using PyMuPDF",
    "def parse_pdf(file_bytes: bytes) -> list[ParsedPage]:",
    "    with fitz.open(stream=file_bytes, filetype='pdf') as doc:",
    "        for page_num, page in enumerate(doc, start=1):",
    "            text = page.get_text().strip()",
    "            if text:   # Skip blank pages",
    "                pages.append(ParsedPage(page_number=page_num, text=text))",
    "",
    "# DOCX parsing — approximates pages every 40 paragraphs",
    "def parse_docx(file_bytes: bytes) -> list[ParsedPage]:",
    "    doc = DocxDocument(io.BytesIO(file_bytes))",
    "    for para in doc.paragraphs:",
    "        current_text.append(para.text.strip())",
    "        line_count += 1",
    "        if line_count >= 40:   # Treat every 40 paragraphs as one 'page'",
    "            pages.append(ParsedPage(page_number=approx_page, ...))",
])]
story += [sp(6), P("Why PyMuPDF (fitz)?", sH2)]
story += [P("""PDFs are not text files. They are binary files containing instructions for rendering a page visually (draw this glyph at this position). PyMuPDF renders each page and extracts the text layer. The `fitz.open(stream=file_bytes, filetype='pdf')` opens the PDF from memory (no disk write needed). `.get_text()` extracts all text from that page in reading order.""", sBody)]
story += [P("The DOCX Page Problem", sH2)]
story += [P("""Word documents (.docx) are actually ZIP files containing XML. The paragraphs are stored sequentially — there is no concept of 'page' in the data structure. Page breaks are calculated by Microsoft Word at display time based on font size, paper size, margins, etc. Our parser approximates: every 40 paragraphs is treated as one page. This is an imperfect but practical solution — page citations in DOCX files are approximate.""", sBody)]
story += [P("What Is a Dataclass?", sH2)]
story += [P("""Python's `@dataclass` decorator auto-generates `__init__`, `__repr__`, and `__eq__` methods for a class. Without it, you'd write: `class ParsedPage: def __init__(self, page_number, text): self.page_number = page_number; self.text = text`. With it, you just declare the fields and Python handles the rest. Purely for convenience.""", sBody)]
story += [sp(4), alt_box("PyMuPDF (fitz)", "Fast, accurate, handles complex PDFs with images/tables, well-maintained, returns text in reading order.", "pdfplumber: better for tables, slower. pdfminer.six: lower-level, more control, harder to use. pypdf: lighter but less accurate text extraction. Tesseract + pdf2image: for scanned PDFs (images not text layers) — DocuZen does NOT handle scanned PDFs.")]
story += [sp(6), info_box("What Happens With a Scanned PDF?", [
    "A scanned PDF is just an image of a page — there is no text layer, only pixels.",
    "PyMuPDF's .get_text() would return an empty string for such a page.",
    "DocuZen does NOT support scanned PDFs — this is a known limitation.",
    "To support them, you would need OCR (Optical Character Recognition):",
    "  1. Convert PDF pages to images (pdf2image library)",
    "  2. Run Tesseract OCR on each image to extract text",
    "  3. Then proceed with the same chunking/embedding pipeline",
], bg=C_BG_NOTE, tc=C_AMBER), sp(6)]
story += [watch_box(["YouTube: 'What is a PDF really?' — search 'how PDF files work internally'", "PyMuPDF docs — pymupdf.readthedocs.io", "YouTube: 'Python read PDF with PyMuPDF' — search 'PyMuPDF fitz tutorial python'"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 7. services/chunker.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("7. File: services/chunker.py — Splitting Text into Chunks", sH1), hr()]
story += [P("""After parsing, you have the full text of each page. You now need to split it into manageable pieces (chunks) for embedding and retrieval. This is one of the most important design decisions in a RAG system — chunk size directly affects answer quality.""", sBody)]
story += [code_block([
    "import tiktoken",
    "",
    "@dataclass",
    "class TextChunk:",
    "    content: str",
    "    page_number: int",
    "    chunk_index: int",
    "",
    "def chunk_pages(pages: list[ParsedPage]) -> list[TextChunk]:",
    "    enc = tiktoken.get_encoding('cl100k_base')  # GPT-4's tokenizer",
    "    chunk_index = 0",
    "",
    "    for page in pages:",
    "        tokens = enc.encode(page.text)   # Convert text -> list of integers",
    "        start = 0",
    "",
    "        while start < len(tokens):",
    "            end = start + 500              # Take 500 tokens",
    "            chunk_tokens = tokens[start:end]",
    "            content = enc.decode(chunk_tokens)  # Convert back to text",
    "            chunks.append(TextChunk(content, page.page_number, chunk_index))",
    "            chunk_index += 1",
    "            start += 500 - 100  # Move forward 400 tokens (100 overlap)",
])]
story += [sp(6), P("What Is a Token?", sH2)]
story += [P("""AI language models do not process words — they process tokens. A token is roughly 3-4 characters or about 0.75 words on average. Here are examples of how text is tokenised by the cl100k_base encoder (the same one used by GPT-4):""", sBody)]
story += [info_box("Token Examples", [
    "  'Hello'               -> 1 token",
    "  'Hello, World!'       -> 4 tokens: [Hello] [,] [ World] [!]",
    "  'machine learning'    -> 2 tokens: [machine] [ learning]",
    "  'unbelievable'        -> 3 tokens: [unbel] [iev] [able]",
    "  'tokenisation'        -> 4 tokens: [token] [isation] (British spelling costs more!)",
    "  500 tokens            -> approximately 375 words, or about 1 paragraph of text",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), P("Why Not Split by Words or Sentences?", sH2)]
story += [P("""AI models have a token limit — not a word limit. If you split by words, chunks could contain vastly different token counts depending on vocabulary. Splitting by tokens is precise and directly controls how much each chunk costs to embed and process.""", sBody)]
story += [P("The Sliding Window (Overlap)", sH2)]
story += [P("""With chunk_size=500 and chunk_overlap=100, the sliding window moves 400 tokens forward each step (500 - 100 = 400). This means consecutive chunks share 100 tokens of content. Why? Consider this sentence that might straddle a chunk boundary:""", sBody)]
story += [diagram_box("Why Overlap Matters", [
    "Document text: '... the total invoice amount of R5,000 is due within 30 days of...'",
    "",
    "WITHOUT overlap (chunk boundary falls in the middle of this sentence):",
    "  Chunk 7: '... the total invoice amount of R5,000'   <- incomplete",
    "  Chunk 8: 'is due within 30 days of...'              <- incomplete",
    "  Neither chunk fully captures: 'R5,000 due in 30 days' -> retrieval fails",
    "",
    "WITH 100-token overlap:",
    "  Chunk 7: '... the total invoice amount of R5,000 is due within 30 days of...'",
    "  Chunk 8: '... R5,000 is due within 30 days of receipt. Late fees apply...'",
    "  Both chunks capture the complete fact -> retrieval succeeds",
])]
story += [sp(6), P("Chunk Size Trade-offs", sH2)]
story += [info_box("Chunk Size — Bigger vs Smaller", [
    "SMALLER chunks (e.g. 200 tokens):",
    "  + More precise retrieval — each chunk is about one specific idea",
    "  - More chunks to store and embed -> more API cost",
    "  - Less context for the LLM -> may miss surrounding information",
    "",
    "LARGER chunks (e.g. 1000 tokens):",
    "  + More context per retrieved chunk",
    "  - Less precise — a chunk may contain many different topics",
    "  - Costs more to embed and process",
    "",
    "DocuZen uses 500 tokens — a common default that balances precision and context.",
], bg=C_BG_GOOD, tc=C_GREEN)]
story += [sp(6), alt_box("tiktoken (token-based chunking)", "Precise token control. Same tokenizer as the embedding model — what you measure is what gets sent.", "Word-based splitting (imprecise). Sentence splitting with spaCy/NLTK (better semantics, variable chunk sizes). RecursiveCharacterTextSplitter from LangChain (popular alternative, splits on paragraphs then sentences then characters). Semantic chunking (use embeddings to find natural topic boundaries — most accurate but slower).")]
story += [sp(6), watch_box(["YouTube: 'Tokenization explained' — search 'OpenAI tokenization how it works'", "OpenAI Tokenizer (interactive): platform.openai.com/tokenizer — paste text and see how it tokenises", "YouTube: 'RAG chunking strategies' — search 'RAG chunking strategy comparison'", "LangChain docs: 'Text Splitters' — python.langchain.com/docs/how_to/split_by_token"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 8. services/embeddings.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("8. File: services/embeddings.py — Creating Meaning Vectors", sH1), hr()]
story += [P("""This is the machine learning core of DocuZen. An embedding model takes text as input and outputs a list of numbers (a vector) that encodes the semantic meaning of that text. Similar meanings produce vectors that are mathematically close to each other.""", sBody)]
story += [code_block([
    "from openai import AsyncOpenAI",
    "",
    "client = AsyncOpenAI(api_key=settings.openai_api_key)",
    "",
    "async def embed_text(text: str) -> list[float]:",
    "    response = await client.embeddings.create(",
    "        model='text-embedding-3-small',",
    "        input=text,",
    "    )",
    "    return response.data[0].embedding  # A list of 1536 floats",
    "",
    "async def embed_batch(texts: list[str]) -> list[list[float]]:",
    "    response = await client.embeddings.create(",
    "        model='text-embedding-3-small',",
    "        input=texts,   # Send ALL chunks in one API call",
    "    )",
    "    return [item.embedding for item in response.data]",
])]
story += [sp(6), P("What Is an Embedding — The Math Explained", sH2)]
story += [P("""Imagine a two-dimensional map where every English word has a location (x, y). Words with related meanings are placed near each other. 'King' and 'Queen' are close. 'Car' and 'Automobile' are close. 'Dog' and 'Banana' are far apart. A text embedding does this in 1536 dimensions instead of 2. You cannot visualise 1536 dimensions, but the mathematics works the same way.""", sBody)]
story += [diagram_box("Embedding Space — 2D Simplified Illustration", [
    "                    HIGH y (abstract concepts)",
    "                         |",
    "        'royalty'     Queen . King",
    "                         |",
    "        'vehicles'   Car . Automobile . Truck",
    "                         |",
    "        'animals'    Dog . Cat . Wolf",
    "                         |         LOW y (concrete)",
    "              <-----------+----------->",
    "              LOW x                  HIGH x",
    "",
    "In reality: 1536 axes, not 2. Each number in the vector is one axis.",
    "The embedding model was trained to place similar texts near each other.",
])]
story += [sp(6), P("text-embedding-3-small — What Is It?", sH2)]
story += [P("""text-embedding-3-small is a neural network model trained by OpenAI. It was trained on vast amounts of text data to learn associations between words, phrases, and concepts. The training process optimised the model so that similar texts produce similar vectors. You call it via an API — you do not run the model yourself.""", sBody)]
story += [P("Single vs Batch Embedding", sH2)]
story += [P("""`embed_text` sends one piece of text and gets one vector back. `embed_batch` sends a list of texts and gets a list of vectors back — in a single API call. When processing a 50-page document, you might have 200 chunks. Embedding them one by one would mean 200 API calls. Batching them means 1 API call. The OpenAI API supports batching natively — much faster and cheaper.""", sBody)]
story += [sp(4), info_box("What Does 1536 Mean?", [
    "text-embedding-3-small always outputs exactly 1536 numbers per piece of text.",
    "This is called the 'embedding dimension' or 'vector dimension'.",
    "Every chunk gets a vector: [0.0234, -0.0891, 0.1234, ... (1536 total)]",
    "The numbers themselves have no human-readable meaning — only their relationships do.",
    "text-embedding-3-large outputs 3072 dimensions (more accurate, more expensive).",
    "OpenAI's ada-002 (older model) outputs 1536 dimensions too.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), alt_box("OpenAI text-embedding-3-small", "High quality, fast, cheap ($0.02 per million tokens), no GPU required — API call. Same company as GPT-4.", "Sentence-BERT / sentence-transformers: open source, run locally, free but needs GPU or is slow. Cohere Embed: competitor, similar quality. Google's text-embedding-gecko: Google Cloud. HuggingFace BAAI/bge models: strong open-source models, self-hosted.")]
story += [sp(6), watch_box(["YouTube: 'Word Embeddings and Word2Vec' — search 'word embeddings explained visually'", "YouTube: 'Sentence embeddings explained' — search 'sentence transformers embeddings tutorial'", "3Blue1Brown: 'Visualizing Attention' — part of his Transformer series, explains how neural networks process language", "OpenAI docs: 'Embeddings' — platform.openai.com/docs/guides/embeddings"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 9. services/rag.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("9. File: services/rag.py — Retrieval and Answering", sH1), hr()]
story += [P("""This is the heart of the system. It contains three functions: store_chunks (saves embeddings to the database), search_chunks (finds the most relevant chunks for a question), and answer_question (puts it all together).""", sBody)]
story += [code_block([
    "# FUNCTION 1: Store embeddings after uploading",
    "async def store_chunks(db, document_id, chunks):",
    "    texts = [chunk.content for chunk in chunks]",
    "    embeddings = await embed_batch(texts)   # One API call for all chunks",
    "    # chunks already saved to DB — now update their embedding column",
    "    for db_chunk, embedding in zip(db_chunks, embeddings):",
    "        db_chunk.embedding = embedding",
    "    await db.commit()",
    "",
    "# FUNCTION 2: Find relevant chunks",
    "async def search_chunks(db, document_id, question, top_k=5):",
    "    query_vector = await embed_text(question)  # Embed the question",
    "    result = await db.execute(",
    "        select(Chunk)",
    "        .where(Chunk.document_id == document_id)",
    "        .order_by(Chunk.embedding.cosine_distance(query_vector))",
    "        .limit(5)   # Return the 5 closest chunks",
    "    )",
    "    return result.scalars().all()",
])]
story += [sp(4), code_block([
    "# FUNCTION 3: Answer the question",
    "async def answer_question(db, document_id, question):",
    "    chunks = await search_chunks(db, document_id, question)",
    "",
    "    context = '\\n\\n---\\n\\n'.join([",
    "        f'[Page {c.page_number}, Chunk {c.chunk_index}]\\n{c.content}'",
    "        for c in chunks",
    "    ])",
    "",
    "    prompt = f'''You are a document analysis assistant.",
    "Answer the question using ONLY the provided document excerpts.",
    "If the answer is not in the excerpts, say so clearly.",
    "Always cite the page number when referencing specific content.",
    "",
    "Document excerpts:",
    "{context}",
    "",
    "Question: {question}'''",
    "",
    "    response = await openai_client.chat.completions.create(",
    "        model='gpt-4o-mini',",
    "        messages=[{'role': 'user', 'content': prompt}],",
    "        temperature=0.1,   # Low = factual, not creative",
    "    )",
    "    return response.choices[0].message.content, chunks",
])]
story += [sp(6), P("Cosine Distance — The Mathematics", sH2)]
story += [P("""Cosine distance measures how different the direction of two vectors is. Two vectors pointing in the same direction have cosine distance 0 (identical meaning). Two vectors at right angles (90 degrees) have cosine distance 1 (unrelated). Cosine distance = 1 - cosine_similarity.""", sBody)]
story += [diagram_box("Cosine Similarity — Visual Explanation", [
    "Two vectors in 2D space (simplified from 1536D):",
    "",
    "  Question vector:  [0.8, 0.6]   (points northeast)",
    "  Chunk A vector:   [0.9, 0.5]   (points northeast, similar direction)",
    "  Chunk B vector:   [-0.7, 0.7]  (points northwest, different direction)",
    "",
    "  cos_similarity(Question, Chunk A) = 0.97  -> very similar meaning",
    "  cos_similarity(Question, Chunk B) = 0.14  -> very different meaning",
    "",
    "  cosine_distance = 1 - cosine_similarity",
    "  .order_by(cosine_distance) puts the MOST SIMILAR chunk FIRST",
    "",
    "  Formula: cos(angle) = (A . B) / (|A| * |B|)",
    "  Where (A . B) is the dot product and |A|, |B| are the magnitudes.",
])]
story += [sp(6), P("Why Cosine and Not Euclidean Distance?", sH2)]
story += [P("""Euclidean distance (straight-line distance between points) is affected by the length of a vector. A short text produces a vector of smaller magnitude than a long text, making them appear different even if the meaning is the same. Cosine distance ignores magnitude — it only cares about direction (meaning). This makes it the correct choice for semantic similarity.""", sBody)]
story += [P("The Prompt Engineering", sH2)]
story += [P("""The prompt sent to GPT-4o-mini is carefully constructed. 'Answer using ONLY the provided excerpts' prevents the model from using its own knowledge (which could hallucinate or be wrong). 'If the answer is not in the excerpts, say so clearly' forces honesty when the relevant content isn't there. 'Always cite the page number' makes the output useful and verifiable. `temperature=0.1` keeps the model close to factual — lower temperature means less randomness.""", sBody)]
story += [sp(4), info_box("What Is Temperature in an LLM?", [
    "Temperature controls how 'creative' or 'random' the model's responses are.",
    "temperature=0.0: deterministic, always picks the most likely next token (very factual)",
    "temperature=0.7: balanced — default for chat (some creativity)",
    "temperature=1.0+: very creative, more varied, can become incoherent",
    "For Q&A on documents, we want 0.1 — factual answers, minimal creative deviation.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), alt_box("pgvector cosine_distance", "Built into PostgreSQL, no extra service, can SQL-join with document metadata, good performance at moderate scale.", "Dedicated vector DBs (Pinecone, Qdrant, Weaviate): faster at massive scale (millions of vectors), but another service to manage. FAISS (Facebook AI Similarity Search): in-memory, extremely fast, but no persistence without extra work. Annoy (Spotify): fast approximate nearest neighbour, in-memory only.")]
story += [sp(6), watch_box(["YouTube: '3Blue1Brown — Dot products and duality' — explains the math of dot product beautifully", "YouTube: 'Cosine Similarity explained' — search 'cosine similarity NLP explained'", "YouTube: 'Prompt Engineering Guide' — search 'prompt engineering best practices 2024'", "OpenAI docs: 'Chat Completions' — platform.openai.com/docs/guides/chat-completions"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 10. routers/documents.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("10. File: routers/documents.py — The Upload API", sH1), hr()]
story += [P("""This file defines the HTTP endpoints for document management: upload, list, get one, and delete. It is the entry point for all document processing.""", sBody)]
story += [code_block([
    "@router.post('/upload', response_model=DocumentResponse)",
    "async def upload_document(",
    "    file: UploadFile = File(...),     # The file sent from the browser",
    "    db: AsyncSession = Depends(get_db),  # Injected DB session",
    "):",
    "    # 1. Validate file type (only PDF and DOCX)",
    "    if file.content_type not in ALLOWED_TYPES:",
    "        raise HTTPException(status_code=400, detail='Only PDF and DOCX supported')",
    "",
    "    file_bytes = await file.read()   # Read the raw bytes into memory",
    "",
    "    # 2. Validate size (max 50MB)",
    "    if len(file_bytes) > 50 * 1024 * 1024:",
    "        raise HTTPException(status_code=400, detail='File exceeds 50MB limit')",
    "",
    "    # 3. Save document record first (status='processing')",
    "    doc = Document(filename=file.filename, file_type=file_type, ...)",
    "    db.add(doc)",
    "    await db.commit()",
    "",
    "    # 4. Run the full pipeline",
    "    pages = parse_file(file_bytes, file_type)   # Extract text",
    "    chunks = chunk_pages(pages)                  # Split into chunks",
    "    db_chunks = [Chunk(...) for chunk in chunks] # Save chunks to DB",
    "    db.add_all(db_chunks)",
    "    await db.commit()",
    "    await store_chunks(db, doc.id, chunks)       # Embed and store vectors",
    "",
    "    doc.status = 'ready'   # Mark complete",
    "    await db.commit()",
    "    return doc",
])]
story += [sp(6), P("Dependency Injection — How get_db Works", sH2)]
story += [P("""FastAPI's `Depends(get_db)` is dependency injection. When a request arrives, FastAPI calls `get_db()`, which opens a database session, yields it to the route function, and closes it when the request is done. This ensures every request gets a fresh session and sessions are always properly closed — even if an error occurs.""", sBody)]
story += [P("Why Save to DB Before Processing?", sH2)]
story += [P("""The document record is saved with `status='processing'` before the heavy processing starts. This way, if the server restarts mid-processing, you can see which documents are stuck in 'processing' state and retry them. If saving happened only at the end, a crash would leave no trace. This is called the 'write-ahead' pattern.""", sBody)]
story += [P("Error Handling", sH2)]
story += [P("""The try/except block catches any processing error and sets `doc.status = 'failed'`. The user sees a 500 error with the detail. The document record remains in the database with status='failed' so you can inspect what went wrong.""", sBody)]
story += [sp(4), alt_box("FastAPI UploadFile", "Async file handling, content_type detection, memory-efficient streaming. Built into FastAPI.", "Flask's request.files (synchronous, no async). Django's request.FILES (synchronous). Storing to disk first then reading (slower, requires cleanup)."), sp(6)]
story += [watch_box(["YouTube: 'FastAPI File Upload Tutorial' — search 'FastAPI file upload example'", "FastAPI docs: 'Request Files' — fastapi.tiangolo.com/tutorial/request-files/", "YouTube: 'Dependency Injection in FastAPI' — search 'FastAPI depends injection tutorial'"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 11. routers/chat.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("11. File: routers/chat.py — The Question API", sH1), hr()]
story += [P("""The simplest file in the backend. One endpoint: receive a question and document ID, call answer_question, return the answer with sources.""", sBody)]
story += [code_block([
    "@router.post('/', response_model=ChatResponse)",
    "async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):",
    "    if not request.question.strip():",
    "        raise HTTPException(status_code=400, detail='Question cannot be empty')",
    "",
    "    answer, sources = await answer_question(db, request.document_id, request.question)",
    "",
    "    source_chunks = [",
    "        SourceChunk(content=s.content, page_number=s.page_number,",
    "                    chunk_index=s.chunk_index, score=0.0)",
    "        for s in sources",
    "    ]",
    "    return ChatResponse(answer=answer, sources=source_chunks)",
])]
story += [sp(6), P("Schemas (ChatRequest / ChatResponse)", sH2)]
story += [P("""These are Pydantic models defined in schemas/document.py. They define the exact shape of request and response JSON. FastAPI auto-validates incoming JSON against the schema and rejects malformed requests before they reach the route function. The `response_model=ChatResponse` tells FastAPI to validate the output too — preventing bugs where you return unexpected data.""", sBody)]
story += [code_block([
    "# schemas/document.py (inferred from the chat router usage)",
    "class ChatRequest(BaseModel):",
    "    document_id: str",
    "    question: str",
    "",
    "class SourceChunk(BaseModel):",
    "    content: str",
    "    page_number: int",
    "    chunk_index: int",
    "    score: float",
    "",
    "class ChatResponse(BaseModel):",
    "    answer: str",
    "    sources: list[SourceChunk]",
], dark=False), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 12. main.py
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("12. File: main.py — Application Entry Point", sH1), hr()]
story += [P("""main.py wires everything together: it creates the FastAPI app, registers middleware, attaches routers, and defines startup behaviour.""", sBody)]
story += [code_block([
    "@asynccontextmanager",
    "async def lifespan(app: FastAPI):",
    "    await create_tables()   # Enable pgvector + create all tables on startup",
    "    yield                   # App runs here",
    "    # cleanup code would go here (after yield)",
    "",
    "app = FastAPI(title='DocuZen API', lifespan=lifespan)",
    "",
    "app.add_middleware(CORSMiddleware,",
    "    allow_origins=['http://localhost:3000', 'https://docuzen.netlify.app'],",
    "    allow_methods=['*'],",
    "    allow_headers=['*'],",
    ")",
    "",
    "app.include_router(documents.router)  # Mounts all /documents routes",
    "app.include_router(chat.router)       # Mounts all /chat routes",
    "",
    "@app.get('/health')",
    "async def health():",
    "    return {'status': 'ok'}  # Used by Render to check app is alive",
])]
story += [sp(6), P("What Is CORS?", sH2)]
story += [P("""CORS (Cross-Origin Resource Sharing) is a browser security feature. When your Next.js frontend (running at docuzen.netlify.app) makes a request to the FastAPI backend (running at api.render.com), the browser checks if the server explicitly allows requests from that origin. Without CORS middleware, the browser blocks all requests from your frontend. `allow_origins` lists which domains are allowed to call the API.""", sBody)]
story += [info_box("Why Allow Only Specific Origins?", [
    "Allowing all origins ('*') would mean any website on the internet could call your API.",
    "This could lead to API abuse (someone else's site using your OpenAI key for free).",
    "By listing only 'https://docuzen.netlify.app', only your frontend can use the API.",
    "Note: This is enforced by browsers only — a direct curl/Postman call ignores CORS headers.",
], bg=C_BG_NOTE, tc=C_AMBER)]
story += [sp(6), P("The Lifespan Context Manager", sH2)]
story += [P("""The `@asynccontextmanager lifespan` function runs code when the app starts (before the first request) and when it shuts down (after the last request). `create_tables()` runs at startup — it enables the pgvector extension and creates all tables if they don't exist yet. This makes the app self-initialising: deploy it to a fresh database and it sets itself up.""", sBody)]
story += [sp(4), watch_box(["YouTube: 'FastAPI CORS explained' — search 'FastAPI CORS middleware tutorial'", "MDN Web Docs: 'Cross-Origin Resource Sharing (CORS)' — developer.mozilla.org/en-US/docs/Web/HTTP/CORS", "FastAPI docs: 'Bigger Applications' — fastapi.tiangolo.com/tutorial/bigger-applications/"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 13. Dockerfile
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("13. File: Dockerfile — Containerisation", sH1), hr()]
story += [P("""A Dockerfile defines how to build a container image for the application. A container is a lightweight, isolated environment that packages the app and all its dependencies together. 'It works on my machine' stops being a problem — the container runs identically everywhere.""", sBody)]
story += [code_block([
    "FROM python:3.11-slim   # Start from an official Python image (Debian-based)",
    "",
    "WORKDIR /app            # All subsequent commands run in /app",
    "",
    "COPY requirements.txt . # Copy dependency list first (for Docker layer caching)",
    "RUN pip install --no-cache-dir -r requirements.txt  # Install dependencies",
    "",
    "COPY . .                # Copy application code",
    "",
    "EXPOSE 8000             # Document that the app listens on port 8000",
    "",
    "CMD ['uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000']",
])]
story += [sp(6), P("Docker Layer Caching — Why COPY requirements.txt Before COPY . .?", sH2)]
story += [P("""Docker builds images in layers. Each instruction creates a new layer. If a layer hasn't changed, Docker reuses the cached version. By copying requirements.txt before the application code, the `pip install` layer is only re-run when dependencies change (rare) — not every time you change a Python file (frequent). This makes rebuilds much faster.""", sBody)]
story += [P("Uvicorn — The ASGI Server", sH2)]
story += [P("""FastAPI is an ASGI framework. ASGI (Asynchronous Server Gateway Interface) is the Python standard for async web servers. Uvicorn is the ASGI server that actually handles HTTP connections and passes requests to FastAPI. `--host 0.0.0.0` means 'accept connections on all network interfaces' (required inside Docker so external traffic can reach the container).""", sBody)]
story += [sp(4), alt_box("Docker + Render", "Simple deployment, consistent environment, Render handles HTTPS, auto-redeploy from Git, free tier available.", "AWS ECS / EKS (more powerful, much more complex). Fly.io (Docker-based, good free tier). Railway (even simpler than Render). Bare metal (no containerisation — dependency hell across environments).")]
story += [sp(6), watch_box(["YouTube: 'Docker explained in 100 seconds' — Fireship YouTube channel", "YouTube: 'Docker for beginners full course' — search 'docker tutorial beginner python'", "YouTube: 'What is ASGI?' — search 'ASGI vs WSGI python explained'"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 14. ASYNC / AWAIT
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("14. Concept Deep-Dive: Async / Await", sH1), hr()]
story += [P("""The entire DocuZen backend uses `async def` functions and `await` keywords. This is Python's concurrency model for I/O-bound work. Understanding it is critical because it explains why the app is fast and how FastAPI handles multiple requests simultaneously.""", sBody)]
story += [P("The Problem: Waiting Is Expensive", sH2)]
story += [P("""A server that processes requests one at a time (synchronous) blocks on every slow operation: waiting for a database response, waiting for OpenAI's API to reply, waiting for a file to be read. During that wait, the server is idle — it could be serving other users.""", sBody)]
story += [diagram_box("Sync vs Async — Two Requests Arriving At The Same Time", [
    "SYNCHRONOUS (traditional):          ASYNC (DocuZen):",
    "Request 1 arrives                   Request 1 arrives",
    "  |--embed(chunk 1)--WAITING--|       |--await embed(chunk 1)--|",
    "                               |      Request 2 arrives         |",
    "  (server idle, request 2      |        |--await embed(q2)--|   |",
    "   is stuck waiting)           |      Request 2 gets response    |",
    "Request 1 gets response        |      Request 1 gets response",
    "Request 2 starts               |",
    "                               |      Both finish in ~same time",
    "Total: 2x the wait time        |      Total: ~1x the wait time",
])]
story += [sp(6), P("How async/await Works", sH2)]
story += [P("""`async def` declares a coroutine — a function that can pause and resume. `await` pauses the coroutine until the awaited thing is ready, and hands control back to the event loop. The event loop (uvicorn's event loop) then runs another coroutine that is ready. When the awaited operation completes, the event loop resumes the paused coroutine.""", sBody)]
story += [code_block([
    "# SYNCHRONOUS — server blocks here, doing nothing, waiting",
    "def get_embedding_sync(text):",
    "    response = openai.embeddings.create(...)  # Wait 300ms — server frozen",
    "    return response.data[0].embedding",
    "",
    "# ASYNCHRONOUS — server can do other work while waiting",
    "async def get_embedding_async(text):",
    "    response = await openai_client.embeddings.create(...)  # Pause, do other work",
    "    return response.data[0].embedding",
])]
story += [sp(6), alt_box("asyncio (async/await)", "Perfect for I/O-bound work: DB queries, API calls, file reads. Python's native concurrency model.", "Threading: traditional concurrency, fine for I/O, but Python's GIL limits CPU parallelism. Multiprocessing: true parallelism for CPU-bound work (not needed here). Celery / task queues: for background tasks that should run outside the request-response cycle."), sp(6)]
story += [watch_box(["YouTube: 'Python asyncio explained' — search 'python async await explained simply'", "YouTube: 'Async IO in Python: A Complete Walkthrough' — Real Python YouTube channel", "Python docs: 'asyncio — Asynchronous I/O' — docs.python.org/3/library/asyncio.html"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 15. REST APIs
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("15. Concept Deep-Dive: REST APIs & HTTP", sH1), hr()]
story += [P("""DocuZen's backend communicates with its frontend through a REST API over HTTP. Understanding REST and HTTP is fundamental to understanding how any web application works.""", sBody)]
story += [P("HTTP Methods Used in DocuZen", sH2)]
story += [info_box("HTTP Methods — What Each One Means", [
    "POST /documents/upload  — Send new data to the server (upload a file). Creates a resource.",
    "GET  /documents/        — Retrieve a list. Server returns data, changes nothing.",
    "GET  /documents/{id}    — Retrieve one specific document by its ID.",
    "DELETE /documents/{id}  — Remove a resource from the server.",
    "POST /chat/             — Send a question (not a GET because we're sending data: document_id + question).",
    "",
    "Convention: GET = read only. POST = create. PUT/PATCH = update. DELETE = remove.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), P("HTTP Status Codes", sH2)]
story += [info_box("Status Codes Used in DocuZen", [
    "200 OK             — Request succeeded. Used for GET, DELETE responses.",
    "201 Created        — Resource was created. Returned after successful upload.",
    "400 Bad Request    — Client sent bad data (wrong file type, empty question).",
    "404 Not Found      — Document with that ID does not exist.",
    "500 Internal Error — Something went wrong on the server (processing failed).",
], bg=C_BG_GOOD, tc=C_GREEN)]
story += [sp(6), P("What Happens in a Real Request", sH2)]
story += [diagram_box("POST /documents/upload — Full Request Lifecycle", [
    "Browser (Next.js frontend):",
    "  1. User picks a PDF file",
    "  2. JavaScript creates FormData object with the file",
    "  3. fetch('https://api.render.com/documents/upload', {method:'POST', body:formData})",
    "",
    "HTTP travels over the internet to Render's servers",
    "",
    "FastAPI backend (Render/Docker):",
    "  4. Uvicorn receives the HTTP request",
    "  5. FastAPI parses the multipart form data -> UploadFile object",
    "  6. upload_document() runs (parse -> chunk -> embed -> store)",
    "  7. Returns: {id:'abc-123', filename:'report.pdf', status:'ready'}",
    "",
    "HTTP response travels back to the browser",
    "",
    "Browser:",
    "  8. JavaScript receives JSON, updates the UI to show document is ready",
])]
story += [sp(6), watch_box(["YouTube: 'HTTP Crash Course' — Traversy Media YouTube channel, search 'HTTP crash course traversy'", "YouTube: 'REST API concepts and examples' — search 'REST API tutorial beginners'", "YouTube: 'FastAPI tutorial' — official FastAPI docs have a great video walkthrough"]), PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# 16. QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("16. Quick Reference — Technology Choices", sH1), hr(), sp(4)]
tdata = [
    ["Technology", "What It Does", "Category", "Main Alternative"],
    ["FastAPI", "Python web framework, handles HTTP requests/responses", "Web Framework", "Flask, Django"],
    ["SQLAlchemy", "ORM — Python <-> PostgreSQL", "Database ORM", "raw psycopg2, Tortoise ORM"],
    ["PostgreSQL", "Relational database (tables, foreign keys)", "Database", "MySQL, SQLite"],
    ["pgvector", "Adds vector columns + cosine search to Postgres", "Vector Store", "Pinecone, Qdrant, Weaviate"],
    ["Neon", "Serverless hosted Postgres (cloud)", "Hosting", "Supabase, ElephantSQL, RDS"],
    ["Pydantic", "Data validation, settings management", "Validation", "marshmallow, attrs"],
    ["OpenAI API", "Embeddings (text->vector) + GPT-4o-mini (answers)", "AI / ML", "Cohere, sentence-transformers"],
    ["tiktoken", "Tokenises text for precise chunk sizing", "Text Processing", "transformers tokenizer"],
    ["PyMuPDF", "Extracts text from PDFs page by page", "File Parsing", "pdfplumber, pdfminer"],
    ["python-docx", "Reads text from Word (.docx) files", "File Parsing", "Apache POI (Java)"],
    ["Docker", "Packages app in a container for deployment", "DevOps", "bare metal, VMs"],
    ["Render", "Cloud hosting for Docker containers", "Cloud Hosting", "Fly.io, Railway, AWS ECS"],
    ["Uvicorn", "ASGI server that runs FastAPI", "Web Server", "Hypercorn, Daphne"],
    ["asyncpg", "Async PostgreSQL driver for Python", "DB Driver", "psycopg2 (sync)"],
    ["asyncio", "Python's async concurrency framework", "Concurrency", "threading, multiprocessing"],
]
col_widths = [(W-ML-MR-4)*x for x in [0.2, 0.35, 0.2, 0.25]]
t = Table(tdata, colWidths=col_widths)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), C_NAVY),
    ("TEXTCOLOR",  (0,0), (-1,0), C_WHITE),
    ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 8.5),
    ("FONTNAME",   (0,1), (-1,-1), "Helvetica"),
    ("FONTNAME",   (0,1), (0,-1), "Courier-Bold"),
    ("BACKGROUND", (0,1), (-1,-1), C_WHITE),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [C_WHITE, C_LIGHT]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#BDC3C7")),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
]))
story += [t, sp(12)]
story += [hr(C_NAVY, 2), sp(8)]
story += [P("This document was generated specifically for Denzel Chingodza to help him understand and speak confidently about DocuZen in interviews and technical conversations.", sCaption)]
story += [P("DocuZen — github.com/denzelchingodza/doc-analyzer  |  Live at docuzen.netlify.app", sCaption)]

# ── Build PDF ────────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_GRAY)
    canvas.drawString(ML, 12*mm, "DocuZen Backend Deep-Dive")
    canvas.drawRightString(W - MR, 12*mm, f"Page {doc.page}")
    canvas.restoreState()

pdf = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)
pdf.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Done: {OUT}")
