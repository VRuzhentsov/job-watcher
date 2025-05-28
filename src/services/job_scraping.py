"""
Job Scraping Service using JobSpy
"""

import logging
from typing import Dict, List, Optional
from jobspy import scrape_jobs
import pandas as pd

logger = logging.getLogger(__name__)

class JobScrapingService:
    """Service to handle job scraping using JobSpy"""
    
    def __init__(self):
        self.default_site_name = ["indeed"]
        self.max_results = 20  # Limit results for Telegram display
    
    async def search_jobs(
        self, 
        search_term: str, 
        location: str | None = None,
        site_name: List[str] | None = None
    ) -> Dict:
        """
        Search for jobs using JobSpy
        
        Args:
            search_term: Job search keywords
            location: Job location (city, state/province)
            site_name: List of job sites to search

        Returns:
            Dict with jobs data or error info
        """
        try:
            # Use defaults if not provided
            if site_name is None:
                site_name = self.default_site_name
                logger.info(f"🔍 Searching jobs: '{search_term}' in '{location}' from {site_name}")
            
            # Determine country based on location
            country_indeed = 'usa'  # default
            if location:
                location_lower = location.lower()
                # Check for Canadian indicators
                if any(indicator in location_lower for indicator in [
                    ', on', ', ontario', ', bc', ', british columbia', ', ab', ', alberta', 
                    ', qc', ', quebec', ', ns', ', nova scotia', ', nb', ', new brunswick',
                    ', mb', ', manitoba', ', sk', ', saskatchewan', ', pe', ', prince edward island',
                    ', nl', ', newfoundland', ', yt', ', yukon', ', nt', ', northwest territories',
                    ', nu', ', nunavut', 'canada', 'canadian'
                ]):
                    country_indeed = 'canada'
                    logger.info(f"Detected Canadian location, using country_indeed='canada'")

            # Search using JobSpy
            jobs_df = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                location=location,
                results_wanted=self.max_results,
                country_indeed=country_indeed,
                hours_old=2  # Search jobs posted in last 2 hours
            )
            
            if jobs_df.empty:
                return {
                    'success': False,
                    'message': f"No jobs found for '{search_term}' in '{location}'"
                }
            
            # Convert to list of dictionaries for easy handling
            jobs_list = jobs_df.to_dict('records')
            
            logger.info(f"✅ Found {len(jobs_list)} jobs")
            
            return {
                'success': True,
                'jobs': jobs_list,
                'count': len(jobs_list),
                'search_term': search_term,
                'location': location
            }
            
        except Exception as e:
            logger.error(f"❌ Job search failed: {e}")
            return {
                'success': False,
                'message': f"Search failed: {str(e)}"
            }
    
    def format_job_for_telegram(self, job: Dict, index: int) -> str:
        """
        Format a single job posting for Telegram display
        
        Args:
            job: Job dictionary from JobSpy
            index: Job number for display
            
        Returns:
            Formatted string for Telegram
        """
        try:
            title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            location = job.get('location', 'N/A')
            job_url = job.get('job_url', '')
            site = job.get('site', 'N/A')
            date_posted = job.get('date_posted', 'N/A')
            
            # Format job posting
            message = f"**{index}. {title}**\n"
            message += f"🏢 {company}\n"
            message += f"📍 {location}\n"
            message += f"🌐 {site.title()}\n"
            
            if date_posted != 'N/A':
                message += f"📅 {date_posted}\n"
            
            if job_url:
                message += f"🔗 [Apply Here]({job_url})\n"
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting job: {e}")
            return f"{index}. Error formatting job data"
    
    def format_jobs_summary(self, result: Dict) -> str:
        """
        Format jobs search results for Telegram
        
        Args:
            result: Result dictionary from search_jobs
            
        Returns:
            Formatted string for Telegram
        """
        if not result.get('success'):
            return f"❌ {result.get('message', 'Search failed')}"
        
        jobs = result.get('jobs', [])
        search_term = result.get('search_term', '')
        location = result.get('location', '')
        count = result.get('count', 0)
        
        if not jobs:
            return f"No jobs found for '{search_term}' in '{location}'"
        
        # Header
        header = f"🔍 **Search Results**\n"
        header += f"**Query**: {search_term}\n"
        if location:
            header += f"**Location**: {location}\n"
        header += f"**Found**: {count} jobs\n\n"
        
        # Format first few jobs (limit for Telegram message size)
        max_display = 5
        jobs_text = ""
        for i, job in enumerate(jobs[:max_display], 1):
            jobs_text += self.format_job_for_telegram(job, i)
            jobs_text += "\n"
        
        if len(jobs) > max_display:
            jobs_text += f"... and {len(jobs) - max_display} more jobs\n"
        
        return header + jobs_text
