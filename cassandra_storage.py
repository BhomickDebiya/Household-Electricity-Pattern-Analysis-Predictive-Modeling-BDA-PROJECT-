"""
cassandra_storage.py - Cassandra Storage & Local Persistence Fallback Manager
Big Data Analytics Lab - Household Electricity Pattern Analysis & Predictive Modeling
Authors: Bhomick Debiya (Roll 32), Shorya Chilate
"""

import os
import sys
import json
import uuid
from datetime import datetime

CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "127.0.0.1")
CASSANDRA_PORT = int(os.environ.get("CASSANDRA_PORT", 9042))
KEYSPACE = "bda_electricity"

CQL_SCHEMA = """
-- 1. Create Keyspace
CREATE KEYSPACE IF NOT EXISTS bda_electricity
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

-- 2. Hourly Aggregates Table
CREATE TABLE IF NOT EXISTS bda_electricity.hourly_aggregates (
    hour int,
    avg_active_power double,
    total_records bigint,
    source text,
    created_at timestamp,
    PRIMARY KEY (hour)
);

-- 3. Model Predictions Table
CREATE TABLE IF NOT EXISTS bda_electricity.model_predictions (
    prediction_id uuid,
    hour int,
    day_of_week text,
    month int,
    predicted_load_kw double,
    created_at timestamp,
    PRIMARY KEY (prediction_id)
);
"""

def is_cassandra_available(host=CASSANDRA_HOST, port=CASSANDRA_PORT, timeout=2.0):
    """Test TCP connectivity to Cassandra native CQL port."""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

