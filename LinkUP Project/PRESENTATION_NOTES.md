# LinkUP — Presentation Notes
### Read this on your phone while presenting

---

## THE BIG PICTURE

LinkUP is a C2C (customer-to-customer) marketplace for South African informal traders.

**Two layers:**
- **Frontend** — 13 HTML pages the user sees and clicks
- **Backend** — Python (FastAPI) server that handles data and logic

The live demo on Netlify uses **localStorage** (browser storage) as a demo data layer. The real Python backend is built and ready to plug in.

---

## FRONTEND FILES (what the user sees)

**index.html** — Home page. Shows featured products, trust strip, nav bar. When you land here it checks localStorage for `isLoggedIn` and `isGuest` to decide what to show in the nav.

**products.html** — The marketplace. Reads all products from `admin_products` in localStorage. Filters out anything with `status: suspended` so banned listings never show. Has search, category filter, price filter, condition filter, and a Today's Deals strip.

**product.html** — Single product detail page. Reads the product ID from the URL, finds it in localStorage, displays title, price, images, seller info. Add to cart button writes to `linkup_cart`.

**sell.html** — The seller form. When submitted, creates a product object and pushes it into `admin_products` in localStorage. It instantly appears in products.html.

**cart.html** — Shows items from `linkup_cart`. Has two checkout options:
1. **PayFast** — builds a real payment form with MD5 signature and redirects to PayFast sandbox
2. **COD** — skips payment, confirms order immediately

Both save to `linkup_orders` in localStorage.

**account.html** — Personal dashboard. Reads real data — filters `linkup_orders` by logged-in email for order history, filters `admin_products` by email for active listings, reads `linkup_saved` for wishlist.

**register.html** — Sign up form. Saves new user to `linkup_users` array in localStorage. Hashes are not used in the demo (localStorage version) but the backend uses bcrypt.

**login.html** — Checks email + password against `linkup_users`. If account has `is_banned: true`, blocks login immediately. On success sets `isLoggedIn`, `userEmail` in localStorage.

**admin-login.html** — Separate login page for admin only. Credentials: admin@linkup.com / Admin@2025

**admin.html** — Admin control panel.
- Dashboard stats (total users, listings, orders)
- Users tab: see all users, ban or unban instantly
- Products tab: see all listings, suspend or reinstate instantly
- Changes take effect immediately — no page reload needed

**about.html** — About page with project description and developer section (Denzel Chingodza, EDUV4940179).

**settings.html** — Edit profile, change password, delete account.

**chat.html** — Messaging between buyers and sellers.

---

## HOW LOCALSTORAGE WORKS AS A DATABASE

Think of localStorage like a set of database tables stored in the browser:

| localStorage key | What it stores |
|---|---|
| `linkup_users` | All registered accounts |
| `admin_products` | All product listings |
| `linkup_orders` | All placed orders |
| `linkup_cart` | Current user's cart |
| `linkup_saved` | Wishlist / saved items |
| `isLoggedIn` | Is a user logged in? |
| `userEmail` | Which user is logged in |
| `isGuest` | Is someone browsing as guest? |

Every page reads from and writes to these keys. That is our entire data layer for the demo.

---

## REAL BACKEND (FastAPI + Python + MongoDB)

This is the actual server-side code in the `/backend` folder.

**main.py** — Entry point. Starts the server. Connects to MongoDB on startup. Registers all the route files. Sets up CORS (so the frontend can talk to the backend). Serves uploaded images.

**routes/auth.py** — Handles user accounts:
- `POST /api/auth/register` — creates account, saves to MongoDB, returns a JWT token
- `POST /api/auth/login` — checks email + password (using bcrypt), returns JWT token
- `GET /api/auth/me` — returns logged-in user's profile (requires valid token)

**routes/products.py** — Handles listings:
- `GET /api/products` — returns all products, supports search, category, price filters
- `POST /api/products` — creates a new listing (must be logged in)
- `PUT /api/products/{id}` — edit your own listing
- `DELETE /api/products/{id}` — delete your own listing
- `POST /api/products/{id}/images` — upload product photos (resized automatically with Pillow)

**routes/cart.py** — Handles cart and checkout

**routes/messages.py** — Handles buyer-seller messaging

**config/database.py** — MongoDB connection. Uses Motor (async MongoDB driver) so the server can handle many users at once without slowing down.

**middleware/auth.py** — JWT authentication. Every protected route checks the token in the request header. If missing or expired, access is denied.

**models/user.py, product.py, cart_message.py** — Pydantic models. These define the exact shape of data going in and out of the API. Think of them as the form validation layer.

---

## WHAT IS DOCKER AND WHAT DOES IT DO HERE

**Docker** packages your entire application — code, Python version, all dependencies — into a container. A container is like a mini computer that runs the same way on any machine.

**Without Docker:**
Someone else downloads your code, installs Python, installs the wrong version, installs libraries — and it breaks.

**With Docker:**
They run one command: `docker compose up --build` — and everything starts automatically, configured correctly, every time.

**Your Dockerfile (in /backend):**
```
FROM python:3.12-slim       ← use Python 3.12
WORKDIR /app                ← work inside /app folder
COPY requirements.txt .     ← copy the dependencies list
RUN pip install -r ...      ← install all dependencies
COPY . .                    ← copy all your code
CMD ["uvicorn", "main:app"] ← start the FastAPI server
```

**What to say:**
> "The Dockerfile containerises our Python backend. When deployed, Docker pulls the Python image, installs our dependencies from requirements.txt, copies the code, and starts the FastAPI server on port 8000. This makes the backend portable — it runs the same way on any server or cloud platform."

---

## PHP vs PYTHON — WHY WE USED PYTHON

| PHP | Our Python (FastAPI) |
|---|---|
| Server-side scripting | Server-side API |
| Returns HTML pages | Returns JSON (REST API) |
| Typically with MySQL | We use MongoDB |
| Synchronous | Async — handles more users |

The logic is identical — register user, verify login, list products, place order, admin controls. Python with FastAPI is just a more modern approach, especially for a marketplace that needs to handle many requests at once.

---

## WHAT TO SAY IF ASKED

**"Why localStorage and not a real database?"**
> localStorage was used for the demo so the app can run on Netlify without a server. The real MongoDB backend is built and ready — it would just replace the localStorage calls.

**"Is the backend functional?"**
> Yes. The FastAPI backend connects to MongoDB, handles authentication with JWT tokens, manages products, cart, and messaging. It's containerised with Docker and can be deployed to any cloud server.

**"What does Docker do?"**
> It packages the backend so it runs consistently anywhere. One command starts the server, database, and everything needed.

**"How does the admin ban work?"**
> In the demo: the user object in `linkup_users` gets `is_banned: true`. The login page checks that flag before granting access. In the backend: MongoDB updates the user document, and every login attempt queries that field first.

---

*Student: Denzel Chingodza | EDUV4940179 | ITECA3-12 | Eduvos Mowbray | Mr S. Mazibuko*
