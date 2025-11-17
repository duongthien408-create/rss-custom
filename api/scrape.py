"""
Vercel Serverless Function để scrape TrendForce và lưu vào Supabase
Endpoint: /api/scrape
"""

from http.server import BaseHTTPRequestHandler
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from supabase_scraper import SupabaseScraper
except ImportError:
    # Fallback nếu import không được
    SupabaseScraper = None


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request - trigger scraping"""
        try:
            # Check if SupabaseScraper is available
            if SupabaseScraper is None:
                self.send_error_response(500, "SupabaseScraper not available")
                return

            # Get environment variables
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')

            if not supabase_url or not supabase_key:
                self.send_error_response(500, "Missing SUPABASE_URL or SUPABASE_KEY")
                return

            # Initialize scraper
            scraper = SupabaseScraper(supabase_url, supabase_key)

            # Scrape and save (limit to 3 pages to avoid timeout)
            result = scraper.scrape_and_save(
                start_page=1,
                end_page=3,
                table_name='trendforce_news'
            )

            # Send success response
            self.send_success_response(result)

        except Exception as e:
            self.send_error_response(500, str(e))

    def do_POST(self):
        """Handle POST request - same as GET"""
        self.do_GET()

    def send_success_response(self, result):
        """Send successful JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = {
            'success': True,
            'message': 'Scraping completed successfully',
            'data': result
        }

        self.wfile.write(json.dumps(response).encode())

    def send_error_response(self, code, message):
        """Send error JSON response"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        response = {
            'success': False,
            'error': message
        }

        self.wfile.write(json.dumps(response).encode())
