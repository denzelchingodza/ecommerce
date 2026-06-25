<?php
// ============================================================
//  LinkUP — PHP REST API (Server-Side Backend)
//  Handles all core functionality via HTTP requests.
//  Frontend sends requests here; PHP talks to MySQL and
//  returns JSON responses back to the browser.
// ============================================================

header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

// ── DATABASE CONNECTION ──────────────────────────────────────
$conn = new mysqli("localhost", "root", "", "linkup_db");
if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(["error" => "Database connection failed."]);
    exit;
}

// ── ROUTER ───────────────────────────────────────────────────
// Reads the URL and method, then calls the right function.
$method = $_SERVER['REQUEST_METHOD'];
$path   = trim($_SERVER['PATH_INFO'] ?? '/', '/');
$body   = json_decode(file_get_contents("php://input"), true);

switch ("$method $path") {
    case "POST register":       registerUser($body);        break;
    case "POST login":          loginUser($body);           break;
    case "GET products":        getProducts();              break;
    case "POST products":       addProduct($body);          break;
    case "POST orders":         placeOrder($body);          break;
    case "GET admin/stats":     adminStats();               break;
    case "PUT admin/ban":       banUser($body);             break;
    case "PUT admin/unban":     unbanUser($body);           break;
    case "PUT admin/suspend":   suspendProduct($body);      break;
    case "PUT admin/reinstate": reinstateProduct($body);    break;
    default:
        http_response_code(404);
        echo json_encode(["error" => "Endpoint not found."]);
}


// ════════════════════════════════════════════════════════════
//  1. USER REGISTRATION
//  Called when a user submits the register form.
//  POST /register   { name, email, password }
// ════════════════════════════════════════════════════════════
function registerUser($data) {
    global $conn;

    $name     = $data['name']     ?? '';
    $email    = $data['email']    ?? '';
    $password = $data['password'] ?? '';

    if (!$name || !$email || !$password) {
        http_response_code(400);
        echo json_encode(["error" => "All fields are required."]);
        return;
    }

    // Check if email already registered
    $check = $conn->prepare("SELECT id FROM users WHERE email = ?");
    $check->bind_param("s", $email);
    $check->execute();
    if ($check->get_result()->num_rows > 0) {
        http_response_code(409);
        echo json_encode(["error" => "Email already registered."]);
        return;
    }

    // Hash password — never store plain text
    $hashed = password_hash($password, PASSWORD_BCRYPT);

    $stmt = $conn->prepare(
        "INSERT INTO users (name, email, password, is_banned, created_at)
         VALUES (?, ?, ?, 0, NOW())"
    );
    $stmt->bind_param("sss", $name, $email, $hashed);
    $stmt->execute();

    http_response_code(201);
    echo json_encode(["success" => true, "message" => "Account created."]);
}


// ════════════════════════════════════════════════════════════
//  2. USER LOGIN
//  Verifies credentials. Blocks banned accounts.
//  POST /login   { email, password }
// ════════════════════════════════════════════════════════════
function loginUser($data) {
    global $conn;

    $email    = $data['email']    ?? '';
    $password = $data['password'] ?? '';

    $stmt = $conn->prepare("SELECT * FROM users WHERE email = ? LIMIT 1");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $user = $stmt->get_result()->fetch_assoc();

    if (!$user) {
        http_response_code(401);
        echo json_encode(["error" => "No account found with that email."]);
        return;
    }

    // Block banned users before checking password
    if ($user['is_banned']) {
        http_response_code(403);
        echo json_encode(["error" => "Your account has been banned by an administrator."]);
        return;
    }

    if (!password_verify($password, $user['password'])) {
        http_response_code(401);
        echo json_encode(["error" => "Incorrect password."]);
        return;
    }

    // Return a simple session token (in production: JWT)
    $token = base64_encode($user['email'] . ':' . time());

    echo json_encode([
        "success" => true,
        "token"   => $token,
        "user"    => [
            "name"  => $user['name'],
            "email" => $user['email'],
        ]
    ]);
}


// ════════════════════════════════════════════════════════════
//  3. GET ALL ACTIVE PRODUCTS
//  Returns only listings that are not suspended.
//  Supports optional filters: category, max_price, condition.
//  GET /products?category=Electronics&max_price=500
// ════════════════════════════════════════════════════════════
function getProducts() {
    global $conn;

    $sql    = "SELECT * FROM products WHERE status = 'active'";
    $params = [];
    $types  = "";

    if (!empty($_GET['category'])) {
        $sql .= " AND category = ?";
        $params[] = $_GET['category'];
        $types   .= "s";
    }

    if (!empty($_GET['max_price'])) {
        $sql .= " AND price <= ?";
        $params[] = (float) $_GET['max_price'];
        $types   .= "d";
    }

    if (!empty($_GET['condition'])) {
        $sql .= " AND product_condition = ?";
        $params[] = $_GET['condition'];
        $types   .= "s";
    }

    $sql .= " ORDER BY created_at DESC";

    $stmt = $conn->prepare($sql);
    if ($params) {
        $stmt->bind_param($types, ...$params);
    }
    $stmt->execute();
    $products = $stmt->get_result()->fetch_all(MYSQLI_ASSOC);

    echo json_encode(["success" => true, "products" => $products]);
}


