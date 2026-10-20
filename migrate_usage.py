import json
import sqlite3
import os
import time
import glob

def migrate(usage_dir):
    jsonl_path = os.path.join(usage_dir, "usage.jsonl")
    db_path = os.path.join(usage_dir, "usage.db")
    
    print(f"Migrating {jsonl_path} to {db_path}...")
    
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            at REAL,
            iso TEXT,
            model TEXT,
            stream BOOLEAN,
            outcome TEXT,
            status INTEGER,
            message TEXT,
            elapsed_ms INTEGER,
            ttft_ms INTEGER,
            gen_ms INTEGER,
            key_id TEXT,
            key_name TEXT,
            usage_missing BOOLEAN,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            reasoning_tokens INTEGER,
            cached_tokens INTEGER,
            total_tokens INTEGER,
            credit REAL,
            account TEXT,
            realm TEXT,
            tokens_per_sec REAL,
            cache_hit_pct REAL
        )
    ''')
    
    # Indexes for fast aggregation
    conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_at ON usage_logs(at);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_realm ON usage_logs(realm);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_account ON usage_logs(account);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_key_id ON usage_logs(key_id);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_model ON usage_logs(model);")
    
    count = 0
    batch = []
    
    if os.path.exists(jsonl_path):
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    row = json.loads(line)
                except:
                    continue
                
                # Normalize
                outcome = row.get("outcome")
                if not outcome:
                    outcome = "failed" if row.get("error") else "completed"
                    
                batch.append((
                    float(row.get("at", 0)),
                    row.get("iso", ""),
                    row.get("model", "unknown"),
                    1 if row.get("stream") else 0,
                    outcome,
                    row.get("status"),
                    row.get("message"),
                    row.get("elapsed_ms"),
                    row.get("ttft_ms"),
                    row.get("gen_ms"),
                    row.get("key_id", ""),
                    row.get("key_name", ""),
                    1 if row.get("usage_missing") else 0,
                    row.get("prompt_tokens", 0),
                    row.get("completion_tokens", 0),
                    row.get("reasoning_tokens", 0),
                    row.get("cached_tokens", 0),
                    row.get("total_tokens", 0),
                    row.get("credit", 0.0),
                    row.get("account", ""),
                    row.get("realm", ""),
                    row.get("tokens_per_sec"),
                    row.get("cache_hit_pct")
                ))
                
                count += 1
                if len(batch) >= 5000:
                    conn.executemany('''
                        INSERT INTO usage_logs (
                            at, iso, model, stream, outcome, status, message, elapsed_ms, ttft_ms, gen_ms,
                            key_id, key_name, usage_missing, prompt_tokens, completion_tokens, reasoning_tokens,
                            cached_tokens, total_tokens, credit, account, realm, tokens_per_sec, cache_hit_pct
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', batch)
                    batch = []
                    print(f"Inserted {count} rows...")
                    
    if batch:
        conn.executemany('''
            INSERT INTO usage_logs (
                at, iso, model, stream, outcome, status, message, elapsed_ms, ttft_ms, gen_ms,
                key_id, key_name, usage_missing, prompt_tokens, completion_tokens, reasoning_tokens,
                cached_tokens, total_tokens, credit, account, realm, tokens_per_sec, cache_hit_pct
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', batch)
        
    conn.commit()
    conn.close()
    print(f"Migration complete. Total rows: {count}")

if __name__ == "__main__":
    migrate("/app/usage")
