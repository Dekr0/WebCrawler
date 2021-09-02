import logging

import modules.util as util
import modules.jobtype as jobtype


def main(jobs):
    writer = util.SQLUtil()
    columns_def = jobtype.IndeedJob.get_columns_def()

    if not writer.table_exist("Indeed"):
        writer.create_table("Indeed", columns_def)

    jobs_update = 0
    jobs_wrote = 0

    for job in jobs:
        info = job.get_info()
        job_id = info["Id"]
        job_company = info["Company"]
        conditions = {
            "Id": job_id,
            "Company": job_company
        }

        if writer.record_exist("Indeed", conditions):
            writer.delete_rows("Indeed", conditions)
            jobs_update += 1

        writer.insert_row("Indeed", info)
        jobs_wrote += 1

    logging.info(f"Finished writing. Number of jobs written into database : {jobs_wrote}; "
                 f"Number of jobs updated: {jobs_update}; "
                 f"Number of new jobs written into database: {jobs_wrote - jobs_update}")
    print("Finish writing")

    return