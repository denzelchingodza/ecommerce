const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, BorderStyle, WidthType,
  ExternalHyperlink, TabStopType, TabStopPosition,
} = require('/tmp/docx-install/lib/node_modules/docx');
const fs = require('fs');

const ACCENT = "1A5276";
const RULE   = "2C3E50";
const MUTED  = "555555";
const BLACK  = "000000";

const sp = (before, after) => ({ before, after });

function rule() {
  return new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE, space: 2 } },
    spacing: sp(0, 80),
    children: [],
  });
}

function sectionHeading(text) {
  return new Paragraph({
    spacing: sp(180, 0),
    children: [new TextRun({ text, bold: true, size: 22, color: ACCENT, font: "Calibri" })],
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: ACCENT, space: 1 } },
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: sp(36, 0),
    children: [new TextRun({ text, size: 19, font: "Calibri", color: BLACK })],
  });
}

function jobHeader(title, org, period) {
  return new Paragraph({
    spacing: sp(160, 0),
    tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
    children: [
      new TextRun({ text: title, bold: true, size: 21, font: "Calibri", color: BLACK }),
      new TextRun({ text: " · " + org, size: 19, font: "Calibri", color: MUTED }),
      new TextRun({ text: "\t" + period, size: 18, font: "Calibri", color: MUTED, italic: true }),
    ],
  });
}

