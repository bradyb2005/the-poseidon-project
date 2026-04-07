# backend/repositories/review_repository.py
import json
from pathlib import Path
from typing import List
from backend.schemas.review_schema import ReviewDisplay

<<<<<<< HEAD
# This is a dummy file to allow for review service to be tested

class ReviewRepository:
    def __init__(self, file_path: str = None):
=======
class ReviewRepository:
    def __init__(self, file_path: str = None):
        # Default path to backend/data/reviews.json
>>>>>>> review_repo
        if file_path:
            self._file_path = Path(file_path)
        else:
            self._file_path = Path(__file__).parent.parent / "data" / "reviews.json"
        
        if not self._file_path.parent.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> List[ReviewDisplay]:
<<<<<<< HEAD
        if not self._file_path.exists():
            return []
        try:
            with open(self._file_path, 'r') as f:
                data = json.load(f)
=======
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
    
>>>>>>> review_repo
                return [ReviewDisplay(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, reviews: List[ReviewDisplay]) -> bool:
<<<<<<< HEAD
        try:
            # mode='json' is required to serialize the 'created_at' datetime
            data = [rev.model_dump(mode='json') for rev in reviews]
=======
        """
        Writes list of ReviewDisplay objects back to JSON
        """
        try:
            # mode='json' handles the datetime serialization automatically
            data = [rev.model_dump(by_alias=True, mode='json') for rev in reviews]
>>>>>>> review_repo
            with open(self._file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except (IOError, TypeError):
            return False