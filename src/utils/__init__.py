"""
Version information for Jobs Watcher application
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

def get_version() -> str:
    """Get application version from pyproject.toml"""
    try:
        # Get the project root directory (2 levels up from src/utils/)
        project_root = Path(__file__).parent.parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        if pyproject_path.exists():
            with open(pyproject_path, 'r') as f:
                content = f.read()
                # Simple regex to extract version
                version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if version_match:
                    return version_match.group(1)
                else:
                    logger.warning("Version not found in pyproject.toml")
                    return 'unknown'
        else:
            logger.warning(f"pyproject.toml not found at {pyproject_path}")
            return 'unknown'
            
    except Exception as e:
        logger.error(f"Failed to read version: {e}")
        return 'unknown'

def log_version():
    """Log application version on startup"""
    version = get_version()
    logger.info(f"Jobs Watcher v{version} starting up")
    return version
