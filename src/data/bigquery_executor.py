from google.cloud import bigquery

class BigQueryExecutor:
    def __init__(self, project: str):
        self.client = bigquery.Client(project=project)

    def execute(self, sql: str):
        query_job = self.client.query(sql)
        results = query_job.result()
        return [dict(row) for row in results]
