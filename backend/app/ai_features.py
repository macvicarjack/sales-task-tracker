"""
AI Features for Sales Task Tracker
This module demonstrates how AI could enhance the application
"""

import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class AITaskAnalyzer:
    """AI-powered task analysis and insights"""
    
    def __init__(self):
        self.priority_keywords = {
            'urgent': 10,
            'asap': 9,
            'critical': 8,
            'important': 7,
            'follow up': 6,
            'meeting': 5,
            'proposal': 4,
            'quote': 3
        }
        
        self.revenue_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # $1,000 or $1,000.00
            r'[\d,]+(?:\.\d{2})?\s*(?:dollars?|USD)',  # 1000 dollars
            r'[\d,]+(?:\.\d{2})?\s*(?:k|K)',  # 50k
            r'[\d,]+(?:\.\d{2})?\s*(?:million|M)',  # 1M
        ]
    
    def extract_revenue(self, text: str) -> float:
        """Extract revenue potential from text using regex patterns"""
        text = text.lower()
        max_revenue = 0.0
        
        for pattern in self.revenue_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean and convert to float
                clean_match = re.sub(r'[^\d.]', '', match)
                if clean_match:
                    value = float(clean_match)
                    # Handle k (thousands) and M (millions)
                    if 'k' in match.lower():
                        value *= 1000
                    elif 'm' in match.lower() or 'million' in match.lower():
                        value *= 1000000
                    max_revenue = max(max_revenue, value)
        
        return max_revenue
    
    def calculate_ai_priority(self, task_data: Dict) -> Dict:
        """Calculate AI-enhanced priority score"""
        title = task_data.get('title', '').lower()
        description = task_data.get('description', '').lower()
        full_text = f"{title} {description}"
        
        # Base priority from keywords
        keyword_score = 0
        for keyword, score in self.priority_keywords.items():
            if keyword in full_text:
                keyword_score += score
        
        # Revenue-based scoring
        revenue = task_data.get('revenue_potential', 0)
        revenue_score = min(revenue / 1000, 50)  # Cap at 50 points
        
        # Time-based urgency
        due_date = task_data.get('due_date')
        time_score = 0
        if due_date:
            days_until_due = (due_date - datetime.now().date()).days
            if days_until_due < 0:
                time_score = 30  # Overdue
            elif days_until_due <= 3:
                time_score = 25  # Due soon
            elif days_until_due <= 7:
                time_score = 15  # Due this week
        
        # Status bonus
        status = task_data.get('status', 'open')
        status_score = 20 if status == 'open' else 0
        
        # Calculate total AI priority
        ai_priority = keyword_score + revenue_score + time_score + status_score
        
        return {
            'ai_priority_score': ai_priority,
            'keyword_score': keyword_score,
            'revenue_score': revenue_score,
            'time_score': time_score,
            'status_score': status_score,
            'insights': self.generate_insights(task_data, ai_priority)
        }
    
    def generate_insights(self, task_data: Dict, priority_score: float) -> List[str]:
        """Generate AI insights about the task"""
        insights = []
        
        # Revenue insights
        revenue = task_data.get('revenue_potential', 0)
        if revenue > 10000:
            insights.append("High-value opportunity - prioritize accordingly")
        elif revenue > 5000:
            insights.append("Medium-value deal - good ROI potential")
        
        # Time insights
        due_date = task_data.get('due_date')
        if due_date:
            days_until_due = (due_date - datetime.now().date()).days
            if days_until_due < 0:
                insights.append("⚠️ Task is overdue - immediate attention needed")
            elif days_until_due <= 3:
                insights.append("🚨 Due soon - consider escalating")
        
        # Status insights
        status = task_data.get('status', 'open')
        if status == 'open' and priority_score > 50:
            insights.append("High-priority open task - consider starting soon")
        
        # Account insights
        account = task_data.get('account', '')
        if account and len(account) > 0:
            insights.append(f"Account: {account} - review account history")
        
        return insights
    
    def suggest_next_actions(self, task_data: Dict) -> List[str]:
        """Suggest next actions based on task data"""
        suggestions = []
        
        status = task_data.get('status', 'open')
        if status == 'open':
            suggestions.append("Schedule initial contact")
            suggestions.append("Prepare proposal/quote")
            suggestions.append("Research account information")
        elif status == 'in-progress':
            suggestions.append("Follow up on previous communication")
            suggestions.append("Schedule next meeting")
            suggestions.append("Prepare next steps")
        
        return suggestions

class AISalesPredictor:
    """AI-powered sales predictions and forecasting"""
    
    def predict_closure_probability(self, task_data: Dict) -> float:
        """Predict probability of task/opportunity closing"""
        # This would use historical data and ML models
        # For now, using simple heuristics
        
        base_probability = 0.5
        
        # Revenue impact
        revenue = task_data.get('revenue_potential', 0)
        if revenue > 10000:
            base_probability += 0.2
        elif revenue > 5000:
            base_probability += 0.1
        
        # Time impact
        due_date = task_data.get('due_date')
        if due_date:
            days_until_due = (due_date - datetime.now().date()).days
            if days_until_due > 30:
                base_probability -= 0.1  # Far future = lower probability
            elif days_until_due <= 7:
                base_probability += 0.1  # Near term = higher probability
        
        # Status impact
        status = task_data.get('status', 'open')
        if status == 'in-progress':
            base_probability += 0.2
        elif status == 'closed':
            base_probability = 1.0
        
        return min(max(base_probability, 0.0), 1.0)
    
    def forecast_revenue(self, tasks: List[Dict]) -> Dict:
        """Forecast total revenue from all tasks"""
        total_potential = sum(task.get('revenue_potential', 0) for task in tasks)
        
        # Calculate weighted revenue based on closure probability
        weighted_revenue = 0
        for task in tasks:
            probability = self.predict_closure_probability(task)
            weighted_revenue += task.get('revenue_potential', 0) * probability
        
        return {
            'total_potential': total_potential,
            'weighted_forecast': weighted_revenue,
            'confidence_interval': (weighted_revenue * 0.8, weighted_revenue * 1.2)
        }

# Example usage
if __name__ == "__main__":
    analyzer = AITaskAnalyzer()
    predictor = AISalesPredictor()
    
    # Example task
    sample_task = {
        'title': 'Follow up with ABC Corp on $50k deal',
        'description': 'Urgent proposal needed for new software implementation',
        'revenue_potential': 50000,
        'due_date': datetime.now().date() + timedelta(days=5),
        'status': 'open',
        'account': 'ABC Corporation'
    }
    
    # AI analysis
    ai_analysis = analyzer.calculate_ai_priority(sample_task)
    closure_prob = predictor.predict_closure_probability(sample_task)
    
    print(f"AI Priority Score: {ai_analysis['ai_priority_score']}")
    print(f"Closure Probability: {closure_prob:.1%}")
    print(f"Insights: {ai_analysis['insights']}") 