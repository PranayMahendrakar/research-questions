#!/usr/bin/env python3
"""
Research Question Formulation Assistant - Llama-Based Academic Tool
Helps refine research questions and hypotheses
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
import json

console = Console()

RESEARCH_TYPES = ["Quantitative", "Qualitative", "Mixed Methods", "Experimental",
                  "Descriptive", "Exploratory", "Explanatory", "Case Study"]


class ResearchQuestionAssistant:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.questions = []
    
    def refine_question(self, initial_question: str, field: str) -> dict:
        prompt = f"""Help refine this research question.

Initial Question: {initial_question}
Research Field: {field}

Return JSON:
{{
    "original_question": "{initial_question}",
    "analysis": {{
        "clarity": "clear/vague/ambiguous",
        "scope": "too broad/appropriate/too narrow",
        "researchability": "easily researched/moderately/difficult",
        "originality": "novel/somewhat original/common"
    }},
    "issues_identified": [
        {{
            "issue": "problem with question",
            "explanation": "why it's a problem"
        }}
    ],
    "refined_versions": [
        {{
            "question": "improved version",
            "improvement": "what was changed",
            "research_type": "quantitative/qualitative/mixed"
        }}
    ],
    "recommended_question": "best refined version",
    "frap_analysis": {{
        "feasible": true,
        "relevant": true,
        "appropriate": true,
        "potential": true,
        "notes": "assessment notes"
    }},
    "picot_format": {{
        "population": "who",
        "intervention": "what",
        "comparison": "compared to what",
        "outcome": "expected result",
        "time": "timeframe"
    }}
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        result = self._parse_json(response['message']['content'])
        self.questions.append(result)
        return result
    
    def generate_hypotheses(self, research_question: str) -> dict:
        prompt = f"""Generate research hypotheses for this question.

Research Question: {research_question}

Return JSON:
{{
    "research_question": "{research_question}",
    "null_hypothesis": {{
        "h0": "null hypothesis statement",
        "explanation": "what it means"
    }},
    "alternative_hypotheses": [
        {{
            "h1": "hypothesis statement",
            "type": "directional/non-directional",
            "rationale": "theoretical basis",
            "testability": "how to test"
        }}
    ],
    "variables": {{
        "independent": ["IV1", "IV2"],
        "dependent": ["DV1"],
        "control": ["control variables"],
        "confounding": ["potential confounders"]
    }},
    "operationalization": {{
        "variable": "how to measure it"
    }},
    "testing_approach": "recommended statistical test or method",
    "sample_size_considerations": "power analysis notes"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def brainstorm_questions(self, topic: str, field: str) -> dict:
        prompt = f"""Brainstorm research questions for this topic.

Topic: {topic}
Field: {field}

Return JSON:
{{
    "topic": "{topic}",
    "field": "{field}",
    "research_questions": [
        {{
            "question": "research question",
            "type": "descriptive/correlational/experimental/etc",
            "feasibility": "high/medium/low",
            "potential_impact": "high/medium/low",
            "methodology_hint": "suggested approach"
        }}
    ],
    "question_categories": {{
        "descriptive": ["what/who/when questions"],
        "relational": ["how X relates to Y"],
        "causal": ["does X cause Y"],
        "comparative": ["how X differs from Y"]
    }},
    "gap_analysis": "what's missing in current research",
    "emerging_directions": ["new areas to explore"],
    "interdisciplinary_angles": ["cross-field opportunities"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def evaluate_question(self, question: str, criteria: str = "academic") -> dict:
        prompt = f"""Evaluate this research question.

Question: {question}
Evaluation Criteria: {criteria}

Return JSON:
{{
    "question": "{question}",
    "evaluation_criteria": "{criteria}",
    "scores": {{
        "clarity": {{"score": 8, "feedback": "assessment"}},
        "significance": {{"score": 7, "feedback": "assessment"}},
        "feasibility": {{"score": 6, "feedback": "assessment"}},
        "originality": {{"score": 7, "feedback": "assessment"}},
        "scope": {{"score": 8, "feedback": "assessment"}},
        "measurability": {{"score": 7, "feedback": "assessment"}}
    }},
    "overall_score": 72,
    "strengths": ["what's good about this question"],
    "weaknesses": ["areas for improvement"],
    "comparison_to_standards": "how it compares to strong research questions",
    "recommendations": ["specific improvements"],
    "verdict": "ready/needs refinement/major revision needed"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def suggest_methodology(self, question: str) -> dict:
        prompt = f"""Suggest appropriate research methodology.

Research Question: {question}

Return JSON:
{{
    "research_question": "{question}",
    "recommended_approach": "quantitative/qualitative/mixed",
    "methodology_options": [
        {{
            "methodology": "approach name",
            "description": "what it involves",
            "fit_for_question": "why it fits",
            "pros": ["advantages"],
            "cons": ["disadvantages"],
            "resources_needed": ["what you'll need"]
        }}
    ],
    "data_collection_methods": ["surveys", "interviews", "etc"],
    "analysis_methods": ["statistical tests", "thematic analysis", "etc"],
    "ethical_considerations": ["IRB", "consent", "etc"],
    "timeline_estimate": "rough timeline",
    "challenges_to_anticipate": ["potential obstacles"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def _parse_json(self, content: str) -> dict:
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"raw_response": content}


def display_menu():
    table = Table(title="🔬 Research Question Assistant", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Refine Question", "Improve your research question")
    table.add_row("2", "Generate Hypotheses", "Create testable hypotheses")
    table.add_row("3", "Brainstorm", "Generate question ideas")
    table.add_row("4", "Evaluate Question", "Score your question")
    table.add_row("5", "Suggest Methodology", "Get method recommendations")
    table.add_row("6", "View Saved", "See refined questions")
    table.add_row("0", "Exit", "Close application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]🔬 Research Question Formulation Assistant[/bold blue]\n"
        "[green]AI-Powered Research Question Refinement[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    assistant = ResearchQuestionAssistant()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Good luck with your research! 🔬[/yellow]")
            break
        
        elif choice == "6":
            if assistant.questions:
                for i, q in enumerate(assistant.questions[-3:], 1):
                    console.print(f"  {i}: {q.get('recommended_question', q.get('original_question', 'N/A'))[:60]}...")
            else:
                console.print("[dim]No saved questions.[/dim]")
            continue
        
        with console.status("[bold green]Analyzing..."):
            if choice == "1":
                question = Prompt.ask("Enter your research question")
                field = Prompt.ask("Research field", default="General")
                result = assistant.refine_question(question, field)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="✨ Refined Question"))
            
            elif choice == "2":
                question = Prompt.ask("Research question for hypotheses")
                result = assistant.generate_hypotheses(question)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📊 Hypotheses"))
            
            elif choice == "3":
                topic = Prompt.ask("Research topic")
                field = Prompt.ask("Field", default="General")
                result = assistant.brainstorm_questions(topic, field)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="💡 Question Ideas"))
            
            elif choice == "4":
                question = Prompt.ask("Question to evaluate")
                result = assistant.evaluate_question(question)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📈 Evaluation"))
            
            elif choice == "5":
                question = Prompt.ask("Research question")
                result = assistant.suggest_methodology(question)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="🔧 Methodology Suggestions"))
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
