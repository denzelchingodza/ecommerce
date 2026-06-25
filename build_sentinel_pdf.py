#!/usr/bin/env python3
"""Sentinel Backend Deep-Dive PDF generator."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUT = "/sessions/hopeful-inspiring-heisenberg/mnt/ecommerce/Sentinel_Backend_Deep_Dive.pdf"
W, H = A4
ML = MR = 20*mm
MT = MB = 18*mm

C_NAVY   = colors.HexColor("#0A2342")
C_BLUE   = colors.HexColor("#1565C0")
C_TEAL   = colors.HexColor("#00695C")
C_AMBER  = colors.HexColor("#E65100")
C_PURPLE = colors.HexColor("#6A1B9A")
C_GREEN  = colors.HexColor("#2E7D32")
C_CODE   = colors.HexColor("#1E2A3A")
C_BG_ALT = colors.HexColor("#E3F2FD")
C_BG_NOTE= colors.HexColor("#FFF3E0")
C_BG_GOOD= colors.HexColor("#E8F5E9")
C_LIGHT  = colors.HexColor("#F5F5F5")
C_LINE   = colors.HexColor("#1565C0")
C_WHITE  = colors.white
C_BLACK  = colors.black
C_GRAY   = colors.HexColor("#546E7A")
C_FG     = colors.HexColor("#CDD6F4")

def S(name, **kw): return ParagraphStyle(name, **kw)

sTitle  = S("Title", fontName="Helvetica-Bold", fontSize=28, leading=34, textColor=C_NAVY, spaceAfter=6, alignment=TA_CENTER)
sSubT   = S("SubT",  fontName="Helvetica",      fontSize=14, leading=18, textColor=C_BLUE, spaceAfter=4, alignment=TA_CENTER)
sLabel  = S("Label", fontName="Helvetica",      fontSize=10, leading=13, textColor=C_GRAY, alignment=TA_CENTER)
sH1     = S("H1",    fontName="Helvetica-Bold", fontSize=17, leading=22, textColor=C_NAVY, spaceBefore=18, spaceAfter=6)
sH2     = S("H2",    fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=C_BLUE, spaceBefore=14, spaceAfter=4)
sH3     = S("H3",    fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=C_TEAL, spaceBefore=10, spaceAfter=3)
sBody   = S("Body",  fontName="Helvetica",      fontSize=10, leading=16, textColor=C_BLACK, spaceAfter=6, alignment=TA_JUSTIFY)
sBodyL  = S("BodyL", fontName="Helvetica",      fontSize=10, leading=16, textColor=C_BLACK, spaceAfter=6)
sBullet = S("Bullet",fontName="Helvetica",      fontSize=10, leading=15, textColor=C_BLACK, leftIndent=14, spaceAfter=3, bulletIndent=4)
sCode   = S("Code",  fontName="Courier",        fontSize=8.5, leading=13, textColor=C_FG, backColor=C_CODE, leftIndent=8, rightIndent=8, spaceAfter=2, spaceBefore=2)
sCodeL  = S("CodeL", fontName="Courier",        fontSize=8.5, leading=13, textColor=C_BLACK, leftIndent=8, spaceAfter=2, spaceBefore=2)
sAlt    = S("Alt",   fontName="Helvetica",      fontSize=9.5, leading=14, textColor=C_BLACK, spaceAfter=3, leftIndent=8)
sSmall  = S("Small", fontName="Helvetica",      fontSize=8.5, leading=12, textColor=C_GRAY)
sCaption= S("Cap",   fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=C_GRAY, alignment=TA_CENTER, spaceAfter=8)

def hr(color=C_LINE, w=1.5): return HRFlowable(width="100%", thickness=w, color=color, spaceAfter=6, spaceBefore=4)
def sp(h=6): return Spacer(1, h)
def P(text, style=None): return Paragraph(text, style or sBody)
def B(text): return Paragraph(f"<bullet>•</bullet> {text}", sBullet)

def code_block(lines, dark=True):
    st = sCode if dark else sCodeL
    bg = C_CODE if dark else C_LIGHT
    cells = [[Paragraph(l.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), st)] for l in lines]
    t = Table(cells, colWidths=[W-ML-MR-4])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
    return t

def info_box(title, lines, bg=C_BG_ALT, tc=C_BLUE):
    rows = [[Paragraph(f"<b>{title}</b>", S("h",fontName="Helvetica-Bold",fontSize=10,leading=14,textColor=tc))]]
    rows += [[Paragraph(l, sAlt)] for l in lines]
    t = Table(rows, colWidths=[W-ML-MR-4])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("BOX",(0,0),(-1,-1),1,tc),("LINEBELOW",(0,0),(-1,0),0.5,tc),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
    return t

def alt_box(chosen, why, alts):
    rows = [[P("<b>We used:</b>",sAlt), P(f"<b>{chosen}</b>",S("g",fontName="Helvetica-Bold",fontSize=10,leading=14,textColor=C_GREEN))],[P("<b>Why:</b>",sAlt),P(why,sAlt)],[P("<b>Alternatives:</b>",sAlt),P(alts,sAlt)]]
    t = Table(rows, colWidths=[(W-ML-MR-4)*0.22,(W-ML-MR-4)*0.78])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_BG_GOOD),("BOX",(0,0),(-1,-1),1,C_GREEN),("LINEAFTER",(0,0),(0,-1),0.5,C_GREEN),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"TOP")]))
    return t

def watch_box(resources):
    rows = [[P("<b>Watch / Read to understand this concept:</b>",S("wh",fontName="Helvetica-Bold",fontSize=9.5,leading=13,textColor=C_PURPLE))]]
    rows += [[P(f"  ▶  {r}",S("wr",fontName="Helvetica",fontSize=9,leading=13,textColor=C_PURPLE))] for r in resources]
    t = Table(rows, colWidths=[W-ML-MR-4])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F3E5F5")),("BOX",(0,0),(-1,-1),1,C_PURPLE),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
    return t

def diagram_box(title, lines):
    rows = [[P(f"<b>{title}</b>",S("dh",fontName="Courier-Bold",fontSize=9.5,leading=13,textColor=C_WHITE))]]
    rows += [[P(f"  {l}".replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"),S("dl",fontName="Courier",fontSize=9,leading=13,textColor=C_FG))] for l in lines]
    t = Table(rows, colWidths=[W-ML-MR-4])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),C_CODE),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0D1B2A")),("BOX",(0,0),(-1,-1),1,C_LINE),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12)]))
    return t

story = []

# COVER
story += [sp(60), P("Sentinel", sTitle), sp(4), P("Backend Deep-Dive", sSubT), sp(2),
    P("A complete technical reference — every file, every AWS service, every Terraform resource,", sLabel),
    P("why each was used, what else could have been used, and what to study to understand it fully.", sLabel),
    sp(30), HRFlowable(width="100%", thickness=2, color=C_NAVY, spaceAfter=8), sp(8),
    P("Written for: Denzel Chingodza", sSmall), sp(2),
    P("Project: Sentinel — Serverless Uptime Monitoring System", sSmall), sp(2),
    P("Stack: AWS Lambda  |  DynamoDB  |  EventBridge  |  SES  |  API Gateway  |  IAM  |  Terraform  |  Node.js", sSmall),
    PageBreak()]

# TOC
story += [P("Contents", sH1), hr(), sp(4)]
toc = [
    ("1.", "How Sentinel Works — The Big Picture", "3"),
    ("2.", "Concept: Serverless Architecture", "4"),
    ("3.", "File: lambda/functions/monitor/index.js", "6"),
    ("4.", "File: lambda/functions/api/index.js", "11"),
    ("5.", "File: terraform/modules/dynamodb/main.tf", "14"),
    ("6.", "File: terraform/modules/lambda/main.tf", "17"),
    ("7.", "File: terraform/modules/eventbridge/main.tf", "20"),
    ("8.", "File: terraform/modules/ses/main.tf", "22"),
    ("9.", "File: terraform/modules/api_gateway/main.tf", "24"),
    ("10.", "File: terraform/main.tf — Root Orchestration", "26"),
    ("11.", "Concept Deep-Dive: IAM — Identity and Access Management", "27"),
    ("12.", "Concept Deep-Dive: DynamoDB Data Modelling", "29"),
    ("13.", "Concept Deep-Dive: Infrastructure as Code", "31"),
    ("14.", "Concept Deep-Dive: HTTP, CORS, and the Event Object", "33"),
    ("15.", "Quick Reference — AWS Services & Technology Choices", "35"),
]
tdata = [[P(a,sBodyL),P(b,sBodyL),P(c,sBodyL)] for a,b,c in toc]
tt = Table(tdata, colWidths=[20,(W-ML-MR-4-20-30),30])
tt.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("ALIGN",(2,0),(2,-1),"RIGHT")]))
story += [tt, PageBreak()]

# 1. BIG PICTURE
story += [P("1. How Sentinel Works — The Big Picture", sH1), hr(), sp(4)]
story += [P("""Sentinel is a serverless uptime monitoring system. You add a URL to monitor through the dashboard. Every 60 seconds, an automated system checks if that URL is responding correctly. If it goes down, you get an email immediately. When it comes back up, you get another email. The dashboard shows you real-time status, response times, and uptime percentage.""", sBody)]
story += [sp(6), diagram_box("Sentinel Full System Architecture", [
    "USER ACTION: 'Monitor this URL'",
    "  |",
    "  v",
    "  Next.js Dashboard  -->  POST /monitors  -->  API Gateway",
    "                                                    |",
    "                                                    v",
    "                                             sentinel_api (Lambda)",
    "                                                    |",
    "                                                    v",
    "                                             DynamoDB: sentinel_monitors",
    "",
    "EVERY 60 SECONDS (automated):",
    "  EventBridge (cron: rate(1 minute))",
    "         |",
    "         v",
    "  sentinel_monitor (Lambda) -- runs automatically, no user action",
    "         |",
    "         |-- fetches all active monitors from DynamoDB",
    "         |-- pings each URL (HTTP GET, 10s timeout)",
    "         |-- stores check result in DynamoDB: sentinel_checks",
    "         |-- if DOWN: creates incident in sentinel_incidents",
    "         |            sends email via SES",
    "         |-- if UP after DOWN: resolves incident, sends recovery email via SES",
    "",
    "USER ACTION: 'Show me my dashboard'",
    "  Next.js Dashboard  -->  GET /monitors  -->  API Gateway  -->  sentinel_api  -->  DynamoDB",
]), sp(8)]

# 2. SERVERLESS
story += [P("2. Concept: Serverless Architecture", sH1), hr(), sp(4)]
story += [P("""'Serverless' does not mean there are no servers. It means you do not manage servers. AWS runs your code on their servers, handles scaling automatically, and you pay only for the milliseconds your code actually runs. When nothing is happening, you pay nothing.""", sBody)]
story += [P("Traditional Server vs Serverless — The Key Difference", sH2)]
story += [diagram_box("Traditional Server vs AWS Lambda", [
    "TRADITIONAL SERVER (e.g., a VPS on DigitalOcean):",
    "  - You rent a server: R400/month regardless of traffic",
    "  - Server is always on, always consuming resources",
    "  - You manage: OS updates, security patches, scaling",
    "  - If traffic spikes: manually add more servers",
    "  - If server crashes: you fix it",
    "",
    "AWS LAMBDA (Sentinel's approach):",
    "  - No server to manage",
    "  - Code only runs when triggered (EventBridge every 60s, or API call)",
    "  - Billing: $0.20 per million invocations + $0.0000166667 per GB-second",
    "  - Sentinel runs ~43,200 times/month (60x24x30) -> costs cents",
    "  - AWS handles scaling: 1000 concurrent executions auto-supported",
    "  - If code fails: AWS logs it, Lambda retries automatically",
])]
story += [sp(6), P("Lambda Cold Starts", sH2)]
story += [P("""When a Lambda function hasn't been called recently, AWS has to initialise a new execution environment (download your code, start the Node.js runtime, etc.). This takes 100-500ms and is called a 'cold start'. Subsequent calls in the same environment are fast ('warm starts'). For Sentinel, this is fine — the monitor Lambda runs every 60 seconds so it's always warm. The API Lambda has occasional cold starts but they are acceptable for a monitoring dashboard.""", sBody)]
story += [sp(4), alt_box("AWS Lambda", "No infrastructure management, scales automatically, very cheap for periodic workloads, integrates natively with all AWS services.", "EC2 (virtual machine — you manage everything). ECS/Fargate (Docker containers on AWS — more control, more cost). Google Cloud Functions (same concept, Google's cloud). Azure Functions (same concept, Microsoft's cloud). Self-hosted server on Render/Railway (simpler setup but always-on cost).")]
story += [sp(6), watch_box(["YouTube: 'AWS Lambda explained in 15 minutes' — search 'AWS Lambda tutorial beginner 2024'", "YouTube: 'Serverless computing explained' — search 'serverless computing explained simply'", "YouTube: 'AWS Lambda cold starts explained' — search 'Lambda cold start problem solutions'"]), PageBreak()]

# 3. MONITOR LAMBDA
story += [P("3. File: lambda/functions/monitor/index.js", sH1), hr()]
story += [P("""This is the most important file in Sentinel. It runs every 60 seconds, triggered by EventBridge. It checks every monitored URL, records the result, and sends email alerts when things go wrong.""", sBody)]
story += [P("Imports and Setup", sH2)]
story += [code_block([
    "const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');",
    "const { DynamoDBDocumentClient, ScanCommand, PutCommand,",
    "        QueryCommand, UpdateCommand } = require('@aws-sdk/lib-dynamodb');",
    "const { SESClient, SendEmailCommand } = require('@aws-sdk/client-ses');",
    "const https = require('https');   // Node.js built-in for HTTPS requests",
    "const http  = require('http');    // Node.js built-in for HTTP requests",
    "const { randomUUID } = require('crypto');  // Built-in UUID generator",
    "",
    "const dynamo = DynamoDBDocumentClient.from(new DynamoDBClient({}));",
    "// DynamoDBClient: low-level AWS SDK. DynamoDBDocumentClient: wrapper that",
    "// auto-converts JavaScript types (numbers, strings, booleans) to DynamoDB's",
    "// internal format and back. Always use DocumentClient — it saves you pain.",
    "",
    "const ses = new SESClient({ region: 'af-south-1' });",
    "",
    "const LATENCY_THRESHOLD_MS = 5000;  // If response > 5s, treat as unhealthy",
    "const COOLDOWN_MINUTES = 30;         // Don't spam repeat alerts",
])]
story += [sp(6), P("The ping() Function", sH2)]
story += [P("""This function hits a URL and measures how long it takes to respond. It returns the HTTP status code, response time in milliseconds, and any error message.""", sBody)]
story += [code_block([
    "function ping(url) {",
    "  return new Promise((resolve) => {",
    "    const start = Date.now();   // Timestamp before request",
    "    const lib = url.startsWith('https') ? https : http;  // Pick the right module",
    "",
    "    const req = lib.get(url, { timeout: 10000 }, (res) => {",
    "      res.resume();  // Consume response body (required to free the connection)",
    "      resolve({",
    "        statusCode: res.statusCode,           // e.g. 200, 404, 500",
    "        responseTime: Date.now() - start,     // milliseconds elapsed",
    "        error: null",
    "      });",
    "    });",
    "",
    "    req.on('error', (err) => resolve({ statusCode: 0, responseTime: Date.now() - start, error: err.message }));",
    "    req.on('timeout', () => { req.destroy(); resolve({ statusCode: 0, responseTime: Date.now() - start, error: 'timeout' }); });",
    "  });",
    "}",
])]
story += [sp(6), P("What Is a Promise?", sH2)]
story += [P("""In JavaScript, many operations (network requests, file reads) are asynchronous — they take time and you don't want to block. A Promise represents a value that will be available in the future. You `await` it to pause until it resolves. The `new Promise((resolve) => {...})` pattern wraps a callback-based API (Node's http.get) into a Promise that async/await can understand.""", sBody)]
story += [info_box("Promise States", [
    "Pending: the operation is in progress (e.g. waiting for HTTP response)",
    "Fulfilled: the operation completed successfully -> resolve(value) was called",
    "Rejected: the operation failed -> reject(error) was called",
    "await a promise: pauses execution until it fulfills or rejects",
    "Promise.all([p1, p2, p3]): run all three in parallel, wait for all to finish",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), P("The Main Handler", sH2)]
story += [code_block([
    "exports.handler = async () => {",
    "  // 1. Fetch all active monitors from DynamoDB",
    "  const { Items: monitors = [] } = await dynamo.send(new ScanCommand({",
    "    TableName: MONITORS_TABLE,",
    "    FilterExpression: 'active = :a',",
    "    ExpressionAttributeValues: { ':a': true },",
    "  }));",
    "",
    "  // 2. Check ALL monitors in parallel (Promise.all)",
    "  await Promise.all(monitors.map(async (monitor) => {",
    "    const { statusCode, responseTime, error } = await ping(monitor.url);",
    "    const healthy = statusCode >= 200 && statusCode < 400",
    "                    && responseTime < LATENCY_THRESHOLD_MS;",
    "    const timestamp = new Date().toISOString();",
    "",
    "    // 3. Store check result",
    "    await dynamo.send(new PutCommand({",
    "      TableName: CHECKS_TABLE,",
    "      Item: { id: randomUUID(), monitorId: monitor.id, url: monitor.url,",
    "              statusCode, responseTime, healthy, timestamp },",
    "    }));",
    "",
    "    // 4. Update monitor's last known status",
    "    await dynamo.send(new UpdateCommand({",
    "      TableName: MONITORS_TABLE,",
    "      Key: { id: monitor.id },",
    "      UpdateExpression: 'SET lastStatus = :s, lastChecked = :t, lastResponseTime = :r',",
    "      ExpressionAttributeValues: { ':s': healthy ? 'up' : 'down', ':t': timestamp, ':r': responseTime },",
    "    }));",
    "",
    "    // 5. Handle alerts (see incident logic below)",
    "    if (!healthy) { /* ... incident + alert logic */ }",
    "    else          { /* ... recovery logic */ }",
    "  }));",
    "};",
])]
story += [sp(6), P("Why Promise.all?", sH2)]
story += [P("""If you have 10 monitors and check them one by one (await ping(url1), then await ping(url2)...), and each ping takes up to 10 seconds, the Lambda could take 100 seconds total. With Promise.all, all 10 pings run concurrently. If each takes 2 seconds, Promise.all finishes in 2 seconds total. This is critical because the Lambda has a 30-second timeout.""", sBody)]
story += [P("The Healthy Definition", sH2)]
story += [code_block([
    "const healthy = statusCode >= 200 && statusCode < 400",
    "                && responseTime < LATENCY_THRESHOLD_MS;",
    "",
    "// statusCode >= 200 && < 400 means:",
    "// 200 OK, 201 Created, 301 Redirect, 304 Not Modified -> healthy",
    "// 400 Bad Request, 404 Not Found, 500 Server Error -> unhealthy",
    "// 0 -> connection failed entirely (DNS error, refused, timeout) -> unhealthy",
    "",
    "// LATENCY_THRESHOLD_MS = 5000",
    "// Even if a site responds 200, if it takes > 5 seconds, it's treated as unhealthy",
    "// This catches degraded performance, not just complete outages",
], dark=False)]
story += [sp(6), P("Incident Logic — Down Detection", sH2)]
story += [code_block([
    "if (!healthy) {",
    "  // Query for open incidents for this monitor",
    "  const { Items: incidents = [] } = await dynamo.send(new QueryCommand({",
    "    TableName: INCIDENTS_TABLE,",
    "    IndexName: 'monitorId-index',         // Use the GSI for fast lookup",
    "    KeyConditionExpression: 'monitorId = :m',",
    "    FilterExpression: 'resolved = :r',",
    "    ExpressionAttributeValues: { ':m': monitor.id, ':r': false },",
    "  }));",
    "",
    "  if (incidents.length === 0) {",
    "    // First time this monitor is down -> create incident + send alert",
    "    await dynamo.send(new PutCommand({ TableName: INCIDENTS_TABLE, Item: { ... } }));",
    "    await sendAlert(monitor, 'down', { statusCode, responseTime, error });",
    "  } else {",
    "    // Already have an open incident -> only re-alert after COOLDOWN_MINUTES (30)",
    "    const lastAlert = new Date(incidents[0].lastAlertTime).getTime();",
    "    if (Date.now() - lastAlert > 30 * 60 * 1000) {",
    "      await sendAlert(monitor, 'down', { ... });  // Reminder alert",
    "    }",
    "  }",
    "}",
])]
story += [sp(4), P("The Cooldown Logic — Why It Matters", sH2)]
story += [P("""Without a cooldown, if your site stays down for 2 hours, you'd receive 120 emails (one per minute). The 30-minute cooldown means you get one alert when it goes down, and another every 30 minutes if it stays down. Much more reasonable.""", sBody)]
story += [P("Recovery Logic", sH2)]
story += [code_block([
    "else {  // healthy == true",
    "  // Check if we're recovering from an incident",
    "  const { Items: incidents = [] } = await dynamo.send(new QueryCommand({",
    "    ... filtered by monitorId and resolved = false",
    "  }));",
    "",
    "  if (incidents.length > 0) {",
    "    // Site was down, now it's up -> resolve the incident",
    "    const duration = Math.round((Date.now() - new Date(incident.startTime)) / 1000 / 60);",
    "    await dynamo.send(new UpdateCommand({",
    "      ... SET resolved = true, endTime = now",
    "    }));",
    "    await sendAlert(monitor, 'recovery', { statusCode, responseTime,",
    "                                           duration: `${duration} minutes` });",
    "  }",
    "}",
])]
story += [sp(6), alt_box("Node.js https.get (native)", "Zero dependencies, always available in Lambda runtime, lightweight.", "axios (popular HTTP client, cleaner API but adds a dependency). node-fetch (fetch API for Node.js). got (feature-rich HTTP client). Superagent.")]
story += [sp(6), watch_box(["YouTube: 'JavaScript Promises explained' — search 'JavaScript promises async await tutorial'", "YouTube: 'Promise.all vs Promise.allSettled' — search 'promise all javascript explained'", "MDN Web Docs: 'Using Promises' — developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises", "YouTube: 'HTTP status codes explained' — search 'HTTP status codes 200 404 500 explained'"]), PageBreak()]

