import os
import uuid
import time
import psycopg2
from databricks.sdk import WorkspaceClient


class _LakebaseService:
    """Singleton service for Lakebase database connections."""
    
    _TOKEN_LIFETIME_SECONDS = 59 * 60  # 59 minutes
    
    def __init__(self):
        self._connection = None
        self._connection_time = None
    
    def _is_connection_expired(self) -> bool:
        """Check if the current connection is older than 59 minutes."""
        if self._connection_time is None:
            return True
        return (time.time() - self._connection_time) > self._TOKEN_LIFETIME_SECONDS
    
    def _create_connection(self):
        """Create a new database connection with a fresh token."""
        # Close existing connection if any
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
        
        # Initialize Databricks SDK client
        w = WorkspaceClient(
            client_id=os.getenv("DATABRICKS_CLIENT_ID"),
            client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
        )
        
        instance_name = os.getenv("LAKEBASE_INSTANCE_NAME")
        db_name = os.getenv("LAKEBASE_DB_NAME")
        db_user = "2025_vibe_coding"
        
        # Generate database credential
        cred = w.database.generate_database_credential(
            request_id=str(uuid.uuid4()),
            instance_names=[instance_name]
        )
        
        # Get instance info for the DNS
        instance = w.database.get_database_instance(name=instance_name)
        
        # Create connection
        self._connection = psycopg2.connect(
            host=instance.read_write_dns,
            dbname=db_name,
            user=db_user,
            password=cred.token,
            sslmode="require",
        )
        self._connection_time = time.time()
    
    def query(self, sql: str):
        """
        Execute a SQL query and return the results.
        
        Creates connection on first call.
        Refreshes connection if older than 59 minutes.
        """
        if self._connection is None or self._is_connection_expired():
            self._create_connection()
        
        with self._connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self._connection.commit()
            return rows


# Singleton instance
Lakebase = _LakebaseService()
