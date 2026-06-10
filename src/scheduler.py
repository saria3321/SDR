"""
Job Scheduler - Run SDR pipeline on schedule
"""
import logging
import schedule
import time
from typing import Callable

logger = logging.getLogger(__name__)


class JobScheduler:
    """Schedule and run SDR jobs at intervals"""

    def __init__(self, job_func: Callable, interval_hours: int = 24):
        """
        Initialize Job Scheduler

        Args:
            job_func: Function to run on schedule
            interval_hours: Hours between runs
        """
        self.job_func = job_func
        self.interval_hours = interval_hours

    def run_once(self):
        """Run the job once immediately"""
        logger.info("Running SDR pipeline once")
        try:
            self.job_func()
            logger.info("Pipeline completed successfully")
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

    def run_scheduled(self):
        """Run the job on schedule continuously"""
        logger.info(f"Starting scheduled job (every {self.interval_hours} hours)")

        # Schedule the job
        schedule.every(self.interval_hours).hours.do(self.job_func)

        # Run immediately first time
        logger.info("Running initial job")
        try:
            self.job_func()
        except Exception as e:
            logger.error(f"Initial run failed: {e}")

        # Then run on schedule
        logger.info(f"Waiting for next run in {self.interval_hours} hours")

        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
