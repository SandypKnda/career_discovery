def filter_jobs(jobs, keywords=["remote", "aws", "etl"], exclude_locations=["India"]):
    filtered = []
    for job in jobs:
        if any(kw.lower() in (job.title or "").lower() for kw in keywords):
            if not any(loc.lower() in (job.location or "").lower() for loc in exclude_locations):
                filtered.append(job)
    return filtered
