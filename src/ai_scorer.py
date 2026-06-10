"""
AI Lead Scorer - Score leads using OpenRouter AI
"""
import logging
import json
from typing import Dict, Any, Tuple, List
import openai
from .models import ICPSettings, EmployeeProfile, ScoredLead
from datetime import datetime

logger = logging.getLogger(__name__)


class AIScorer:
    """Score leads against ICP using OpenRouter AI"""

    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet",
                 temperature: float = 0.3, max_tokens: int = 500):
        """
        Initialize AI Scorer

        Args:
            api_key: OpenRouter API key
            model: Model to use for scoring
            temperature: Temperature for generation
            max_tokens: Max tokens per request
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Configure OpenAI client for OpenRouter
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def score_lead(self, profile: EmployeeProfile, icp: ICPSettings) -> ScoredLead:
        """
        Score a single lead against ICP

        Args:
            profile: Employee profile to score
            icp: ICP settings

        Returns:
            ScoredLead with score and reasoning
        """
        logger.info(f"Scoring lead: {profile.full_name} at {profile.company_name}")

        prompt = self._build_scoring_prompt(profile, icp)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert B2B lead qualification specialist. "
                                 "Score leads from 0-100 based on ICP fit. Be objective and concise."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            result_text = response.choices[0].message.content
            score, reasoning = self._parse_ai_response(result_text)

            scored_lead = ScoredLead(
                profile=profile,
                score=score,
                reasoning=reasoning,
                date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_new=True
            )

            logger.info(f"Score: {score}/100 - {profile.full_name}")
            return scored_lead

        except Exception as e:
            logger.error(f"Failed to score lead {profile.full_name}: {e}")
            # Return default score on error
            return ScoredLead(
                profile=profile,
                score=0,
                reasoning=f"Error during scoring: {str(e)}",
                date_added=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_new=True
            )

    def _build_scoring_prompt(self, profile: EmployeeProfile, icp: ICPSettings) -> str:
        """Build prompt for AI scoring"""
        prompt = f"""Score this B2B lead from 0-100 based on how well they match the Ideal Customer Profile (ICP).

**LEAD PROFILE:**
- Name: {profile.full_name}
- Job Title: {profile.job_title}
- Company: {profile.company_name}
- Industry: {profile.industry or 'Unknown'}
- Company Size: {profile.company_size or 'Unknown'}
- Location: {profile.location or 'Unknown'}
- Seniority: {profile.seniority_level or 'Unknown'}
- Department: {profile.department or 'Unknown'}
- Profile Summary: {profile.profile_summary or 'Not available'}

**IDEAL CUSTOMER PROFILE (ICP):**
- Target Industries: {', '.join(icp.industries) if icp.industries else 'Any'}
- Company Size Range: {icp.company_size_min or 'Any'} - {icp.company_size_max or 'Any'} employees
- Target Countries: {', '.join(icp.countries) if icp.countries else 'Any'}
- Target Job Titles: {', '.join(icp.target_job_titles) if icp.target_job_titles else 'Any'}
- Required Keywords: {', '.join(icp.required_keywords) if icp.required_keywords else 'None'}
- Target Seniority: {', '.join(icp.seniority_levels) if icp.seniority_levels else 'Any'}
- Target Departments: {', '.join(icp.departments) if icp.departments else 'Any'}
- Company Types: {', '.join(icp.company_types) if icp.company_types else 'Any'}
- Required Languages: {', '.join(icp.languages) if icp.languages else 'Any'}
- Excluded Keywords: {', '.join(icp.excluded_keywords) if icp.excluded_keywords else 'None'}

**SCORING CRITERIA:**
1. Job Title Match (30 points): How well does the job title match target roles?
2. Company Fit (25 points): Industry, size, type, and location alignment
3. Seniority Level (20 points): Is this the right decision-maker level?
4. Department Fit (15 points): Does their department align with ICP?
5. Keywords & Signals (10 points): Required keywords present, excluded keywords absent?

**RESPONSE FORMAT:**
Score: [0-100]
Reasoning: [2-3 sentences explaining the score, highlighting matches and mismatches]

Provide your assessment:"""

        return prompt

    def _parse_ai_response(self, response_text: str) -> Tuple[int, str]:
        """Parse AI response to extract score and reasoning"""
        try:
            lines = response_text.strip().split('\n')
            score = 0
            reasoning = ""

            for line in lines:
                if line.startswith('Score:'):
                    score_str = line.replace('Score:', '').strip()
                    # Extract just the number
                    score = int(''.join(filter(str.isdigit, score_str)))
                    score = max(0, min(100, score))  # Clamp to 0-100
                elif line.startswith('Reasoning:'):
                    reasoning = line.replace('Reasoning:', '').strip()

            # If reasoning is still empty, use the whole response
            if not reasoning:
                reasoning = response_text.strip()

            return score, reasoning

        except Exception as e:
            logger.warning(f"Failed to parse AI response: {e}")
            return 50, response_text.strip()

    def score_batch(self, profiles: List[EmployeeProfile], icp: ICPSettings,
                   min_score: int = 60) -> List[ScoredLead]:
        """
        Score multiple leads and filter by minimum score

        Args:
            profiles: List of employee profiles
            icp: ICP settings
            min_score: Minimum qualifying score

        Returns:
            List of qualified scored leads
        """
        logger.info(f"Scoring {len(profiles)} leads (min score: {min_score})")

        scored_leads = []
        for profile in profiles:
            try:
                scored = self.score_lead(profile, icp)
                if scored.score >= min_score:
                    scored_leads.append(scored)
                else:
                    logger.info(f"Lead {profile.full_name} rejected with score {scored.score}")
            except Exception as e:
                logger.error(f"Error scoring {profile.full_name}: {e}")
                continue

        logger.info(f"Qualified leads: {len(scored_leads)}/{len(profiles)}")
        return scored_leads
