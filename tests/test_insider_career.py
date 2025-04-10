import sys
import os
import pytest


from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage

""" Test case is:

    1. Go to Insider homepage and check accessibility
    2. Go to Careers via Company menu
    3. Check Locations, Teams, and Life at Insider sections
    4. Go to QA Careers page and click "See all QA jobs"
    5. Filter by location: Istanbul, Turkey and department: Quality Assurance
    6. Check that job listings are visible
    7. Verify each job shows QA in Position and Department, and Istanbul in Location
    8. Click "View Role" and check redirection to Lever page

"""

@pytest.mark.usefixtures("driver")
class TestInsiderCareer:

    @pytest.fixture(autouse=True)
    def setup_pages(self, driver):
        self.home_page = HomePage(driver)
        self.careers_page = CareersPage(driver)
        self.qa_careers_page = QACareersPage(driver)

    def test_insider_career_page(self):
        """
        E2E test to verify QA jobs in Istanbul are visible and accessible.

        """
        print("🚀 Opening homepage...")
        self.home_page.open()
        assert self.home_page.is_accessible()

        print("✅ Accepting cookies...")
        self.home_page.accept_cookies()

        print("✅ Navigating to careers...")
        self.home_page.navigate_to_careers()
        assert self.careers_page.is_accessible()
        assert self.careers_page.verify_sections()

        print("✅ Navigating to QA Careers...")
        self.careers_page.go_to_qa_careers()
        assert self.qa_careers_page.is_accessible()

        print("✅ Clicking 'See all QA jobs'...")
        self.qa_careers_page.click_see_all_qa_jobs()

        print("✅ Filtering jobs...")
        self.qa_careers_page.select_location_if_department_is_qa()
        self.qa_careers_page.wait_for_job_cards_to_be_replaced()
        self.qa_careers_page.wait_for_job_cards_to_load()

        print("✅ Verifying listings...")
        assert self.qa_careers_page.verify_job_listings()

        print("✅ Verifying 'View Role' redirection...")
        assert self.qa_careers_page.verify_view_role_redirects()

        print("🎉 Test completed! ✅")
