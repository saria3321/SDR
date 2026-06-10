"""
Data models for the AI SDR system
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class ICPSettings(BaseModel):
    """Ideal Customer Profile settings loaded from Google Sheets"""
    industries: List[str] = Field(default_factory=list)
    company_size_min: Optional[int] = None
    company_size_max: Optional[int] = None
    countries: List[str] = Field(default_factory=list)
    target_job_titles: List[str] = Field(default_factory=list)
    required_keywords: List[str] = Field(default_factory=list)
    seniority_levels: List[str] = Field(default_factory=list)
    departments: List[str] = Field(default_factory=list)
    company_types: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    excluded_keywords: List[str] = Field(default_factory=list)
    years_experience_min: Optional[int] = None
    years_experience_max: Optional[int] = None


class CompanyProfile(BaseModel):
    """LinkedIn company profile"""
    name: str
    linkedin_url: str
    industry: Optional[str] = None
    company_size: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class EmployeeProfile(BaseModel):
    """LinkedIn employee profile"""
    full_name: str
    job_title: str
    linkedin_url: str
    company_name: str
    company_url: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[int] = None
    seniority_level: Optional[str] = None
    department: Optional[str] = None
    years_of_experience: Optional[int] = None
    profile_summary: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ScoredLead(BaseModel):
    """Lead with AI scoring"""
    profile: EmployeeProfile
    score: int = Field(ge=0, le=100)
    reasoning: str
    date_added: str
    is_new: bool = True
