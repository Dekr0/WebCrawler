import logging

import modules.util as util
import modules.jobtype as jobtype


def main(jobs):
    writer = util.SQLUtil("Indeed")
    columnType = jobtype.IndeedJob.getColumnType()

    writer.createTable(columnType)

    updatedJobs = 0
    jobsWritten = 0

    for job in jobs:
        info = job.getJobInfo()
        id = info["Id"]
        company = info["Company"]
        conditions = {
            "Id": id,
            "Company": company
        }

        if writer.hasRecord(conditions):
            writer.deleteRow(conditions)
            updatedJobs += 1

        writer.insertRow(info)
        jobsWritten += 1

    logging.info(f"Finished writing. Number of jobs written into database : {jobsWritten}; "
                 f"Number of jobs updated: {updatedJobs}; "
                 f"Number of new jobs written into database: {jobsWritten - updatedJobs}")
    print("Finish writing")

    return