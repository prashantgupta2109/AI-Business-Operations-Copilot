import requests
import time

BASE = "http://localhost:8000"
PASS_COUNT = 0
FAIL_COUNT = 0

def test(name, fn):
    global PASS_COUNT, FAIL_COUNT
    try:
        result = fn()
        print(f"  [PASS] {name}")
        if result:
            print(f"         -> {result}")
        PASS_COUNT += 1
    except Exception as e:
        print(f"  [FAIL] {name}")
        print(f"         -> {e}")
        FAIL_COUNT += 1

print("=" * 60)
print("  AI Business Operations Copilot - Full Test Suite")
print("=" * 60)

# ─── GROUP 1: System ────────────────────────────────────────────
print("\n[ GROUP 1: System & Health ]")

def t_health():
    r = requests.get(f"{BASE}/health", timeout=5)
    d = r.json()
    assert d["status"] == "healthy", "Not healthy"
    assert d["index_ready"] is True, "Index not ready"
    assert d["total_chunks"] > 0, "No chunks in index"
    chunks = d["total_chunks"]
    doc_count = len(d["documents"])
    return f"status=healthy | chunks={chunks} | documents={doc_count}"

def t_root():
    r = requests.get(f"{BASE}/", timeout=5)
    assert r.status_code == 200
    return r.json()["message"][:60]

test("Health endpoint returns healthy status + index info", t_health)
test("Root endpoint responds with 200", t_root)

# ─── GROUP 2: Documents ─────────────────────────────────────────
print("\n[ GROUP 2: Document Management ]")

def t_list_docs():
    r = requests.get(f"{BASE}/documents/list", timeout=5)
    assert r.status_code == 200
    docs = r.json()
    assert len(docs) == 4, f"Expected 4 docs, got {len(docs)}"
    filenames = [d["filename"] for d in docs]
    for expected in ["hr_policy.txt", "company_policy.txt",
                     "financial_report_q1_2024.txt", "sop_customer_support.txt"]:
        assert expected in filenames, f"Missing: {expected}"
    total = sum(d["chunks"] for d in docs)
    return f"{len(docs)} documents | {total} total chunks"

def t_upload_doc():
    content = b"Bonus Policy: All employees receive a 10% annual bonus in December."
    r = requests.post(
        f"{BASE}/documents/upload",
        files={"file": ("test_bonus_policy.txt", content, "text/plain")},
        timeout=60,
    )
    assert r.status_code == 200
    d = r.json()
    assert "test_bonus_policy.txt" in d["message"]
    return f"Uploaded OK | total_chunks now={d['total_chunks']}"

def t_delete_doc():
    r = requests.delete(f"{BASE}/documents/test_bonus_policy.txt", timeout=60)
    assert r.status_code == 200
    d = r.json()
    assert "test_bonus_policy.txt" in d["message"]
    return "Deleted and index rebuilt successfully"

def t_reingest():
    r = requests.post(f"{BASE}/documents/reingest", timeout=60)
    assert r.status_code == 200
    d = r.json()
    assert d["documents_processed"] == 4
    assert d["total_chunks"] == 20
    return f"Re-ingested {d['documents_processed']} docs -> {d['total_chunks']} chunks"

def t_delete_nonexistent():
    r = requests.delete(f"{BASE}/documents/does_not_exist.txt", timeout=10)
    assert r.status_code == 404, f"Expected 404, got {r.status_code}"
    return "Correctly returned 404 for missing file"

test("List documents returns all 4 files with chunk counts", t_list_docs)
test("Upload new document + re-ingest succeeds", t_upload_doc)
test("Delete uploaded document + rebuild index", t_delete_doc)
test("Re-ingest all documents restores original 20 chunks", t_reingest)
test("Delete non-existent file returns 404", t_delete_nonexistent)

# ─── GROUP 3: Chat / Agent Pipeline ─────────────────────────────
print("\n[ GROUP 3: Chat & Agent Pipeline ]")
print("  (Each LLM call takes 20-60 seconds - please wait)")

def t_chat_response_structure():
    r = requests.post(
        f"{BASE}/chat/",
        json={"query": "What are the work from home rules?", "top_k": 3},
        timeout=180,
    )
    assert r.status_code == 200
    d = r.json()
    # Check all required fields are present
    assert "answer"     in d, "Missing 'answer'"
    assert "plan"       in d, "Missing 'plan'"
    assert "sources"    in d, "Missing 'sources'"
    assert "confidence" in d, "Missing 'confidence'"
    assert "timing"     in d, "Missing 'timing'"
    # Check types and quality
    assert len(d["answer"]) > 20,     "Answer too short"
    assert len(d["plan"]) >= 2,       "Plan has fewer than 2 steps"
    assert len(d["sources"]) > 0,     "No sources returned"
    assert 0 <= d["confidence"] <= 1, "Confidence out of 0-1 range"
    # Check timing has all 4 agents
    for agent in ["planner", "researcher", "executor", "reviewer"]:
        assert agent in d["timing"], f"Missing timing for {agent}"
    return f"All fields present | confidence={d['confidence']} | plan_steps={len(d['plan'])}"

def t_chat_correct_source():
    r = requests.post(
        f"{BASE}/chat/",
        json={"query": "What is the Q1 2024 revenue?", "top_k": 3},
        timeout=180,
    )
    assert r.status_code == 200
    d = r.json()
    src_files = [s["filename"] for s in d["sources"]]
    assert any("financial" in f for f in src_files), \
        f"Financial report not in sources. Got: {src_files}"
    return f"Answer: {d['answer'][:80]}... | sources={src_files}"

def t_chat_empty_query():
    r = requests.post(
        f"{BASE}/chat/",
        json={"query": "   ", "top_k": 5},
        timeout=10,
    )
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    return "Empty query correctly rejected with HTTP 400"

def t_chat_answer_contains_numbers():
    r = requests.post(
        f"{BASE}/chat/",
        json={"query": "How many paid leaves do employees get per year?", "top_k": 3},
        timeout=180,
    )
    assert r.status_code == 200
    d = r.json()
    answer_lower = d["answer"].lower()
    # Answer should mention 20 (the correct leave count from the docs)
    assert "20" in answer_lower or "twenty" in answer_lower, \
        f"Expected '20' in answer. Got: {d['answer'][:150]}"
    return f"Answer mentions '20 leaves' correctly | confidence={d['confidence']}"

test("Chat response has all required fields (answer/plan/sources/confidence/timing)", t_chat_response_structure)
test("Financial question retrieves financial_report.txt as source", t_chat_correct_source)
test("Empty query is rejected with HTTP 400 error", t_chat_empty_query)
test("Leave policy answer contains '20' (correct from docs)", t_chat_answer_contains_numbers)

# ─── SUMMARY ─────────────────────────────────────────────────────
total = PASS_COUNT + FAIL_COUNT
print()
print("=" * 60)
print(f"  RESULTS  : {PASS_COUNT}/{total} tests passed  |  {FAIL_COUNT} failed")
if FAIL_COUNT == 0:
    print("  STATUS   : ALL TESTS PASSED - Your project is working!")
else:
    print("  STATUS   : SOME TESTS FAILED - Check the [FAIL] items above")
print("=" * 60)
