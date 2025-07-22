import csv
import json
import markdown
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from models.research_response import ResearchResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

class ResearchExporter:
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    
    def _get_filename(self, format_type: str, topic: str) -> str:
        clean_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_topic = clean_topic.replace(' ', '_')[:50]
        return f"{clean_topic}_{self.timestamp}.{format_type}"
    
    
    def export_txt(self, research: ResearchResponse, filename: Optional[str] = None) -> str:
        if not filename:
            filename = self._get_filename("txt", research.topic)
        
        filepath = self.output_dir / filename

        content = f"""Research Report: {research.topic}

Research Results:
{research.result}

Sources:
{chr(10).join(f"- {source}" for source in research.sources)}

Tools Used:
{chr(10).join(f"- {tool}" for tool in research.tools_used)}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    
    def export_json(self, research: ResearchResponse, filename: Optional[str] = None) -> str:
        if not filename:
            filename = self._get_filename("json", research.topic)
        
        filepath = self.output_dir / filename
        
        data = {
            "topic": research.topic,
            "result": research.result,
            "sources": research.sources,
            "tools_used": research.tools_used,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    
    def export_markdown(self, research: ResearchResponse, filename: Optional[str] = None) -> str:
        if not filename:
            filename = self._get_filename("md", research.topic)
        
        filepath = self.output_dir / filename
        
        content = f"""# Research Report: {research.topic}
## Research Results
{research.result}

## Sources
{chr(10).join(f"- {source}" for source in research.sources)}

## Tools Used
{chr(10).join(f"- {tool}" for tool in research.tools_used)}

<br>

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(filepath)
    
    
    def export_pdf(self, research: ResearchResponse, filename: Optional[str] = None) -> str:
        if not filename:
            filename = self._get_filename("pdf", research.topic)
        
        filepath = self.output_dir / filename
        
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=24,
            alignment=1
        )
        
        content.append(Paragraph(f"Research Report: {research.topic}", title_style))
        content.append(Spacer(1, 10))
        
        content.append(Paragraph("Research Results", styles['Heading2']))
        content.append(Spacer(1, 2))
        content.append(Paragraph(research.result, styles['Normal']))
        content.append(Spacer(1, 10))
        
        content.append(Paragraph("Sources", styles['Heading2']))
        content.append(Spacer(1, 2))
        for source in research.sources:
            content.append(Paragraph(f"• {source}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        content.append(Paragraph("Tools Used", styles['Heading2']))
        content.append(Spacer(1, 2))
        for tool in research.tools_used:
            content.append(Paragraph(f"• {tool}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor='gray',
            alignment=2
        )
        content.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))

        doc.build(content)
        
        return str(filepath)
    
    
    def export_all(self, research: ResearchResponse, formats: list[str] = None) -> Dict[str, str]:
        if formats is None:
            formats = ['txt', 'json', 'markdown', 'pdf']
        
        results = {}
        available_formats = {
            'txt': self.export_txt,
            'json': self.export_json,
            'markdown': self.export_markdown,
            'pdf': self.export_pdf
        }
        
        for fmt in formats:
            if fmt in available_formats:
                try:
                    results[fmt] = available_formats[fmt](research)
                except ImportError as e:
                    results[fmt] = f"Error: {str(e)}"
            else:
                results[fmt] = f"Error: Unsupported format '{fmt}'"
        
        return results


def export_research(research: ResearchResponse, format_type: str = "txt", output_dir: str = "exports") -> str:
    exporter = ResearchExporter(output_dir)
    
    format_mapping = {
        'txt': exporter.export_txt,
        'json': exporter.export_json,
        'markdown': exporter.export_markdown,
        'md': exporter.export_markdown,
        'pdf': exporter.export_pdf
    }
    
    if format_type not in format_mapping:
        raise ValueError(f"Unsupported format: {format_type}. Supported formats: {list(format_mapping.keys())}")
    
    return format_mapping[format_type](research)