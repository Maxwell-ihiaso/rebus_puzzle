
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io
from typing import List, Tuple, Dict

# ------------------------------
# Utilities
# ------------------------------
def get_font(size: int):
    for name in ["DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"]:
        try:
            return ImageFont.truetype(name, size=size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_puzzle(layout: List[Dict], w: int = 1100, h: int = 650, bg="#0b1220", fg="#e7edf7"):
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    border = 8
    draw.rounded_rectangle((border, border, w-border, h-border), radius=24, outline=fg, width=2)

    for item in layout:
        text = item.get("text", "")
        x, y = item.get("xy", [w//2, h//2])
        size = item.get("size", 64)
        rotate = item.get("rotate", 0)
        align = item.get("align", "center")
        underline = item.get("underline", False)
        box = item.get("box", None)
        dashed = item.get("dashed", False)
        opacity = item.get("opacity", 255)

        font = get_font(size)
        bbox = font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        if align == "center":
            tx = x - tw//2
            ty = y - th//2
        elif align == "left":
            tx = x
            ty = y - th//2
        else:
            tx = x - tw
            ty = y - th//2

        if box:
            pad = box.get("pad", 16)
            rx1, ry1 = tx - pad, ty - pad
            rx2, ry2 = tx + tw + pad, ty + th + pad
            radius = box.get("radius", 12)
            fill = box.get("fill", None)
            outline = box.get("outline", fg)
            width = box.get("width", 2)
            if dashed:
                dash_len = 12
                gap = 8
                cur = rx1
                while cur < rx2:
                    draw.line((cur, ry1, min(cur+dash_len, rx2), ry1), fill=outline, width=width)
                    cur += dash_len + gap
                cur = rx1
                while cur < rx2:
                    draw.line((cur, ry2, min(cur+dash_len, rx2), ry2), fill=outline, width=width)
                    cur += dash_len + gap
                cur = ry1
                while cur < ry2:
                    draw.line((rx1, cur, rx1, min(cur+dash_len, ry2)), fill=outline, width=width)
                    cur += dash_len + gap
                cur = ry1
                while cur < ry2:
                    draw.line((rx2, cur, rx2, min(cur+dash_len, ry2)), fill=outline, width=width)
                    cur += dash_len + gap
            else:
                draw.rounded_rectangle((rx1, ry1, rx2, ry2), radius=radius, outline=outline, width=width, fill=fill)

        txt_img = Image.new("RGBA", (tw+4, th+4), (0,0,0,0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((2,2), text, font=font, fill=(231,237,247, opacity))
        if underline:
            txt_draw.line((0, th+1, tw, th+1), fill=(231,237,247, opacity), width=max(2, size//16))
        if rotate != 0:
            txt_img = txt_img.rotate(rotate, expand=True)
        img.paste(txt_img, (int(tx), int(ty)), txt_img)
    return img

# ------------------------------
# PUZZLES (~50)
# ------------------------------
PUZZLES = [
    {
        "id": "microservices",
        "answer": "Microservices",
        "hint": "Many small 'SERV' pieces.",
        "layout": [
            {"text": "SERV", "xy": [300, 200], "size": 72},
            {"text": "SERV", "xy": [480, 200], "size": 72},
            {"text": "SERV", "xy": [660, 200], "size": 72},
            {"text": "SERV", "xy": [300, 350], "size": 72},
            {"text": "SERV", "xy": [480, 350], "size": 72},
            {"text": "SERV", "xy": [660, 350], "size": 72},
            {"text": "micro", "xy": [480, 100], "size": 36, "underline": True}
        ]
    },
    {
        "id": "api_gateway",
        "answer": "API Gateway",
        "hint": "One entrance for many APIs.",
        "layout": [
            {"text": "API   API   API", "xy": [200, 240], "size": 56, "align": "left"},
            {"text": "      ↓", "xy": [210, 300], "size": 48, "align": "left"},
            {"text": "[  GATEWAY  ]", "xy": [550, 360], "size": 64, "align": "center", "box": {"pad": 18, "radius": 10}}
        ]
    },
    {
        "id": "data_pipeline",
        "answer": "Data Pipeline",
        "hint": "Data flows in stages.",
        "layout": [
            {"text": "DATA  →  DATA  →  DATA  →  DATA", "xy": [100, 300], "size": 58, "align": "left"}
        ]
    },
    {
        "id": "devsecops",
        "answer": "DevSecOps",
        "hint": "Development meets security meets ops.",
        "layout": [
            {"text": "SEC", "xy": [550, 200], "size": 72},
            {"text": "SEC", "xy": [550, 270], "size": 72},
            {"text": "SEC", "xy": [550, 340], "size": 72},
            {"text": "DEV", "xy": [350, 380], "size": 72},
            {"text": "OPS", "xy": [750, 380], "size": 72}
        ]
    },
    {
        "id": "agile",
        "answer": "Agile",
        "hint": "AGI over LE.",
        "layout": [
            {"text": "AGI", "xy": [550, 260], "size": 96},
            {"text": "L  E", "xy": [550, 360], "size": 96}
        ]
    },
    {
        "id": "scrum_sprint",
        "answer": "Scrum Sprint",
        "hint": "Scrum, but moving forward quickly.",
        "layout": [
            {"text": "SCRUM", "xy": [420, 260], "size": 72, "align": "center"},
            {"text": "     SCRUM", "xy": [540, 320], "size": 72, "align": "center"},
            {"text": "          SCRUM", "xy": [660, 380], "size": 72, "align": "center"}
        ]
    },
    {
        "id": "load_balancer",
        "answer": "Load Balancer",
        "hint": "Spreading requests evenly.",
        "layout": [
            {"text": "REQUESTS", "xy": [550, 140], "size": 64},
            {"text": "↓↓↓↓↓↓", "xy": [550, 210], "size": 48},
            {"text": "[ BALANCER ]", "xy": [550, 290], "size": 64, "box": {"pad": 16}},
            {"text": "srv1     srv2     srv3     srv4", "xy": [550, 370], "size": 56}
        ]
    },
    {
        "id": "rate_limit",
        "answer": "Rate Limiting",
        "hint": "Requests per time window.",
        "layout": [
            {"text": "REQ REQ REQ REQ REQ", "xy": [550, 240], "size": 56},
            {"text": "per", "xy": [550, 300], "size": 40},
            {"text": "TIME", "xy": [550, 360], "size": 56, "underline": True}
        ]
    },
    {
        "id": "cache_hit",
        "answer": "Cache Hit",
        "hint": "Found in memory.",
        "layout": [
            {"text": "CACHE", "xy": [550, 260], "size": 92},
            {"text": "✓", "xy": [710, 260], "size": 92}
        ]
    },
    {
        "id": "cicd",
        "answer": "CI/CD Pipeline",
        "hint": "Automate build, test, deploy.",
        "layout": [
            {"text": "CI  →  CD", "xy": [550, 180], "size": 84},
            {"text": "build → test → deploy", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "blue_green",
        "answer": "Blue-Green Deployment",
        "hint": "Two parallel environments, one live.",
        "layout": [
            {"text": "BLUE     GREEN", "xy": [550, 260], "size": 76},
            {"text": "        LIVE →", "xy": [690, 320], "size": 48}
        ]
    },
    {
        "id": "monorepo",
        "answer": "Monorepo",
        "hint": "Single repository for many projects.",
        "layout": [
            {"text": "MONO", "xy": [450, 260], "size": 96},
            {"text": "repo repo repo", "xy": [650, 340], "size": 56}
        ]
    },
    {
        "id": "zero_downtime",
        "answer": "Zero-Downtime Migration",
        "hint": "No outage while switching.",
        "layout": [
            {"text": "DB v1  →  DB v2", "xy": [550, 240], "size": 72},
            {"text": "users online: 100%", "xy": [550, 320], "size": 48}
        ]
    },
    {
        "id": "serverless",
        "answer": "Serverless",
        "hint": "You don't manage servers.",
        "layout": [
            {"text": "SERVER", "xy": [550, 240], "size": 88, "opacity": 140},
            {"text": "LESS", "xy": [550, 320], "size": 98}
        ]
    },
    {
        "id": "feature_flag",
        "answer": "Feature Flag / Toggle",
        "hint": "Switch features on/off safely.",
        "layout": [
            {"text": "FEATURE", "xy": [470, 260], "size": 72, "align": "center"},
            {"text": "ON   |   OFF", "xy": [680, 320], "size": 72, "align": "center", "underline": True}
        ]
    },
    {
        "id": "observability",
        "answer": "Observability (Logs, Metrics, Traces)",
        "hint": "See what's happening inside.",
        "layout": [
            {"text": "LOGS   METRICS   TRACES", "xy": [550, 260], "size": 60},
            {"text": "👁", "xy": [790, 260], "size": 72}
        ]
    },
    {
        "id": "token_bucket",
        "answer": "Token Bucket (Rate Limiter)",
        "hint": "Tokens fill, requests consume.",
        "layout": [
            {"text": "TOKEN TOKEN TOKEN", "xy": [550, 210], "size": 58},
            {"text": "🪣", "xy": [550, 270], "size": 72},
            {"text": "REQ → uses token", "xy": [550, 340], "size": 52}
        ]
    },
    {
        "id": "ab_test",
        "answer": "A/B Testing",
        "hint": "Two variants, measure impact.",
        "layout": [
            {"text": "A     vs     B", "xy": [550, 240], "size": 96},
            {"text": "users split 50/50", "xy": [550, 320], "size": 52}
        ]
    },
    {
        "id": "backlog_grooming",
        "answer": "Backlog Grooming / Refinement",
        "hint": "Keep the queue clean.",
        "layout": [
            {"text": "BACKLOG", "xy": [550, 240], "size": 84},
            {"text": "🧹", "xy": [710, 240], "size": 84}
        ]
    },
    {
        "id": "latency_vs_throughput",
        "answer": "Latency vs Throughput",
        "hint": "Speed per request vs total volume.",
        "layout": [
            {"text": "LATENCY  ↔  THROUGHPUT", "xy": [550, 280], "size": 64}
        ]
    },
    {
        "id": "cap_theorem",
        "answer": "CAP Theorem",
        "hint": "Consistency, Availability, Partition tolerance — pick two (with tradeoffs).",
        "layout": [
            {"text": "C   A   P", "xy": [550, 240], "size": 96},
            {"text": "tradeoffs", "xy": [550, 320], "size": 48}
        ]
    },
    {
        "id": "eventual_consistency",
        "answer": "Eventual Consistency",
        "hint": "Not immediately consistent, but becomes so over time.",
        "layout": [
            {"text": "CONSISTENCY", "xy": [550, 220], "size": 68, "opacity": 140},
            {"text": "eventually...", "xy": [550, 300], "size": 56}
        ]
    },
    {
        "id": "strong_consistency",
        "answer": "Strong Consistency",
        "hint": "Everyone sees the same data at once.",
        "layout": [
            {"text": "CONSISTENCY", "xy": [550, 260], "size": 80, "underline": True},
            {"text": "STRONG", "xy": [350, 260], "size": 64}
        ]
    },
    {
        "id": "message_queue",
        "answer": "Message Queue",
        "hint": "Buffered communication between producers and consumers.",
        "layout": [
            {"text": "producer → [ QUEUE ] → consumer", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "pub_sub",
        "answer": "Publish / Subscribe (Pub/Sub)",
        "hint": "Broadcasters and subscribers.",
        "layout": [
            {"text": "PUB → TOPIC → SUB, SUB, SUB", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "event_sourcing",
        "answer": "Event Sourcing",
        "hint": "State from a log of events.",
        "layout": [
            {"text": "event1 → event2 → event3 → state", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "cqrs",
        "answer": "CQRS (Command Query Responsibility Segregation)",
        "hint": "Split write and read models.",
        "layout": [
            {"text": "COMMAND ➜  |  ➜ QUERY", "xy": [550, 240], "size": 64},
            {"text": "write       read", "xy": [550, 320], "size": 48}
        ]
    },
    {
        "id": "sharding",
        "answer": "Sharding",
        "hint": "Horizontal data partitioning.",
        "layout": [
            {"text": "DB", "xy": [350, 240], "size": 96},
            {"text": "├── shard1  ├── shard2  ├── shard3", "xy": [700, 320], "size": 52, "align": "right"}
        ]
    },
    {
        "id": "replication",
        "answer": "Replication",
        "hint": "Copies of data across nodes.",
        "layout": [
            {"text": "PRIMARY → REPLICA → REPLICA", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "leader_election",
        "answer": "Leader Election",
        "hint": "Picking a coordinator among nodes.",
        "layout": [
            {"text": "node node node node", "xy": [550, 240], "size": 60},
            {"text": "   ↑ leader", "xy": [550, 320], "size": 48}
        ]
    },
    {
        "id": "circuit_breaker",
        "answer": "Circuit Breaker",
        "hint": "Fail fast to avoid cascading failures.",
        "layout": [
            {"text": "REQUEST → [ OPEN ] → ✖", "xy": [550, 280], "size": 64}
        ]
    },
    {
        "id": "bulkhead",
        "answer": "Bulkhead Pattern",
        "hint": "Isolate failures.",
        "layout": [
            {"text": "[ svcA ] [ svcB ] [ svcC ]", "xy": [550, 280], "size": 64}
        ]
    },
    {
        "id": "idempotency",
        "answer": "Idempotency",
        "hint": "Same request can be safely retried.",
        "layout": [
            {"text": "REQ + REQ + REQ = 1 outcome", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "saga",
        "answer": "Saga Pattern",
        "hint": "Distributed transactions with compensations.",
        "layout": [
            {"text": "Step1 → Step2 → Step3", "xy": [550, 240], "size": 56},
            {"text": "if fail: ← compensate", "xy": [550, 320], "size": 48}
        ]
    },
    {
        "id": "canary_release",
        "answer": "Canary Release",
        "hint": "Small % of users see new version first.",
        "layout": [
            {"text": "v1  v1  v1  v1   v2", "xy": [550, 260], "size": 72},
            {"text": "few see v2", "xy": [550, 330], "size": 48}
        ]
    },
    {
        "id": "error_budget",
        "answer": "Error Budget",
        "hint": "Allowed unreliability to move fast.",
        "layout": [
            {"text": "SLO: 99.9% → Budget: 0.1%", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "slo_sla",
        "answer": "SLO vs SLA",
        "hint": "Internal target vs external commitment.",
        "layout": [
            {"text": "SLO ↔ SLA", "xy": [550, 260], "size": 84},
            {"text": "target    promise", "xy": [550, 330], "size": 48}
        ]
    },
    {
        "id": "containerization",
        "answer": "Containerization",
        "hint": "Package app + deps consistently.",
        "layout": [
            {"text": "[ APP | DEPS ] → ▶", "xy": [550, 280], "size": 64}
        ]
    },
    {
        "id": "kubernetes",
        "answer": "Kubernetes",
        "hint": "Orchestrates containers.",
        "layout": [
            {"text": "pods pods pods", "xy": [550, 240], "size": 60},
            {"text": "scheduler / controller", "xy": [550, 320], "size": 48}
        ]
    },
    {
        "id": "service_mesh",
        "answer": "Service Mesh",
        "hint": "Sidecars manage networking/security.",
        "layout": [
            {"text": "svc ↔ proxy ↔ network ↔ proxy ↔ svc", "xy": [550, 280], "size": 52}
        ]
    },
    {
        "id": "graphql",
        "answer": "GraphQL",
        "hint": "Ask exactly for the data you need.",
        "layout": [
            {"text": "{ user { id name posts { id } } }", "xy": [550, 280], "size": 44}
        ]
    },
    {
        "id": "rest_api",
        "answer": "REST API",
        "hint": "Resources with verbs.",
        "layout": [
            {"text": "GET /users  POST /users/:id", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "websocket",
        "answer": "WebSocket",
        "hint": "Persistent duplex connection.",
        "layout": [
            {"text": "client ⇄ server (real‑time)", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "oauth2",
        "answer": "OAuth 2.0",
        "hint": "Delegated authorization.",
        "layout": [
            {"text": "client → auth server → token → resource", "xy": [550, 280], "size": 48}
        ]
    },
    {
        "id": "jwt",
        "answer": "JWT",
        "hint": "Signed claims as a compact token.",
        "layout": [
            {"text": "header.payload.signature", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "pagination",
        "answer": "Pagination",
        "hint": "Limit/offset or cursors.",
        "layout": [
            {"text": "← prev   page 3/10   next →", "xy": [550, 280], "size": 64}
        ]
    },
    {
        "id": "indexing",
        "answer": "Indexing",
        "hint": "Faster lookups via data structure.",
        "layout": [
            {"text": "🗂  (field) → quick find", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "acid",
        "answer": "ACID",
        "hint": "Transaction guarantees.",
        "layout": [
            {"text": "Atomic Consistent Isolated Durable", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "base",
        "answer": "BASE",
        "hint": "Eventual consistency counterpart.",
        "layout": [
            {"text": "Basically Available, Soft state, Eventual consistency", "xy": [550, 300], "size": 40}
        ]
    },
    {
        "id": "mapreduce",
        "answer": "MapReduce",
        "hint": "Parallel map then reduce.",
        "layout": [
            {"text": "map → shuffle → reduce", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "data_lake",
        "answer": "Data Lake",
        "hint": "Raw data stored at scale.",
        "layout": [
            {"text": "RAW FILES ~~~", "xy": [550, 260], "size": 72},
            {"text": "lake", "xy": [750, 320], "size": 56}
        ]
    },
    {
        "id": "data_warehouse",
        "answer": "Data Warehouse",
        "hint": "Structured, query-optimized storage.",
        "layout": [
            {"text": "FACTS + DIMENSIONS", "xy": [550, 260], "size": 60},
            {"text": "queries ↑ fast", "xy": [550, 330], "size": 48}
        ]
    },
    {
        "id": "etl",
        "answer": "ETL",
        "hint": "Extract → Transform → Load.",
        "layout": [
            {"text": "Extract → Transform → Load", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "elt",
        "answer": "ELT",
        "hint": "Extract → Load → Transform.",
        "layout": [
            {"text": "Extract → Load → Transform", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "star_schema",
        "answer": "Star Schema",
        "hint": "One fact table with dimension satellites.",
        "layout": [
            {"text": "*  fact  → dim, dim, dim", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "snowflake_schema",
        "answer": "Snowflake Schema",
        "hint": "Normalized dimensions branching.",
        "layout": [
            {"text": "fact → dim → sub-dim", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "bloom_filter",
        "answer": "Bloom Filter",
        "hint": "Probabilistic membership test.",
        "layout": [
            {"text": "might contain? probably yes / no", "xy": [550, 280], "size": 48}
        ]
    },
    {
        "id": "hyperloglog",
        "answer": "HyperLogLog",
        "hint": "Approximate distinct counting.",
        "layout": [
            {"text": "count(distinct) ≈ fast", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "tracing",
        "answer": "Distributed Tracing",
        "hint": "Trace IDs across services.",
        "layout": [
            {"text": "trace-123: svcA → svcB → svcC", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "dead_letter",
        "answer": "Dead-Letter Queue",
        "hint": "Where failed messages go.",
        "layout": [
            {"text": "QUEUE → (fail) → DLQ", "xy": [550, 280], "size": 64}
        ]
    },
    {
        "id": "retry_backoff",
        "answer": "Exponential Backoff",
        "hint": "Retry with increasing delay.",
        "layout": [
            {"text": "retry in 1s → 2s → 4s → 8s", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "throttling",
        "answer": "Throttling",
        "hint": "Slowing down heavy users.",
        "layout": [
            {"text": "limit user X to N/s", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "observability_golden",
        "answer": "Golden Signals",
        "hint": "Latency, Traffic, Errors, Saturation.",
        "layout": [
            {"text": "L  T  E  S", "xy": [550, 260], "size": 96},
            {"text": "golden signals", "xy": [550, 330], "size": 48}
        ]
    },
    {
        "id": "infra_as_code",
        "answer": "Infrastructure as Code",
        "hint": "Provision infra via code.",
        "layout": [
            {"text": "git push → cloud builds infra", "xy": [550, 280], "size": 56}
        ]
    },
    {
        "id": "shadow_traffic",
        "answer": "Shadow Traffic",
        "hint": "Mirror prod traffic to new system.",
        "layout": [
            {"text": "prod → mirror → new (no user impact)", "xy": [550, 280], "size": 48}
        ]
    },
    {
        "id": "rollforward",
        "answer": "Rollforward",
        "hint": "Fix forward instead of rollback.",
        "layout": [
            {"text": "v1 → v2 (bug) → v2.1 (fix)", "xy": [550, 280], "size": 56}
        ]
    }
]

# ------------------------------
# Scoring helpers
# ------------------------------
def init_state():
    if "puzzle_order" not in st.session_state:
        st.session_state.puzzle_order = list(range(len(PUZZLES)))
        random.shuffle(st.session_state.puzzle_order)
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "score" not in st.session_state:
        st.session_state.score = {}
    if "teams" not in st.session_state:
        st.session_state.teams = []
    if "timer_secs" not in st.session_state:
        st.session_state.timer_secs = 90
    if "show_hint" not in st.session_state:
        st.session_state.show_hint = False
    if "revealed" not in st.session_state:
        st.session_state.revealed = False

def next_puzzle():
    st.session_state.idx = (st.session_state.idx + 1) % len(PUZZLES)
    st.session_state.show_hint = False
    st.session_state.revealed = False

def prev_puzzle():
    st.session_state.idx = (st.session_state.idx - 1) % len(PUZZLES)
    st.session_state.show_hint = False
    st.session_state.revealed = False

def add_point(team_name: str):
    st.session_state.score[team_name] = st.session_state.score.get(team_name, 0) + 1

# ------------------------------
# App UI
# ------------------------------
st.set_page_config(page_title="Technical Rebus Game (50 Puzzles)", page_icon="🧩", layout="wide")
init_state()

st.title("🧩 Technical Word Puzzle — Rebus Game (50+)")
st.caption("Product & Engineering edition — guess the technical concept from the arranged words.")

with st.sidebar:
    st.header("Game Controls")
    mode = st.radio("Play as", ["Solo", "Teams"])
    if mode == "Teams":
        teams_input = st.text_input("Teams (comma-separated)", placeholder="Team Alpha, Team Beta")
        if st.button("Set Teams"):
            names = [t.strip() for t in teams_input.split(",") if t.strip()]
            if names:
                st.session_state.teams = names
                for n in names:
                    st.session_state.score.setdefault(n, 0)
    st.divider()
    st.markdown("**Round Timer**")
    st.session_state.timer_secs = st.slider("Seconds per round", min_value=15, max_value=180, value=90, step=5)
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("⬅️ Previous", on_click=prev_puzzle, use_container_width=True)
    with col_b:
        st.button("Next ➡️", on_click=next_puzzle, use_container_width=True)
    if st.button("Shuffle Order 🔀", use_container_width=True):
        random.shuffle(st.session_state.puzzle_order)
        st.session_state.idx = 0
        st.session_state.show_hint = False
        st.session_state.revealed = False
    st.divider()
    if st.button(("Show Hint 🤔" if not st.session_state.show_hint else "Hide Hint 🙈"), use_container_width=True):
        st.session_state.show_hint = not st.session_state.show_hint
    if st.button(("Reveal Answer ✅" if not st.session_state.revealed else "Hide Answer ❌"), use_container_width=True):
        st.session_state.revealed = not st.session_state.revealed

p_idx = st.session_state.puzzle_order[st.session_state.idx]
puz = PUZZLES[p_idx]

img = draw_puzzle(puz["layout"])
buf = io.BytesIO()
img.save(buf, format="PNG")
st.image(buf.getvalue(), use_column_width=True)

cols = st.columns(3)
with cols[0]:
    if st.session_state.show_hint:
        st.info(f"**Hint:** {puz['hint']}")
with cols[1]:
    st.metric("Round Timer (seconds)", value=st.session_state.timer_secs)
with cols[2]:
    st.caption(f"Puzzle {st.session_state.idx + 1} of {len(PUZZLES)}")

if st.session_state.revealed:
    st.success(f"**Answer:** {puz['answer']}")

st.divider()
st.subheader("Make a Guess")
guess = st.text_input("Type your guess here (not case-sensitive):", key=f"guess_{p_idx}")
left, right = st.columns([1,1])
with left:
    if st.button("Check Guess"):
        normalized = (guess or "").strip().lower()
        truth = puz["answer"].lower().replace('-', ' ')
        if normalized == truth or normalized.replace('-', ' ') == truth:
            st.balloons()
            st.success("Correct! 🎉")
        else:
            st.error("Not quite. Try again!")
with right:
    if st.button("Skip ➡️"):
        next_puzzle()

if mode == "Teams" and st.session_state.teams:
    st.subheader("Team Scores")
    cols = st.columns(len(st.session_state.teams))
    for i, t in enumerate(st.session_state.teams):
        with cols[i]:
            st.metric(t, st.session_state.score.get(t, 0))
            if st.button(f"+1 {t}", key=f"pt_{t}"):
                add_point(t)

st.caption("Tip: Use the sidebar to show hints, reveal answers, and navigate. Add your own puzzles in the code (PUZZLES list).")