function skillRow(label, value) {
  const border = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new TableRow({
    children: [
      new TableCell({
        borders,
        width: { size: 1800, type: WidthType.DXA },
        margins: { top: 40, bottom: 40, left: 0, right: 120 },
        children: [new Paragraph({ spacing: sp(0,0), children: [new TextRun({ text: label, bold: true, size: 19, font: "Calibri", color: BLACK })] })],
      }),
      new TableCell({
        borders,
        width: { size: 7560, type: WidthType.DXA },
        margins: { top: 40, bottom: 40, left: 120, right: 0 },
        children: [new Paragraph({ spacing: sp(0,0), children: [new TextRun({ text: value, size: 19, font: "Calibri", color: BLACK })] })],
      }),
    ],
  });
}

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 480, hanging: 240 } } },
      }],
    }],
  },
  styles: {
    default: { document: { run: { font: "Calibri", size: 20 } } },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
      },
    },
    children: [

      // ── NAME ──────────────────────────────────────────────
      new Paragraph({
        spacing: sp(0, 4),
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "DENZEL CHINGODZA", bold: true, size: 40, font: "Calibri", color: ACCENT })],
      }),
      new Paragraph({
        spacing: sp(0, 6),
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Machine Learning & Software Engineering  ·  Cape Town, South Africa", size: 19, font: "Calibri", color: MUTED })],
      }),
      new Paragraph({
        spacing: sp(0, 0),
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "+27 64 983 7714", size: 18, font: "Calibri", color: MUTED }),
          new TextRun({ text: "   |   ", size: 18, font: "Calibri", color: MUTED }),
          new ExternalHyperlink({ link: "mailto:denzel.chingodza@icloud.com", children: [new TextRun({ text: "denzel.chingodza@icloud.com", size: 18, font: "Calibri", color: ACCENT, underline: {} })] }),
          new TextRun({ text: "   |   ", size: 18, font: "Calibri", color: MUTED }),
          new ExternalHyperlink({ link: "https://linkedin.com/in/denzel-chingodza-45b6ab3a0", children: [new TextRun({ text: "linkedin.com/in/denzel-chingodza-45b6ab3a0", size: 18, font: "Calibri", color: ACCENT, underline: {} })] }),
        ],
      }),
      new Paragraph({
        spacing: sp(0, 0),
        alignment: AlignmentType.CENTER,
        children: [
          new ExternalHyperlink({ link: "https://github.com/denzelchingodza", children: [new TextRun({ text: "github.com/denzelchingodza", size: 18, font: "Calibri", color: ACCENT, underline: {} })] }),
          new TextRun({ text: "   |   ", size: 18, font: "Calibri", color: MUTED }),
          new ExternalHyperlink({ link: "https://platform-nine-ochre.vercel.app", children: [new TextRun({ text: "platform-nine-ochre.vercel.app", size: 18, font: "Calibri", color: ACCENT, underline: {} })] }),
        ],
      }),

      rule(),

      // ── PROFESSIONAL SUMMARY ──────────────────────────────
      sectionHeading("PROFESSIONAL SUMMARY"),
      new Paragraph({
        spacing: sp(80, 0),
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "Final-year BSc Information Technology (Software Engineering) student at Eduvos, Cape Town, with hands-on experience designing and deploying AI and machine learning systems. I built a production RAG (Retrieval-Augmented Generation) pipeline from scratch — covering data ingestion, text embedding, vector similarity search, and language model integration — and deployed it as a live application used by real users. I learn fastest through building real things, and I am actively seeking an ML internship where I can apply and deepen my understanding of machine learning techniques alongside experienced professionals.",
          size: 19, font: "Calibri", color: BLACK,
        })],
      }),

      rule(),

      // ── TECHNICAL SKILLS ──────────────────────────────────
      sectionHeading("TECHNICAL SKILLS"),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [1800, 7560],
        rows: [
          skillRow("Languages",       "Python · TypeScript · JavaScript · SQL · HTML · CSS"),
          skillRow("ML / AI",         "RAG pipelines · Text embeddings · Cosine similarity search · Vector databases · OpenAI API (GPT-4o-mini, text-embedding-3-small) · Prompt engineering"),
          skillRow("Data & ML Libs",  "pgvector · tiktoken · PyMuPDF · SQLAlchemy (async) · Pandas · NumPy"),
          skillRow("Frameworks",      "FastAPI · Next.js · React · Tailwind CSS"),
          skillRow("Databases",       "PostgreSQL · MongoDB · DynamoDB · Neon (serverless Postgres)"),
          skillRow("Cloud & DevOps",  "AWS Lambda · EventBridge · SES · DynamoDB · Terraform · Docker · GitHub Actions · Vercel · Render"),
          skillRow("Tools",           "Git · GitHub · Jupyter · Linux · VS Code"),
        ],
      }),

      rule(),

      // ── ML / AI PROJECT EXPERIENCE ────────────────────────
      sectionHeading("MACHINE LEARNING & AI PROJECT EXPERIENCE"),

      // DocuZen — the headline ML project
      jobHeader("DocuZen — AI-Powered Document Intelligence System", "Personal Project", "2025 – Present"),
      new Paragraph({
        spacing: sp(40, 0),
        children: [
          new TextRun({ text: "Live: ", size: 18, font: "Calibri", color: MUTED }),
          new ExternalHyperlink({ link: "https://docuzen.netlify.app", children: [new TextRun({ text: "docuzen.netlify.app", size: 18, font: "Calibri", color: ACCENT, underline: {} })] }),
          new TextRun({ text: "  (password: docuzen2026)   ·   github.com/denzelchingodza/doc-analyzer", size: 18, font: "Calibri", color: MUTED }),
        ],
      }),
      bullet("Designed and implemented a full Retrieval-Augmented Generation (RAG) pipeline end-to-end: document ingestion (PDF/DOCX via PyMuPDF), token-aware chunking with tiktoken, generation of text embeddings via the OpenAI text-embedding-3-small model, and cosine-similarity semantic search using PostgreSQL pgvector."),
      bullet("Engineered the data pipeline to handle multi-format document ingestion, clean and preprocess raw text, split it into semantically meaningful chunks, and persist embeddings to a vector store — directly analogous to ML data preparation workflows."),
      bullet("Integrated GPT-4o-mini as the language model backbone: constructed retrieval-augmented prompts, managed context windows, and returned precise answers with page-level citations — demonstrating practical experience with LLM APIs and prompt engineering."),
      bullet("Deployed a FastAPI backend (async Python, SQLAlchemy ORM) on Docker/Render connected to a Neon serverless PostgreSQL database with the pgvector extension for approximate nearest-neighbour search."),
      bullet("Communicated findings and system design clearly in documentation and code — all logic commented and structured for maintainability."),
      bullet("Stack: Python · FastAPI · PostgreSQL · pgvector · OpenAI API · Docker · Next.js · TypeScript"),

      // Sentinel — cloud / data systems
      jobHeader("Sentinel — Serverless Monitoring & Data Pipeline", "Personal Project", "2025 – Present"),
      new Paragraph({
        spacing: sp(40, 0),
        children: [
          new TextRun({ text: "Live: ", size: 18, font: "Calibri", color: MUTED }),
          new ExternalHyperlink({ link: "https://sentinel-kappa-wine.vercel.app", children: [new TextRun({ text: "sentinel-kappa-wine.vercel.app", size: 18, font: "Calibri", color: ACCENT, underline: {} })] }),
          new TextRun({ text: "   ·   github.com/denzelchingodza/sentinel", size: 18, font: "Calibri", color: MUTED }),
        ],
      }),
      bullet("Built a cloud-native data collection pipeline: AWS Lambda functions trigger via EventBridge every 60 seconds, collect uptime and response-time data from monitored endpoints, and persist structured records to DynamoDB — a real-time time-series data ingestion system."),
      bullet("Designed a DynamoDB schema optimised for querying historical metrics — directly applicable to data warehousing and data modelling concepts."),
      bullet("Provisioned all infrastructure as code with Terraform, demonstrating cloud platform proficiency (AWS) beyond tutorial level."),
      bullet("Stack: Next.js · AWS Lambda · DynamoDB · EventBridge · SES · Terraform"),

      rule(),

      // ── OTHER PROJECTS ────────────────────────────────────
      sectionHeading("OTHER PROJECTS"),

      jobHeader("DenzOS — Interactive Portfolio Platform", "Personal Project", "2025 – Present"),
      bullet("Built a Next.js/TypeScript portfolio platform with custom Canvas API animations and orbital system visualisations — no UI libraries, all logic written from scratch."),
      bullet("Live at platform-nine-ochre.vercel.app"),

      jobHeader("LinkUP — Peer-to-Peer Marketplace", "Academic / Personal Project", "2026"),
      bullet("Full-stack e-commerce platform with user authentication, product listings, cart, and admin controls. Python FastAPI backend connected to MongoDB. Live at ecommerce-seven-iota-31.vercel.app"),

      rule(),

      // ── EDUCATION ─────────────────────────────────────────
      sectionHeading("EDUCATION"),
      jobHeader("BSc Information Technology — Software Engineering", "Eduvos, Cape Town", "2022 – Present"),
      new Paragraph({
        spacing: sp(40, 0),
        children: [new TextRun({ text: "Expected graduation: 2026  ·  Final year  ·  Full-time", size: 19, font: "Calibri", color: MUTED, italic: true })],
      }),
      bullet("Relevant coursework: Data Structures and Algorithms, Software Engineering, Database Systems, Operating Systems, Computer Networks, Object-Oriented Programming."),
      bullet("Independently built and deployed AI/ML systems alongside full-time studies, applying academic concepts to real-world problems beyond the coursework scope."),

      rule(),

      // ── WHY TRAVELSTART ────────────────────────────────────
      sectionHeading("WHY I AM A FIT FOR THIS ROLE"),
      bullet("Practical ML experience: I have built and deployed a production RAG system covering data ingestion, embedding, vector search, and LLM integration — not just coursework theory."),
      bullet("Python-first: all backend and ML work is in Python (FastAPI, async SQLAlchemy, PyMuPDF, tiktoken, OpenAI SDK) — the primary ML language listed in the role requirements."),
      bullet("Cloud-ready: hands-on AWS experience (Lambda, DynamoDB, EventBridge, SES) and infrastructure-as-code with Terraform aligns directly with the cloud platform preference."),
      bullet("Fast learner: every tool I use — embeddings, vector databases, serverless infrastructure — was self-taught through building. I pick up new ML libraries and frameworks quickly when there is a real problem to solve."),
      bullet("Team-oriented: comfortable working independently and contributing to cross-functional teams, with clear written communication in documentation and code."),

      rule(),

      new Paragraph({
        spacing: sp(80, 0),
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "References available on request  ·  All projects live at platform-nine-ochre.vercel.app", size: 17, font: "Calibri", color: MUTED, italic: true })],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/sessions/hopeful-inspiring-heisenberg/mnt/ecommerce/denzel-chingodza-cv-travelstart.docx", buf);
  console.log("done");
});
