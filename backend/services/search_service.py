# backend/services/search_service.py
from typing import List, Dict, Optional


class SearchService:
    def __init__(self, restaurant_repo, item_repo):
        """
        Connects to the repository
        """
        self.repo = restaurant_repo
        self.item_repo = item_repo

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """
        Feat3-FR2: Searching
        Combines keyword matching with specific attribute filters.
        """
        if not keyword or len(keyword.strip()) < 2:
            return []

        search_term = keyword.lower().strip()

        published_restaurant_ids = {
            str(r.id) for r in self.restaurant_repo.load_all() 
            if r.is_published
        }

        all_items = self.item_repo.load_all()

        results = []
        for item in all_items:
            if str(item.restaurant_id) not in published_restaurant_ids:
                continue

            name_match = search_term in item.name.lower()
            tag_match = any(search_term in tag.lower() for tag in item.tags)

            if name_match or tag_match:
                results.append(item.model_dump())

        return results

    def get_homepage_featured(self) -> List[Dict]:
        """
        Returns a random or 'featured' selection of published items
        """
        published_ids = {str(r.id) for r in self.restaurant_repo.load_all() if r.is_published}
        all_items = self.item_repo.load_all()
        
        return [
            item.model_dump() for item in all_items 
            if str(item.restaurant_id) in published_ids
        ][:5]

