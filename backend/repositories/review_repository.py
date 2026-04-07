# backend/repositories/review_repository.py
import json
from pathlib import Path
from typing import List
from backend.schemas.review_schema import ReviewDisplay

class ReviewRepository:
    def __init__(self, file_path: str = None):
        # Default path to backend/data/reviews.json
        if file_path:
            self._file_path = Path(file_path)
        else:
            self._file_path = Path(__file__).parent.parent / "data" / "reviews.json"
        
        if not self._file_path.parent.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> List[ReviewDisplay]:
        """
        Read JSON file and return list of ReviewDisplay objects
        """
        if not self._file_path.exists():
            return []
        
        try:
            with open(self._file_path, 'r') as f:
                data = json.load(f)
                
                if not isinstance(data, list):
                    return []
    
                return [ReviewDisplay(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, reviews: List[ReviewDisplay]) -> bool:
        """
        Writes list of ReviewDisplay objects back to JSON
        """
        try:
            # mode='json' handles the datetime serialization automatically
            data = [rev.model_dump(by_alias=True, mode='json') for rev in reviews]
            with open(self._file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except (IOError, TypeError):
            return False