// ════════════════════════════════════════════════════════════
//  4. ADD A PRODUCT (SELL)
//  Called when a seller submits the listing form.
//  POST /products   { title, price, category, condition, description, seller_email }
// ════════════════════════════════════════════════════════════
function addProduct($data) {
    global $conn;

    $title       = $data['title']        ?? '';
    $price       = $data['price']        ?? 0;
    $category    = $data['category']     ?? '';
    $condition   = $data['condition']    ?? '';
    $description = $data['description'] ?? '';
    $seller      = $data['seller_email'] ?? '';

    $stmt = $conn->prepare(
        "INSERT INTO products (title, price, category, product_condition, description, seller_email, status, created_at)
         VALUES (?, ?, ?, ?, ?, ?, 'active', NOW())"
    );
    $stmt->bind_param("sdssss", $title, $price, $category, $condition, $description, $seller);
    $stmt->execute();

    echo json_encode([
        "success"    => true,
        "product_id" => $conn->insert_id,
        "message"    => "Product listed successfully."
    ]);
}


// ════════════════════════════════════════════════════════════
//  5. PLACE AN ORDER
//  Saves a confirmed order after checkout.
//  POST /orders   { buyer_email, items, total, payment_method }
// ════════════════════════════════════════════════════════════
function placeOrder($data) {
    global $conn;

    $buyer   = $data['buyer_email']    ?? '';
    $items   = json_encode($data['items'] ?? []);
    $total   = $data['total']          ?? 0;
    $payment = $data['payment_method'] ?? 'COD';

    $stmt = $conn->prepare(
        "INSERT INTO orders (buyer_email, items_json, total, payment_method, status, created_at)
         VALUES (?, ?, ?, ?, 'confirmed', NOW())"
    );
    $stmt->bind_param("ssds", $buyer, $items, $total, $payment);
    $stmt->execute();

    echo json_encode([
        "success"  => true,
        "order_id" => $conn->insert_id,
        "message"  => "Order confirmed."
    ]);
}


// ════════════════════════════════════════════════════════════
//  6. ADMIN: DASHBOARD STATS
//  Returns totals shown on the admin dashboard.
//  GET /admin/stats
// ════════════════════════════════════════════════════════════
function adminStats() {
    global $conn;

    $users    = $conn->query("SELECT COUNT(*) c FROM users")->fetch_assoc()['c'];
    $listings = $conn->query("SELECT COUNT(*) c FROM products WHERE status='active'")->fetch_assoc()['c'];
    $orders   = $conn->query("SELECT COUNT(*) c FROM orders")->fetch_assoc()['c'];
    $banned   = $conn->query("SELECT COUNT(*) c FROM users WHERE is_banned=1")->fetch_assoc()['c'];
    $suspended= $conn->query("SELECT COUNT(*) c FROM products WHERE status='suspended'")->fetch_assoc()['c'];

    echo json_encode([
        "total_users"       => $users,
        "active_listings"   => $listings,
        "total_orders"      => $orders,
        "banned_users"      => $banned,
        "suspended_listings"=> $suspended,
    ]);
}


// ════════════════════════════════════════════════════════════
//  7. ADMIN: BAN / UNBAN A USER
//  Banned users are blocked immediately on next login attempt.
//  PUT /admin/ban      { email }
//  PUT /admin/unban    { email }
// ════════════════════════════════════════════════════════════
function banUser($data) {
    global $conn;
    $email = $data['email'] ?? '';
    $stmt  = $conn->prepare("UPDATE users SET is_banned = 1 WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    echo json_encode(["success" => true, "message" => "User banned: $email"]);
}

function unbanUser($data) {
    global $conn;
    $email = $data['email'] ?? '';
    $stmt  = $conn->prepare("UPDATE users SET is_banned = 0 WHERE email = ?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    echo json_encode(["success" => true, "message" => "User unbanned: $email"]);
}


// ════════════════════════════════════════════════════════════
//  8. ADMIN: SUSPEND / REINSTATE A PRODUCT
//  Suspended products are hidden from the marketplace.
//  PUT /admin/suspend    { product_id }
//  PUT /admin/reinstate  { product_id }
// ════════════════════════════════════════════════════════════
function suspendProduct($data) {
    global $conn;
    $id   = $data['product_id'] ?? 0;
    $stmt = $conn->prepare("UPDATE products SET status = 'suspended' WHERE id = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    echo json_encode(["success" => true, "message" => "Product #$id suspended."]);
}

function reinstateProduct($data) {
    global $conn;
    $id   = $data['product_id'] ?? 0;
    $stmt = $conn->prepare("UPDATE products SET status = 'active' WHERE id = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    echo json_encode(["success" => true, "message" => "Product #$id reinstated."]);
}

$conn->close();
?>
