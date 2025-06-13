import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timedelta
import traceback

SECURE_BUNDLE_PATH = os.getenv("ASTRA_DB_BUNDLE_PATH")
ASTRA_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE", "job_scraper")

def get_db_session():
    try:
        cloud_config = {'secure_connect_bundle': SECURE_BUNDLE_PATH}
        auth = PlainTextAuthProvider(
            os.getenv("ASTRA_DB_CLIENT_ID"),
            os.getenv("ASTRA_DB_CLIENT_SECRET")
        )
        cluster = Cluster(cloud=cloud_config, auth_provider=auth)
        session = cluster.connect()
        session.set_keyspace(ASTRA_KEYSPACE)
        return session
    except Exception:
        print("Error connecting to Astra DB:")
        print(traceback.format_exc())
        return None

def fetch_recent_jobs(hours=24):
    session = get_db_session()
    if not session:
        return []
    try:
        since = datetime.utcnow() - timedelta(hours=hours)
        result = session.execute(
            "SELECT * FROM job_postings WHERE scraped_at >= %s ALLOW FILTERING", [since]
        )
        return list(result)
    except Exception:
        print("Error fetching recent jobs:")
        print(traceback.format_exc())
        return []
