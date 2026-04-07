# backend/repositories/review_repository.py
import json
from pathlib import Path
from typing import List
from backend.schemas.review_schema import ReviewDisplay

# This is a dummy file to allow for review service to be tested

class ReviewRepository:
    def __init__(self, file_path: str = None):
        if file_path:
            self._file_path = Path(file_path)
        else:
            self._file_path = Path(__file__).parent.parent / "data" / "reviews.json"
        
        if not self._file_path.parent.exists():
            self._file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> List[ReviewDisplay]:
        if not self._file_path.exists():
            return []
        try:
            with open(self._file_path, 'r') as f:
                data = json.load(f)
                return [ReviewDisplay(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_all(self, reviews: List[ReviewDisplay]) -> bool:
        try:
            # mode='json' is required to serialize the 'created_at' datetime
            data = [rev.model_dump(mode='json') for rev in reviews]
            with open(self._file_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except (IOError, TypeError):
            return False