class CassandraStorageManager:
    def __init__(self, host=CASSANDRA_HOST, port=CASSANDRA_PORT):
        self.host = host
        self.port = port
        self.cluster = None
        self.session = None
        self.is_connected = False
        self.fallback_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage_fallback")
        os.makedirs(self.fallback_dir, exist_ok=True)
        self._init_connection()

    def _init_connection(self):
        if not is_cassandra_available(self.host, self.port):
            print(f"[CASSANDRA NOTICE] Cassandra service is NOT running on {self.host}:{self.port}.")
            print("  -> Active Fallback: Local Structured JSON Persistence.")
            print("  -> To run real Cassandra, launch Docker: docker run -d --name cassandra-bda -p 9042:9042 cassandra:latest")
            self.is_connected = False
            return

        try:
            from cassandra.cluster import Cluster
            self.cluster = Cluster([self.host], port=self.port)
            self.session = self.cluster.connect()
            self._create_schema()
            self.session.set_keyspace(KEYSPACE)
            self.is_connected = True
            print(f"[CASSANDRA SUCCESS] Connected to Cassandra cluster at {self.host}:{self.port}")
        except Exception as e:
            print(f"[CASSANDRA WARNING] Connection failed: {e}. Reverting to local fallback.")
            self.is_connected = False

    def _create_schema(self):
        """Create Keyspace and Tables using CQL."""
        if not self.session:
            return
        statements = [
            f"CREATE KEYSPACE IF NOT EXISTS {KEYSPACE} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}};",
            f"""CREATE TABLE IF NOT EXISTS {KEYSPACE}.hourly_aggregates (
                hour int PRIMARY KEY,
                avg_active_power double,
                total_records bigint,
                source text,
                created_at timestamp
            );""",
            f"""CREATE TABLE IF NOT EXISTS {KEYSPACE}.model_predictions (
                prediction_id uuid PRIMARY KEY,
                hour int,
                day_of_week text,
                month int,
                predicted_load_kw double,
                created_at timestamp
            );"""
        ]
        for stmt in statements:
            self.session.execute(stmt)

    def save_hourly_aggregates(self, hourly_data, source="HADOOP_MAPREDUCE"):
        """
        Save hourly aggregated active power.
        hourly_data: list of dicts [{'hour': int, 'avg_active_power': float, 'total_records': int}]
        """
        now = datetime.utcnow()
        if self.is_connected:
            insert_stmt = self.session.prepare(
                f"INSERT INTO {KEYSPACE}.hourly_aggregates (hour, avg_active_power, total_records, source, created_at) "
                "VALUES (?, ?, ?, ?, ?)"
            )
            for row in hourly_data:
                self.session.execute(insert_stmt, (
                    int(row["hour"]),
                    float(row["avg_active_power"]),
                    int(row["total_records"]),
                    str(source),
                    now
                ))
            print(f"[CASSANDRA] Successfully inserted {len(hourly_data)} hourly records into {KEYSPACE}.hourly_aggregates")
        else:
            fallback_file = os.path.join(self.fallback_dir, "hourly_aggregates_fallback.json")
            payload = {
                "storage_type": "LOCAL_FALLBACK (Cassandra Offline)",
                "keyspace_target": KEYSPACE,
                "table_target": "hourly_aggregates",
                "source": source,
                "updated_at": now.isoformat(),
                "records": hourly_data
            }
            with open(fallback_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print(f"[LOCAL FALLBACK] Saved {len(hourly_data)} hourly records to {fallback_file}")

    def save_prediction(self, hour, day_of_week, month, predicted_load_kw):
        """Save a single model prediction."""
        pred_id = uuid.uuid4()
        now = datetime.utcnow()
        if self.is_connected:
            insert_stmt = self.session.prepare(
                f"INSERT INTO {KEYSPACE}.model_predictions (prediction_id, hour, day_of_week, month, predicted_load_kw, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)"
            )
            self.session.execute(insert_stmt, (
                pred_id,
                int(hour),
                str(day_of_week),
                int(month),
                float(predicted_load_kw),
                now
            ))
            print(f"[CASSANDRA] Saved prediction {pred_id} into {KEYSPACE}.model_predictions")
        else:
            fallback_file = os.path.join(self.fallback_dir, "model_predictions_fallback.json")
            records = []
            if os.path.exists(fallback_file):
                try:
                    with open(fallback_file, "r", encoding="utf-8") as f:
                        records = json.load(f)
                except Exception:
                    records = []
            records.append({
                "prediction_id": str(pred_id),
                "hour": hour,
                "day_of_week": day_of_week,
                "month": month,
                "predicted_load_kw": round(predicted_load_kw, 4),
                "created_at": now.isoformat()
            })
            with open(fallback_file, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=2)
            print(f"[LOCAL FALLBACK] Saved prediction {pred_id} to {fallback_file}")

    def get_hourly_aggregates(self):
        """Retrieve hourly aggregates."""
        if self.is_connected:
            rows = self.session.execute(f"SELECT hour, avg_active_power, total_records, source FROM {KEYSPACE}.hourly_aggregates")
            data = [{"hour": r.hour, "avg_active_power": r.avg_active_power, "total_records": r.total_records, "source": r.source} for r in rows]
            data.sort(key=lambda x: x["hour"])
            return data
        else:
            fallback_file = os.path.join(self.fallback_dir, "hourly_aggregates_fallback.json")
            if os.path.exists(fallback_file):
                with open(fallback_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    records = content.get("records", [])
                    records.sort(key=lambda x: int(x["hour"]))
                    return records
            return []

    def close(self):
        if self.cluster:
            self.cluster.shutdown()

if __name__ == "__main__":
    print("Testing Cassandra Storage Manager...")
    mgr = CassandraStorageManager()
    
    # Test saving sample MapReduce results
    sample_data = [
        {"hour": 0, "avg_active_power": 0.6594, "total_records": 85491},
        {"hour": 20, "avg_active_power": 1.8991, "total_records": 85615}
    ]
    mgr.save_hourly_aggregates(sample_data, source="TEST_RUN")
    retrieved = mgr.get_hourly_aggregates()
    print(f"Retrieved {len(retrieved)} records.")
    mgr.close()
