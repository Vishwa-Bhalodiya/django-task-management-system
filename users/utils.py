from datetime import datetime
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

class Utils:
    @staticmethod
    def format_datetime(dt, fmt="%Y-%m-%d %H:%M:%S"):
        #Convert datetime object to string with given format
        if isinstance(dt, datetime):
            return dt.strftime(fmt)
        raise ValueError("Input must be a datetime object")
       
    @staticmethod
    def parse_datetime(dt_str, fmt="%Y-%m-%d %H:%M:%S"):
        """Convert string to datetime object"""
        return datetime.strptime(dt_str, fmt)

    @staticmethod
    def generate_unique_id(prefix="USR"):
        """Generate a simple unique ID"""
        return f"{prefix}-{int(datetime.utcnow().timestamp())}"

    @staticmethod
    def validate_email(email):
        """Simple email validation"""
        import re
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, email))


class ExternalAPIService:
    
    @staticmethod
    def fetch_public_apis(limit=5):
        """Fetch a list of public APIs from a mock external service"""
        
        url = "https://jsonplaceholder.typicode.com/posts"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "count": len(data[:limit]),
                "data": data[:limit]
            }

        except Timeout:
            return {
                "success": False,
                "error": "External API timeout"
            }

        except ConnectionError:
            return {
                "success": False,
                "error": "Unable to connect to external API (DNS/Network issue)"
            }

        except RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }