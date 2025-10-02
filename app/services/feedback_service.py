"""
Feedback service for MongoDB operations
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.db.database import get_mongodb
from app.db.mongodb_models import StudentFeedback, FeedbackCreate
from app.models.schemas import Feedback, PaginatedResponse


class FeedbackService:
    """Service class for feedback-related MongoDB operations"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.student_feedback
    
    async def get_feedback_paginated(
        self,
        page: int,
        size: int,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        feedback_type: Optional[str] = None,
        rating_min: Optional[int] = None,
        rating_max: Optional[int] = None
    ) -> PaginatedResponse:
        """Get paginated list of feedback with filtering"""
        # Build filter query
        filter_query = {}
        if student_id:
            filter_query["student_id"] = student_id
        if course_id:
            filter_query["course_id"] = course_id
        if feedback_type:
            filter_query["feedback_type"] = feedback_type
        if rating_min is not None:
            filter_query["rating"] = {"$gte": rating_min}
        if rating_max is not None:
            if "rating" in filter_query:
                filter_query["rating"]["$lte"] = rating_max
            else:
                filter_query["rating"] = {"$lte": rating_max}
        
        # Get total count
        total = await self.collection.count_documents(filter_query)
        
        # Get paginated results
        skip = (page - 1) * size
        cursor = self.collection.find(filter_query).skip(skip).limit(size)
        feedback_docs = await cursor.to_list(length=size)
        
        # Convert to Pydantic models
        feedback_list = [Feedback(**doc) for doc in feedback_docs]
        
        return PaginatedResponse(
            items=feedback_list,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    async def get_feedback_by_id(self, feedback_id: str) -> Optional[Feedback]:
        """Get feedback by ID"""
        from bson import ObjectId
        doc = await self.collection.find_one({"_id": ObjectId(feedback_id)})
        return Feedback(**doc) if doc else None
    
    async def create_feedback(self, feedback_data: FeedbackCreate) -> Feedback:
        """Create new feedback"""
        feedback_doc = feedback_data.dict()
        feedback_doc["created_at"] = datetime.utcnow()
        feedback_doc["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(feedback_doc)
        feedback_doc["_id"] = result.inserted_id
        
        return Feedback(**feedback_doc)
    
    async def get_sentiment_analysis(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        feedback_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get sentiment analysis of feedback"""
        # Build filter query
        filter_query = {}
        if student_id:
            filter_query["student_id"] = student_id
        if course_id:
            filter_query["course_id"] = course_id
        if feedback_type:
            filter_query["feedback_type"] = feedback_type
        if start_date:
            filter_query["created_at"] = {"$gte": datetime.fromisoformat(start_date)}
        if end_date:
            if "created_at" in filter_query:
                filter_query["created_at"]["$lte"] = datetime.fromisoformat(end_date)
            else:
                filter_query["created_at"] = {"$lte": datetime.fromisoformat(end_date)}
        
        # Aggregate sentiment data
        pipeline = [
            {"$match": filter_query},
            {"$group": {
                "_id": "$sentiment",
                "count": {"$sum": 1},
                "avg_rating": {"$avg": "$rating"}
            }}
        ]
        
        results = await self.collection.aggregate(pipeline).to_list(length=None)
        
        return {
            "sentiment_distribution": {result["_id"] or "unknown": result["count"] for result in results},
            "average_ratings_by_sentiment": {result["_id"] or "unknown": result["avg_rating"] for result in results}
        }
    
    async def get_feedback_trends(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        period: str = "monthly"
    ) -> Dict[str, Any]:
        """Get feedback trends over time"""
        # Build filter query
        filter_query = {}
        if student_id:
            filter_query["student_id"] = student_id
        if course_id:
            filter_query["course_id"] = course_id
        
        # Determine date grouping
        date_format = {
            "daily": "%Y-%m-%d",
            "weekly": "%Y-%U",
            "monthly": "%Y-%m"
        }.get(period, "%Y-%m")
        
        # Aggregate trends
        pipeline = [
            {"$match": filter_query},
            {"$group": {
                "_id": {
                    "$dateToString": {
                        "format": date_format,
                        "date": "$created_at"
                    }
                },
                "count": {"$sum": 1},
                "avg_rating": {"$avg": "$rating"}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        results = await self.collection.aggregate(pipeline).to_list(length=None)
        
        return {
            "period": period,
            "trends": [
                {
                    "date": result["_id"],
                    "count": result["count"],
                    "avg_rating": result["avg_rating"]
                }
                for result in results
            ]
        }
    
    async def get_rating_distribution(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        feedback_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get rating distribution analysis"""
        # Build filter query
        filter_query = {}
        if student_id:
            filter_query["student_id"] = student_id
        if course_id:
            filter_query["course_id"] = course_id
        if feedback_type:
            filter_query["feedback_type"] = feedback_type
        
        # Aggregate rating distribution
        pipeline = [
            {"$match": filter_query},
            {"$group": {
                "_id": "$rating",
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        
        results = await self.collection.aggregate(pipeline).to_list(length=None)
        
        return {
            "rating_distribution": {str(result["_id"]): result["count"] for result in results},
            "total_feedback": sum(result["count"] for result in results)
        }
    
    async def get_popular_tags(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get most popular feedback tags"""
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {
                "_id": "$tags",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        results = await self.collection.aggregate(pipeline).to_list(length=limit)
        
        return [
            {"tag": result["_id"], "count": result["count"]}
            for result in results
        ]
    
    async def bulk_import_feedback(self, feedback_list: List[FeedbackCreate]) -> Dict[str, Any]:
        """Bulk import feedback data"""
        feedback_docs = []
        for feedback_data in feedback_list:
            doc = feedback_data.dict()
            doc["created_at"] = datetime.utcnow()
            doc["updated_at"] = datetime.utcnow()
            feedback_docs.append(doc)
        
        result = await self.collection.insert_many(feedback_docs)
        
        return {
            "inserted_count": len(result.inserted_ids),
            "message": f"Successfully imported {len(result.inserted_ids)} feedback records"
        }