# 4. API LAMBDA
story += [P("4. File: lambda/functions/api/index.js", sH1), hr()]
story += [P("""This Lambda function serves as the REST API backend for the dashboard. It handles all CRUD (Create, Read, Delete) operations on monitors, plus reading check history, analytics, and incidents.""", sBody)]
story += [code_block([
    "exports.handler = async (event) => {",
    "  const method = event.httpMethod;   // 'GET', 'POST', 'DELETE', 'OPTIONS'",
    "  const path   = event.path;          // '/monitors', '/monitors/abc-123'",
    "  const body   = event.body ? JSON.parse(event.body) : {};",
    "",
    "  // OPTIONS: browser sends this before every cross-origin request (CORS preflight)",
    "  if (method === 'OPTIONS') return response(200, {});",
    "",
    "  // Manual routing — no Express framework",
    "  if (method === 'POST' && path === '/monitors') {",
    "    // Register a new monitor",
    "    const { url, name } = body;",
    "    const monitor = { id: randomUUID(), url, name, active: true, ... };",
    "    await dynamo.send(new PutCommand({ TableName: MONITORS_TABLE, Item: monitor }));",
    "    return response(201, monitor);",
    "  }",
    "",
    "  if (method === 'GET' && path === '/monitors') {",
    "    const { Items = [] } = await dynamo.send(new ScanCommand({ TableName: MONITORS_TABLE }));",
    "    return response(200, Items);",
    "  }",
    "",
    "  if (method === 'DELETE' && path.startsWith('/monitors/')) {",
    "    const id = path.split('/')[2];",
    "    await dynamo.send(new DeleteCommand({ TableName: MONITORS_TABLE, Key: { id } }));",
    "    return response(200, { message: 'Monitor deleted' });",
    "  }",
    "",
    "  // GET /monitors/{id}/history  ->  last N check results",
    "  // GET /monitors/{id}/analytics ->  uptime %, avg response time",
    "  // GET /incidents               ->  active (unresolved) incidents",
    "  // GET /incidents/all           ->  all incidents",
    "};",
])]
story += [sp(6), P("The Event Object — API Gateway Lambda Proxy", sH2)]
story += [P("""When API Gateway invokes the Lambda, it passes an `event` object. This is API Gateway translating an HTTP request into a JSON object the Lambda can understand. Key fields:""", sBody)]
story += [info_box("API Gateway Event Object Structure", [
    "event.httpMethod    -> 'GET', 'POST', 'DELETE', 'OPTIONS'",
    "event.path          -> '/monitors', '/monitors/abc-123/history'",
    "event.body          -> JSON string of the request body (for POST/PUT)",
    "event.queryStringParameters -> { limit: '50' } from /history?limit=50",
    "event.headers       -> HTTP headers from the request",
    "event.pathParameters -> { id: 'abc-123' } if API Gateway extracts path vars",
    "                        (Sentinel uses manual path.split('/') instead)",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), P("The Analytics Endpoint", sH2)]
story += [code_block([
    "if (method === 'GET' && path.match(/^\\/monitors\\/[^\\/]+\\/analytics$/)) {",
    "  const id = path.split('/')[2];",
    "",
    "  // Fetch last 1440 checks (60 checks/hour * 24 hours = last 24 hours)",
    "  const { Items = [] } = await dynamo.send(new QueryCommand({",
    "    TableName: CHECKS_TABLE,",
    "    IndexName: 'monitorId-timestamp-index',",
    "    KeyConditionExpression: 'monitorId = :m',",
    "    ScanIndexForward: false,   // Most recent first",
    "    Limit: 1440,",
    "    ExpressionAttributeValues: { ':m': id },",
    "  }));",
    "",
    "  const total   = Items.length;",
    "  const up      = Items.filter(c => c.healthy).length;",
    "  const avgTime = Items.reduce((s, c) => s + c.responseTime, 0) / total;",
    "",
    "  return response(200, {",
    "    uptime: ((up / total) * 100).toFixed(2),   // e.g. '99.93'",
    "    avgResponseTime: Math.round(avgTime),",
    "    checksUp: up,",
    "    checksDown: total - up,",
    "  });",
    "}",
])]
story += [sp(6), P("The response() Helper Function", sH2)]
story += [code_block([
    "function response(statusCode, body) {",
    "  return {",
    "    statusCode,",
    "    headers: {",
    "      'Content-Type': 'application/json',",
    "      'Access-Control-Allow-Origin': '*',         // CORS: allow all origins",
    "      'Access-Control-Allow-Headers': 'Content-Type',",
    "      'Access-Control-Allow-Methods': 'GET,POST,DELETE,OPTIONS',",
    "    },",
    "    body: JSON.stringify(body),   // Lambda must return body as a string",
    "  };",
    "}",
    "",
    "// This is the Lambda Proxy Integration contract:",
    "// API Gateway passes raw events in, expects { statusCode, headers, body } out",
], dark=False)]
story += [sp(6), alt_box("Manual routing (if/else)", "No dependencies, completely transparent, works in Lambda's minimal environment.", "Express.js with aws-serverless-express (popular, familiar routing). Fastify (faster than Express, good Lambda support). Hono (modern, designed for edge/serverless). AWS SAM / Serverless Framework (higher-level abstractions).")]
story += [sp(6), watch_box(["YouTube: 'AWS API Gateway + Lambda tutorial' — search 'API Gateway Lambda proxy integration tutorial'", "YouTube: 'CRUD API with AWS Lambda and DynamoDB' — search 'lambda dynamodb rest api tutorial'", "AWS docs: 'Set up Lambda proxy integrations' — docs.aws.amazon.com"]), PageBreak()]

# 5. DYNAMODB
story += [P("5. File: terraform/modules/dynamodb/main.tf — DynamoDB Tables", sH1), hr()]
story += [P("""DynamoDB is AWS's managed NoSQL database. It stores all Sentinel data: the monitors you add, every check result, and every incident. DynamoDB is a key-value and document store — very different from the PostgreSQL relational database used in DocuZen.""", sBody)]
story += [P("The Three Tables", sH2)]
story += [code_block([
    "# Table 1: sentinel_monitors — one row per monitored URL",
    "resource 'aws_dynamodb_table' 'monitors' {",
    "  name         = 'sentinel_monitors'",
    "  billing_mode = 'PAY_PER_REQUEST'  # No capacity planning needed",
    "  hash_key     = 'id'               # Primary key = id (UUID string)",
    "  ...",
    "}",
    "",
    "# Table 2: sentinel_checks — one row per check (runs every 60s per monitor)",
    "resource 'aws_dynamodb_table' 'checks' {",
    "  name      = 'sentinel_checks'",
    "  hash_key  = 'id'         # Unique check ID",
    "  range_key = 'timestamp'  # Sort key — enables range queries by time",
    "",
    "  # Global Secondary Index: query checks by monitorId + timestamp",
    "  global_secondary_index {",
    "    name            = 'monitorId-timestamp-index'",
    "    hash_key        = 'monitorId'",
    "    range_key       = 'timestamp'",
    "    projection_type = 'ALL'   # Include all attributes in index",
    "  }",
    "}",
    "",
    "# Table 3: sentinel_incidents — one row per outage event",
    "resource 'aws_dynamodb_table' 'incidents' {",
    "  name     = 'sentinel_incidents'",
    "  hash_key = 'id'",
    "",
    "  global_secondary_index {",
    "    name     = 'monitorId-index'",
    "    hash_key = 'monitorId'   # Query incidents by monitorId",
    "  }",
    "}",
])]
story += [sp(6), P("DynamoDB Key Concepts", sH2)]
story += [P("<b>Hash Key (Partition Key):</b> The primary identifier. DynamoDB uses this to decide which physical partition (server) stores the item. Must be unique for GetItem/PutItem.", sBodyL)]
story += [P("<b>Range Key (Sort Key):</b> Combined with the hash key, forms a composite key. Items with the same hash key but different range keys can coexist. They are stored sorted by range key — enabling range queries ('give me all checks for this monitor between these times').", sBodyL)]
story += [P("<b>Global Secondary Index (GSI):</b> An extra index that lets you query by a different key. The checks table's primary key is `id` — you can look up a specific check by ID. But you often want 'all checks for monitor X'. Without a GSI, you'd have to scan the whole table (expensive). With the `monitorId-timestamp-index` GSI, DynamoDB maintains a separate index sorted by monitorId + timestamp — making this query fast and cheap.", sBodyL)]
story += [diagram_box("DynamoDB Table Structure — Visual", [
    "sentinel_monitors table:",
    "  PK: id (UUID)  |  name  |  url  |  active  |  lastStatus  |  lastChecked",
    "  'abc-123'      | 'API'  | 'https://api.com' | true | 'up' | '2026-06-01T...'",
    "  'def-456'      | 'Site' | 'https://site.com'| true | 'down'| '2026-06-01T...'",
    "",
    "sentinel_checks table:",
    "  PK: id (UUID) + SK: timestamp  |  monitorId  |  healthy  |  responseTime  |  statusCode",
    "  'chk-001' | '2026-06-01T12:00' | 'abc-123'  |  true     |  234           |  200",
    "  'chk-002' | '2026-06-01T12:01' | 'abc-123'  |  true     |  241           |  200",
    "",
    "  GSI 'monitorId-timestamp-index': allows query 'all checks for abc-123, newest first'",
    "",
    "sentinel_incidents table:",
    "  PK: id  |  monitorId  |  startTime  |  endTime  |  resolved  |  alertSent",
    "  'inc-1' | 'def-456'   | '12:05:00'  | '12:35:00'| true       | true",
    "  'inc-2' | 'def-456'   | '14:00:00'  | null      | false      | true  <- open",
    "",
    "  GSI 'monitorId-index': allows query 'open incidents for def-456'",
])]
story += [sp(6), P("NoSQL vs SQL — The Trade-offs", sH2)]
story += [info_box("When DynamoDB Makes Sense vs When It Doesn't", [
    "DynamoDB is GREAT when:",
    "  - You know your access patterns upfront (query by monitorId, query by id)",
    "  - You need infinite scale without configuration",
    "  - Your data is simple key-value or document shaped",
    "  - Cost matters (PAY_PER_REQUEST = pay per query, not per server)",
    "",
    "DynamoDB is HARD when:",
    "  - You need flexible queries (SQL WHERE clauses with many conditions)",
    "  - You need joins across tables (DynamoDB has no JOIN — each query = one table)",
    "  - You need transactions across multiple tables (supported but complex)",
    "  - Your access patterns change frequently (redesigning = expensive rework)",
], bg=C_BG_NOTE, tc=C_AMBER)]
story += [sp(6), alt_box("DynamoDB", "Managed, serverless, millisecond performance at any scale, integrates natively with Lambda (same AWS account = no auth config).", "Aurora Serverless (MySQL/PostgreSQL on AWS — relational, more flexible queries, slightly more complex). MongoDB Atlas (managed NoSQL document DB). Firebase Realtime Database / Firestore (Google Cloud, simpler for small projects). Redis (in-memory, super fast, for caching or simple data).")]
story += [sp(6), watch_box(["YouTube: 'DynamoDB explained in 15 minutes' — search 'DynamoDB tutorial beginner explained'", "YouTube: 'DynamoDB Primary Keys, GSI, LSI explained' — search 'DynamoDB partition key sort key GSI'", "YouTube: 'NoSQL vs SQL' — search 'NoSQL vs SQL when to use which'", "AWS docs: 'Best practices for designing DynamoDB tables' — docs.aws.amazon.com"]), PageBreak()]

# 6. LAMBDA TERRAFORM
story += [P("6. File: terraform/modules/lambda/main.tf — Lambda Deployment", sH1), hr()]
story += [P("""This Terraform file creates both Lambda functions, the IAM role they run as, and the policies that define what they are allowed to do. It also packages the JavaScript code into ZIP files for deployment.""", sBody)]
story += [P("IAM Role and Policy — Permissions", sH2)]
story += [code_block([
    "# IAM Role: what service can assume this role (execute as this identity)",
    "resource 'aws_iam_role' 'lambda_role' {",
    "  name = 'sentinel_lambda_role'",
    "  assume_role_policy = jsonencode({",
    "    Statement = [{",
    "      Action    = 'sts:AssumeRole'",
    "      Principal = { Service = 'lambda.amazonaws.com' }  # Lambda service only",
    "    }]",
    "  })",
    "}",
    "",
    "# IAM Policy: what actions this role can perform",
    "resource 'aws_iam_role_policy' 'lambda_policy' {",
    "  policy = jsonencode({",
    "    Statement = [",
    "      {",
    "        Effect = 'Allow'",
    "        Action = ['dynamodb:PutItem', 'dynamodb:GetItem', 'dynamodb:UpdateItem',",
    "                  'dynamodb:DeleteItem', 'dynamodb:Query', 'dynamodb:Scan']",
    "        Resource = [monitors_arn, checks_arn, incidents_arn, '*/index/*']",
    "      },",
    "      {",
    "        Effect   = 'Allow'",
    "        Action   = ['ses:SendEmail', 'ses:SendRawEmail']",
    "        Resource = '*'",
    "      },",
    "      {",
    "        Effect = 'Allow'",
    "        Action = ['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents']",
    "        Resource = 'arn:aws:logs:*:*:*'",
    "      }",
    "    ]",
    "  })",
    "}",
])]
story += [sp(6), P("Packaging Code with archive_file", sH2)]
story += [code_block([
    "# Terraform zips your code automatically before deploying",
    "data 'archive_file' 'monitor' {",
    "  type        = 'zip'",
    "  source_dir  = '../lambda/functions/monitor'   # Your JS files",
    "  output_path = '../lambda/zips/monitor.zip'    # Output ZIP",
    "}",
    "",
    "resource 'aws_lambda_function' 'monitor' {",
    "  filename         = data.archive_file.monitor.output_path",
    "  function_name    = 'sentinel_monitor'",
    "  role             = aws_iam_role.lambda_role.arn",
    "  handler          = 'index.handler'   # file.exportedFunction",
    "  runtime          = 'nodejs20.x'      # Node.js 20",
    "  timeout          = 30                # Max 30 seconds to run",
    "  source_code_hash = data.archive_file.monitor.output_base64sha256",
    "  # source_code_hash: if code hasn't changed, Lambda doesn't re-deploy",
    "",
    "  environment {",
    "    variables = {",
    "      MONITORS_TABLE  = var.monitors_table_name   # Pass table names at deploy time",
    "      ALERT_EMAIL     = var.alert_email",
    "    }",
    "  }",
    "}",
])]
story += [sp(6), info_box("Why Environment Variables in Lambda?", [
    "Lambda functions should not have hardcoded configuration.",
    "Environment variables are set at deploy time by Terraform and available at runtime.",
    "This way, the same code can be deployed to different environments (dev, prod)",
    "without changing any code — just change the Terraform variables.",
    "In Node.js: process.env.MONITORS_TABLE reads the value.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), watch_box(["YouTube: 'AWS IAM explained simply' — search 'AWS IAM roles policies explained beginner'", "YouTube: 'Deploy Lambda with Terraform' — search 'terraform aws lambda tutorial'", "AWS docs: 'Lambda execution role' — docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html"]), PageBreak()]

# 7. EVENTBRIDGE
story += [P("7. File: terraform/modules/eventbridge/main.tf — Automated Scheduling", sH1), hr()]
story += [P("""EventBridge (formerly CloudWatch Events) is the AWS service that triggers the monitor Lambda every minute. Without it, nobody would be calling the Lambda — it would never run. EventBridge is the heartbeat of Sentinel.""", sBody)]
story += [code_block([
    "# Create a rule that fires every minute",
    "resource 'aws_cloudwatch_event_rule' 'every_minute' {",
    "  name                = 'sentinel_monitor_schedule'",
    "  schedule_expression = 'rate(1 minute)'   # AWS cron: fire every 1 minute",
    "  description         = 'Triggers Sentinel monitor Lambda every 60 seconds'",
    "}",
    "",
    "# Connect the rule to the Lambda function (the target)",
    "resource 'aws_cloudwatch_event_target' 'monitor_lambda' {",
    "  rule      = aws_cloudwatch_event_rule.every_minute.name",
    "  target_id = 'sentinel_monitor'",
    "  arn       = var.monitor_lambda_arn   # ARN of the Lambda to invoke",
    "}",
    "",
    "# Grant EventBridge permission to invoke the Lambda",
    "resource 'aws_lambda_permission' 'allow_eventbridge' {",
    "  statement_id  = 'AllowEventBridgeInvoke'",
    "  action        = 'lambda:InvokeFunction'",
    "  function_name = var.monitor_lambda_name",
    "  principal     = 'events.amazonaws.com'  # EventBridge's service identity",
    "  source_arn    = aws_cloudwatch_event_rule.every_minute.arn",
    "}",
])]
story += [sp(6), P("Schedule Expression Syntax", sH2)]
story += [info_box("EventBridge Schedule Expressions — Examples", [
    "rate(1 minute)      -> every minute",
    "rate(5 minutes)     -> every 5 minutes",
    "rate(1 hour)        -> every hour",
    "rate(1 day)         -> every 24 hours",
    "",
    "cron(0 8 * * ? *)   -> every day at 8:00 AM UTC",
    "cron(0 9 ? * MON *) -> every Monday at 9:00 AM UTC",
    "cron(0/15 * * * ? *)-> every 15 minutes",
    "",
    "Sentinel uses rate(1 minute) — the most frequent AWS allows.",
    "Note: rate(1 minute) means EventBridge fires the Lambda every ~60 seconds.",
    "It is NOT exactly 60.000 seconds — AWS makes best-effort guarantees.",
], bg=C_BG_GOOD, tc=C_GREEN)]
story += [sp(6), P("The Lambda Permission Resource — Why It Exists", sH2)]
story += [P("""In AWS, every service that wants to invoke Lambda must be explicitly granted permission. This is the principle of least privilege — by default, nothing can call anything. The `aws_lambda_permission` resource adds an entry to the Lambda's resource-based policy saying 'EventBridge from this specific rule is allowed to invoke this function'. Without it, EventBridge would get a permission denied error when trying to trigger the Lambda.""", sBody)]
story += [sp(4), alt_box("EventBridge (rate expression)", "Native AWS integration, no extra infrastructure, reliable, free for standard event buses.", "CloudWatch Events (older name for same service — EventBridge IS CloudWatch Events, just rebranded). AWS Step Functions (for complex multi-step workflows). SQS + cron on EC2 (much more complex). External cron services like cron-job.org (sends HTTP request to trigger work).")]
story += [sp(6), watch_box(["YouTube: 'AWS EventBridge explained' — search 'AWS EventBridge tutorial beginner'", "YouTube: 'Cron expressions explained' — search 'cron expression syntax explained'", "AWS docs: 'Schedule expressions using rate or cron' — docs.aws.amazon.com"]), PageBreak()]

# 8. SES
story += [P("8. File: terraform/modules/ses/main.tf — Email Alerting", sH1), hr()]
story += [P("""SES stands for Simple Email Service. It is AWS's email sending service. Sentinel uses it to send alert emails when a monitor goes down and recovery emails when it comes back up.""", sBody)]
story += [code_block([
    "# All SES does at infrastructure level is verify the email address",
    "resource 'aws_ses_email_identity' 'alert' {",
    "  email = var.alert_email  # e.g. 'denzel.chingodza@icloud.com'",
    "}",
    "",
    "# After this Terraform resource is applied:",
    "# - AWS sends a verification email to that address",
    "# - You click the link in it",
    "# - SES will now allow emails FROM and TO this address",
    "",
    "# In SES Sandbox (default for new accounts):",
    "# - Can only send to verified email addresses",
    "# - Limited to 200 emails per day",
    "# To send to any email: request production access from AWS console",
])]
story += [sp(6), P("How sendAlert Works in the Lambda", sH2)]
story += [code_block([
    "async function sendAlert(monitor, type, details) {",
    "  const subject = type === 'down'",
    "    ? `Sentinel Alert: ${monitor.name} is DOWN`",
    "    : `Sentinel Recovery: ${monitor.name} is back UP`;",
    "",
    "  const body = type === 'down'",
    "    ? `Your endpoint is down.\\nURL: ${monitor.url}\\nStatus: ${details.statusCode}\\n...`",
    "    : `Recovered!\\nDowntime: ${details.duration}`;",
    "",
    "  await ses.send(new SendEmailCommand({",
    "    Source: ALERT_EMAIL,          # 'from' address (must be verified in SES)",
    "    Destination: { ToAddresses: [ALERT_EMAIL] },  # 'to' (same address here)",
    "    Message: {",
    "      Subject: { Data: subject },",
    "      Body: { Text: { Data: body } },   # Plain text email",
    "    },",
    "  }));",
    "}",
])]
story += [sp(6), info_box("SES Sandbox vs Production Mode", [
    "Sandbox mode (default): can only send to verified email addresses.",
    "Sentinel uses the same email as both sender and recipient -> fine for personal use.",
    "",
    "Production mode: request via AWS console. Allows sending to any email address.",
    "Required if you wanted Sentinel to be a real product where users sign up with their",
    "own email addresses and receive alerts.",
    "",
    "SES pricing: $0.10 per 1000 emails. At 1 alert per outage, this costs practically nothing.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), alt_box("AWS SES", "No extra service to manage, deep AWS integration, cheap, reliable at scale.", "SendGrid (most popular email API, great developer experience, generous free tier). Mailgun (developer-focused, good deliverability). Postmark (best for transactional email, excellent logs). Resend (modern, simple API). Nodemailer (Node.js library — needs an SMTP server behind it).")]
story += [sp(6), watch_box(["YouTube: 'AWS SES tutorial' — search 'AWS Simple Email Service tutorial Lambda'", "AWS docs: 'Amazon SES Sandbox' — docs.aws.amazon.com/ses/latest/dg/request-production-access.html"]), PageBreak()]

# 9. API GATEWAY
story += [P("9. File: terraform/modules/api_gateway/main.tf — HTTP Routing", sH1), hr()]
story += [P("""API Gateway sits between the internet and the Lambda function. It provides a public HTTPS URL that the Next.js dashboard can call, then forwards requests to the API Lambda and returns its response. Without API Gateway, Lambda is not reachable from the internet.""", sBody)]
story += [code_block([
    "# 1. Create the REST API",
    "resource 'aws_api_gateway_rest_api' 'sentinel' {",
    "  name = 'sentinel-api'",
    "}",
    "",
    "# 2. Catch-all proxy resource: matches ANY path (/monitors, /monitors/123, etc.)",
    "resource 'aws_api_gateway_resource' 'proxy' {",
    "  rest_api_id = aws_api_gateway_rest_api.sentinel.id",
    "  parent_id   = aws_api_gateway_rest_api.sentinel.root_resource_id",
    "  path_part   = '{proxy+}'   # {proxy+} = greedy path match",
    "}",
    "",
    "# 3. Accept ANY HTTP method (GET, POST, DELETE, OPTIONS)",
    "resource 'aws_api_gateway_method' 'proxy' {",
    "  http_method   = 'ANY'",
    "  authorization = 'NONE'   # No authentication required",
    "}",
    "",
    "# 4. Connect to Lambda with Proxy Integration",
    "resource 'aws_api_gateway_integration' 'lambda' {",
    "  type                    = 'AWS_PROXY'",
    "  integration_http_method = 'POST'   # API GW always POSTs to Lambda internally",
    "  uri = 'arn:aws:apigateway:...:lambda:path/.../functions/.../invocations'",
    "}",
    "",
    "# 5. Deploy to 'prod' stage -> creates the URL",
    "resource 'aws_api_gateway_deployment' 'sentinel' {",
    "  stage_name = 'prod'",
    "  # Resulting URL: https://xyz.execute-api.af-south-1.amazonaws.com/prod",
    "}",
])]
story += [sp(6), P("Lambda Proxy Integration — What AWS_PROXY Means", sH2)]
story += [P("""With `type = 'AWS_PROXY'`, API Gateway passes the entire HTTP request to Lambda as a JSON event (the `event` object we saw in the API Lambda). Lambda's response object (`{ statusCode, headers, body }`) becomes the HTTP response sent back to the caller. This is the simplest integration — Lambda controls everything about the response. The alternative ('AWS integration') requires API Gateway to do response mapping, which is complex.""", sBody)]
story += [diagram_box("API Gateway Request Flow", [
    "Browser: GET https://xyz.execute-api.af-south-1.amazonaws.com/prod/monitors",
    "                                    |",
    "                                    v",
    "                              API Gateway",
    "                         (matches {proxy+} resource)",
    "                                    |",
    "                        AWS_PROXY integration",
    "                                    |",
    "                                    v",
    "            Lambda invoked with event = {",
    "              httpMethod: 'GET',",
    "              path: '/monitors',",
    "              headers: { ... },",
    "              queryStringParameters: null,",
    "              body: null",
    "            }",
    "                                    |",
    "                Lambda runs handler, returns:",
    "            { statusCode: 200, headers: {...}, body: '[{...}]' }",
    "                                    |",
    "                                    v",
    "                              API Gateway",
    "                    (converts Lambda response to HTTP response)",
    "                                    |",
    "Browser receives: HTTP 200, Content-Type: application/json, body: [{...}]",
])]
story += [sp(6), alt_box("API Gateway REST API", "Fully managed, integrates natively with Lambda, handles HTTPS, CORS, throttling, usage plans.", "API Gateway HTTP API (newer, cheaper, simpler — Sentinel could use this instead). ALB (Application Load Balancer — for containers, not Lambda). CloudFront Functions (for edge logic). Lambda Function URLs (direct HTTPS URL for Lambda, no API Gateway needed — simpler but less features).")]
story += [sp(6), watch_box(["YouTube: 'AWS API Gateway explained' — search 'API Gateway REST API Lambda tutorial'", "YouTube: 'Lambda Function URLs vs API Gateway' — search 'lambda function url vs api gateway'", "AWS docs: 'Set up a proxy resource with Lambda proxy integration'"]), PageBreak()]

# 10. ROOT TERRAFORM
story += [P("10. File: terraform/main.tf — Root Orchestration", sH1), hr()]
story += [P("""The root main.tf is the entry point for Terraform. It declares the required providers, configures AWS, and calls each module — passing outputs from one module as inputs to another.""", sBody)]
story += [code_block([
    "terraform {",
    "  required_version = '>= 1.0'",
    "  required_providers {",
    "    aws = { source = 'hashicorp/aws', version = '~> 5.0' }",
    "  }",
    "}",
    "",
    "provider 'aws' {",
    "  region = var.aws_region   # e.g. 'af-south-1' (Cape Town)",
    "}",
    "",
    "# Modules are called in order. Terraform resolves dependencies automatically.",
    "module 'dynamodb' { source = './modules/dynamodb' }",
    "",
    "module 'ses' {",
    "  source      = './modules/ses'",
    "  alert_email = var.alert_email",
    "}",
    "",
    "module 'lambda' {",
    "  source               = './modules/lambda'",
    "  monitors_table_name  = module.dynamodb.monitors_table_name  # Output from DynamoDB module",
    "  checks_table_arn     = module.dynamodb.checks_table_arn      # Output from DynamoDB module",
    "  ses_arn              = module.ses.ses_identity_arn            # Output from SES module",
    "  ...",
    "}",
    "",
    "module 'eventbridge' {",
    "  source              = './modules/eventbridge'",
    "  monitor_lambda_arn  = module.lambda.monitor_lambda_arn  # Output from Lambda module",
    "  monitor_lambda_name = module.lambda.monitor_lambda_name",
    "}",
    "",
    "module 'api_gateway' {",
    "  source         = './modules/api_gateway'",
    "  api_lambda_arn = module.lambda.api_lambda_arn",
    "  ...",
    "}",
])]
story += [sp(6), P("How Modules Pass Data", sH2)]
story += [P("""Each module has an `outputs.tf` file that declares what it shares with other modules. For example, the DynamoDB module outputs the table ARNs. The Lambda module receives those as input variables. Terraform resolves this graph automatically — if Lambda depends on DynamoDB's output, DynamoDB is created first.""", sBody)]
story += [sp(4), info_box("Terraform Workflow — Three Commands to Deploy Everything", [
    "terraform init    -> Downloads providers (aws plugin), initialises modules",
    "terraform plan    -> Shows exactly what will be created/modified/destroyed",
    "                     (safe: reads current state, shows diff, makes no changes)",
    "terraform apply   -> Creates/updates all resources (prompts for confirmation)",
    "",
    "After apply, ALL of Sentinel's infrastructure exists in AWS:",
    "3 DynamoDB tables + 2 Lambda functions + 1 EventBridge rule + 1 API Gateway + SES",
    "",
    "To tear everything down: terraform destroy",
], bg=C_BG_GOOD, tc=C_GREEN), sp(6)]
story += [watch_box(["YouTube: 'Terraform tutorial for beginners' — search 'terraform AWS beginners tutorial 2024'", "YouTube: 'Terraform modules explained' — search 'terraform modules reusable infrastructure'", "HashiCorp Learn: 'Get started with Terraform' — developer.hashicorp.com/terraform/tutorials"]), PageBreak()]

# 11. IAM DEEP DIVE
story += [P("11. Concept Deep-Dive: IAM — Identity and Access Management", sH1), hr()]
story += [P("""IAM is the security layer of AWS. Everything in AWS — every service, every action — requires explicit permission. IAM defines who (identity) can do what (action) to which resource. Getting IAM wrong means either a security breach or a broken application.""", sBody)]
story += [P("The Three Core Concepts", sH2)]
story += [info_box("IAM Concepts", [
    "ROLE: An identity that AWS services can assume. Not a user — a role has no password.",
    "  Sentinel's Lambda assumes 'sentinel_lambda_role' when it runs.",
    "  The role defines what the Lambda can do during execution.",
    "",
    "POLICY: A JSON document listing allowed (or denied) actions on resources.",
    "  Example: 'Allow dynamodb:PutItem on arn:aws:dynamodb:...:table/sentinel_checks'",
    "  Policies are attached to roles (or users, or groups).",
    "",
    "PRINCIPAL: Who or what is making the request.",
    "  In Sentinel: 'lambda.amazonaws.com' is the principal that can assume the role.",
    "  The trust policy says: 'Lambda service (and only Lambda) can use this role'.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), P("Principle of Least Privilege", sH2)]
story += [P("""Best practice in security: grant only the minimum permissions needed. Sentinel's Lambda policy grants only the specific DynamoDB actions it uses (PutItem, GetItem, UpdateItem, DeleteItem, Query, Scan) on only the specific table ARNs it accesses. It does NOT grant DynamoDB full access. If the Lambda were compromised, an attacker could not delete other DynamoDB tables — they can only access Sentinel's three tables.""", sBody)]
story += [code_block([
    "# BAD (too broad): 'Effect': 'Allow', 'Action': 'dynamodb:*', 'Resource': '*'",
    "# This grants ALL DynamoDB actions on ALL tables in the account",
    "",
    "# GOOD (least privilege): Sentinel's actual policy",
    "'Action': ['dynamodb:PutItem', 'dynamodb:GetItem', 'dynamodb:UpdateItem',",
    "           'dynamodb:DeleteItem', 'dynamodb:Query', 'dynamodb:Scan']",
    "'Resource': [",
    "  'arn:aws:dynamodb:af-south-1:ACCOUNT_ID:table/sentinel_monitors',",
    "  'arn:aws:dynamodb:af-south-1:ACCOUNT_ID:table/sentinel_checks',",
    "  'arn:aws:dynamodb:af-south-1:ACCOUNT_ID:table/sentinel_incidents',",
    "  # Also need access to the indexes:",
    "  'arn:aws:dynamodb:af-south-1:ACCOUNT_ID:table/sentinel_checks/index/*',",
    "]",
    "",
    "# The Lambda CANNOT access other tables, other accounts, other regions",
], dark=False)]
story += [sp(6), watch_box(["YouTube: 'AWS IAM explained' — search 'AWS IAM tutorial 2024 beginners'", "YouTube: 'AWS IAM roles vs users vs policies' — search 'IAM role policy user difference explained'", "AWS docs: 'Security best practices in IAM' — docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"]), PageBreak()]

# 12. DYNAMODB DATA MODELLING
story += [P("12. Concept Deep-Dive: DynamoDB Data Modelling", sH1), hr()]
story += [P("""DynamoDB requires you to know your access patterns before designing your schema. This is the biggest difference from SQL — in SQL, you can write any query after the fact. In DynamoDB, queries you didn't plan for can be extremely expensive (requiring full table scans).""", sBody)]
story += [P("Access Patterns Sentinel Needs", sH2)]
story += [info_box("Sentinel's Data Access Patterns", [
    "1. Get all active monitors -> ScanCommand on monitors (small table, OK to scan)",
    "2. Get all monitors (for dashboard) -> ScanCommand on monitors",
    "3. Get single monitor -> GetCommand by id",
    "4. Update monitor status -> UpdateCommand by id",
    "5. Store a check result -> PutCommand (new item)",
    "6. Get last N checks for a monitor -> QueryCommand on monitorId-timestamp-index GSI",
    "7. Get open incidents for a monitor -> QueryCommand on monitorId-index GSI",
    "8. Update an incident (resolve it) -> UpdateCommand by id",
    "",
    "Patterns 6 and 7 REQUIRE GSIs — without them, you'd scan the whole table every time.",
], bg=C_BG_GOOD, tc=C_GREEN)]
story += [sp(6), P("UpdateExpression Syntax", sH2)]
story += [P("""DynamoDB's UpdateCommand doesn't take a full item — it takes an expression describing what to change. This avoids overwriting fields you didn't intend to touch:""", sBody)]
story += [code_block([
    "await dynamo.send(new UpdateCommand({",
    "  TableName: MONITORS_TABLE,",
    "  Key: { id: monitor.id },   // Find the item",
    "  UpdateExpression: 'SET lastStatus = :s, lastChecked = :t, lastResponseTime = :r',",
    "  ExpressionAttributeValues: {",
    "    ':s': healthy ? 'up' : 'down',",
    "    ':t': timestamp,",
    "    ':r': responseTime,",
    "  }",
    "}));",
    "",
    "// Only lastStatus, lastChecked, lastResponseTime are updated.",
    "// url, name, active, createdAt are NOT touched.",
    "",
    "// SET: set a value  |  REMOVE: delete an attribute  |  ADD: increment a number",
], dark=False)]
story += [sp(6), P("FilterExpression vs KeyConditionExpression", sH2)]
story += [P("""KeyConditionExpression filters by the primary key (hash + range). DynamoDB uses the key to find the right partition first — fast. FilterExpression is applied AFTER DynamoDB retrieves items matching the key condition — it discards non-matching items but they still cost read capacity. Always prefer KeyConditionExpression where possible.""", sBody)]
story += [watch_box(["YouTube: 'DynamoDB data modelling' — search 'DynamoDB single table design tutorial'", "YouTube: 'DynamoDB GSI explained' — search 'DynamoDB global secondary index tutorial'", "AWS re:Invent: 'Advanced Design Patterns for DynamoDB' — search 'DynamoDB design patterns Rick Houlihan'"]), PageBreak()]

# 13. IaC
story += [P("13. Concept Deep-Dive: Infrastructure as Code", sH1), hr()]
story += [P("""Infrastructure as Code (IaC) means your cloud resources are defined in text files that live in Git, just like your application code. Before IaC, developers would click through AWS consoles to create resources — slow, error-prone, and impossible to reproduce exactly.""", sBody)]
story += [P("Why IaC Matters", sH2)]
story += [info_box("What Terraform Gives You", [
    "REPRODUCIBILITY: 'terraform apply' creates identical infrastructure every time.",
    "  Sentinel's full AWS setup (3 tables + 2 lambdas + eventbridge + API GW + SES)",
    "  is created from scratch in ~2 minutes with one command.",
    "",
    "VERSION CONTROL: infrastructure changes are tracked in Git.",
    "  You can see exactly when a new table was added, what changed, who changed it.",
    "",
    "SAFE CHANGES: 'terraform plan' shows you exactly what will change before applying.",
    "  No surprises — if plan shows 'delete 3 resources', you know before it happens.",
    "",
    "DESTROY AND REBUILD: 'terraform destroy' removes everything cleanly.",
    "  Useful for cost control (spin up for testing, destroy when done).",
    "",
    "TEAM COLLABORATION: everyone on a team works with the same infrastructure definition.",
], bg=C_BG_ALT, tc=C_BLUE)]
story += [sp(6), P("Terraform State", sH2)]
story += [P("""Terraform maintains a state file (`terraform.tfstate`) that records what resources exist in AWS. When you run `terraform apply`, it compares the desired state (your .tf files) with the actual state (tfstate) and the real AWS resources, then makes only the necessary changes. The state file contains sensitive data — it should be stored in S3 with encryption in production, not committed to Git.""", sBody)]
story += [sp(4), alt_box("Terraform", "Cloud-agnostic (works with AWS, GCP, Azure, and 3000+ providers). Declarative (describe what you want, not how to get it). Huge ecosystem.", "AWS CloudFormation (AWS-only, more verbose, free). AWS CDK (define infrastructure in TypeScript/Python — more familiar for developers). Pulumi (IaC in TypeScript/Python/Go — similar to CDK). Serverless Framework (focused on serverless apps, simpler than Terraform for Lambda).")]
story += [sp(6), watch_box(["YouTube: 'Terraform in 100 seconds' — Fireship YouTube channel", "YouTube: 'Terraform AWS full course beginners' — search 'terraform aws tutorial beginner'", "HashiCorp Learn: free interactive Terraform tutorials — developer.hashicorp.com/terraform"]), PageBreak()]

# 14. HTTP + CORS
story += [P("14. Concept Deep-Dive: HTTP, CORS, and the API Contract", sH1), hr()]
story += [P("""Every interaction between Sentinel's Next.js dashboard and the Lambda API happens over HTTP. Understanding HTTP is fundamental to understanding how any web application communicates.""", sBody)]
story += [P("HTTP Request-Response Cycle", sH2)]
story += [diagram_box("A Real Sentinel API Call Dissected", [
    "Request from Next.js dashboard:",
    "  POST https://xyz.execute-api.af-south-1.amazonaws.com/prod/monitors",
    "  Headers:",
    "    Content-Type: application/json",
    "    Origin: https://sentinel-kappa-wine.vercel.app",
    "  Body (JSON): { 'name': 'My API', 'url': 'https://myapi.com/health' }",
    "",
    "What happens at the server:",
    "  1. API Gateway receives HTTPS request, terminates SSL",
    "  2. Creates event object, invokes Lambda",
    "  3. Lambda handler runs: validates input, PutItem to DynamoDB",
    "  4. Lambda returns: { statusCode: 201, headers: {...}, body: '{...}' }",
    "  5. API Gateway sends HTTP 201 response with CORS headers",
    "",
    "Response to browser:",
    "  HTTP/1.1 201 Created",
    "  Content-Type: application/json",
    "  Access-Control-Allow-Origin: *",
    "  Body: { 'id': 'abc-123', 'name': 'My API', 'url': '...', 'active': true }",
])]
story += [sp(6), P("CORS — The Browser's Same-Origin Policy", sH2)]
story += [P("""Browsers enforce the Same-Origin Policy: JavaScript running at origin A cannot read responses from origin B. 'Origin' = protocol + domain + port. `https://sentinel-kappa-wine.vercel.app` and `https://xyz.execute-api.af-south-1.amazonaws.com` are different origins. Without CORS headers in the API response, the browser blocks the response from the JavaScript code — even if the server processed the request successfully.""", sBody)]
story += [info_box("CORS Preflight — The OPTIONS Request", [
    "Before a cross-origin POST, the browser sends a 'preflight' OPTIONS request:",
    "  OPTIONS /monitors HTTP/1.1",
    "  Origin: https://sentinel-kappa-wine.vercel.app",
    "  Access-Control-Request-Method: POST",
    "  Access-Control-Request-Headers: content-type",
    "",
    "The server must respond with permissions:",
    "  Access-Control-Allow-Origin: *",
    "  Access-Control-Allow-Methods: GET,POST,DELETE,OPTIONS",
    "  Access-Control-Allow-Headers: Content-Type",
    "",
    "If the server returns these headers, the browser proceeds with the actual POST.",
    "Sentinel's API Lambda handles OPTIONS explicitly: if (method === 'OPTIONS') return response(200, {})",
], bg=C_BG_NOTE, tc=C_AMBER)]
story += [sp(6), watch_box(["YouTube: 'CORS explained in 6 minutes' — search 'CORS explained simply'", "MDN Web Docs: 'Cross-Origin Resource Sharing (CORS)' — developer.mozilla.org/en-US/docs/Web/HTTP/CORS", "YouTube: 'HTTP request response cycle' — search 'how HTTP works explained'"]), PageBreak()]

# 15. QUICK REFERENCE
story += [P("15. Quick Reference — AWS Services & Technology Choices", sH1), hr(), sp(4)]
tdata = [
    ["Service / Tool", "What It Does in Sentinel", "Alternative"],
    ["AWS Lambda", "Runs monitor logic every 60s + serves the API on demand. No server to manage.", "EC2, ECS, Render"],
    ["DynamoDB", "Stores monitors, check history, incidents. NoSQL key-value + document store.", "Aurora, MongoDB, Firebase"],
    ["EventBridge", "Triggers the monitor Lambda every 60 seconds on a schedule.", "CloudWatch Events (same), SQS+cron"],
    ["AWS SES", "Sends alert emails (down/recovery notifications) via Lambda.", "SendGrid, Mailgun, Resend"],
    ["API Gateway", "Provides a public HTTPS URL that routes requests to the API Lambda.", "Lambda Function URLs, ALB"],
    ["IAM", "Controls permissions — what each Lambda is allowed to do in AWS.", "No alternative (fundamental to AWS)"],
    ["Terraform", "Defines and deploys all infrastructure as code in .tf files.", "CloudFormation, CDK, Pulumi"],
    ["Node.js", "Runtime for Lambda functions. JavaScript on the server.", "Python, Go, Java (all supported in Lambda)"],
    ["AWS SDK v3", "JavaScript library for talking to DynamoDB, SES from Node.js.", "AWS SDK v2 (older), direct HTTP to AWS API"],
    ["randomUUID()", "Generates unique IDs for monitors, checks, incidents.", "uuid npm package, nanoid, ULID"],
    ["Next.js (frontend)", "Dashboard UI — fetches data from API Gateway, displays it.", "React + Vite, plain HTML/JS"],
    ["Vercel (frontend)", "Hosts the Next.js dashboard, deploys from GitHub.", "Netlify, Cloudflare Pages, AWS Amplify"],
]
cw = [(W-ML-MR-4)*x for x in [0.28, 0.44, 0.28]]
t = Table(tdata, colWidths=cw)
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),C_NAVY),("TEXTCOLOR",(0,0),(-1,0),C_WHITE),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8.5),
    ("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTNAME",(0,1),(0,-1),"Courier-Bold"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[C_WHITE,C_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#BDC3C7")),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
]))
story += [t, sp(16)]
story += [HRFlowable(width="100%",thickness=2,color=C_NAVY,spaceAfter=8), sp(6)]
story += [P("This document was generated specifically for Denzel Chingodza to help him understand and speak confidently about Sentinel in interviews and technical conversations.", sCaption)]
story += [P("Sentinel — github.com/denzelchingodza/sentinel  |  Live at sentinel-kappa-wine.vercel.app", sCaption)]

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(C_GRAY)
    canvas.drawString(ML, 12*mm, "Sentinel Backend Deep-Dive")
    canvas.drawRightString(W-MR, 12*mm, f"Page {doc.page}")
    canvas.restoreState()

pdf = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB)
pdf.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Done: {OUT}")
