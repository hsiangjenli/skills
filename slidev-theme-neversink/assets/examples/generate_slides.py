#!/usr/bin/env python3
"""
Slidev Presentation Generator

Generate Slidev presentations from structured data:
- CSV data to chart slides
- JSON data to content slides
- API data to dynamic presentations
- Templates with data binding

Usage:
    uv run python generate_slides.py --data data.json --template tech --output slides.md
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime
import requests


def load_data(data_path):
    """Load data from JSON, CSV, or API endpoint."""
    # Check for HTTP URLs first before converting to Path
    if str(data_path).startswith("http"):
        # API endpoint
        try:
            response = requests.get(str(data_path), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching API data: {e}")
            sys.exit(1)

    # Convert to Path for file operations
    data_path = Path(data_path)

    if data_path.suffix.lower() == ".json":
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ Error loading JSON: {e}")
            sys.exit(1)

    elif data_path.suffix.lower() == ".csv":
        try:
            data = []
            with open(data_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)
            return data
        except FileNotFoundError as e:
            print(f"❌ Error loading CSV: {e}")
            sys.exit(1)

    else:
        print(f"❌ Unsupported data format: {data_path.suffix}")
        sys.exit(1)


def generate_chart_slide(title, data, chart_type="bar"):
    """Generate a slide with chart from data."""
    # Convert data to Mermaid chart format
    if chart_type == "bar":
        chart_data = []
        for item in data[:5]:  # Limit to 5 items for readability
            name = list(item.values())[0]
            value = list(item.values())[1]
            chart_data.append(f'    "{name}" : {value}')

        chart = f"""```mermaid
pie title {title}
{chr(10).join(chart_data)}
```"""
    else:
        # Simple table fallback
        if data:
            headers = list(data[0].keys())
            table_rows = []
            table_rows.append("| " + " | ".join(headers) + " |")
            table_rows.append("|" + "---|" * len(headers))

            for item in data[:10]:  # Limit rows
                row = []
                for header in headers:
                    row.append(str(item.get(header, "")))
                table_rows.append("| " + " | ".join(row) + " |")

            chart = "\n".join(table_rows)
        else:
            chart = "No data available"

    return f"""---
layout: default
color: sky-light
---

# {title}

{chart}

<AdmonitionType type="note">
Data generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}
</AdmonitionType>
"""


def generate_content_slide(item, layout="two-cols-title"):
    """Generate a content slide from data item."""

    title = item.get("title", item.get("name", "Content Slide"))

    if layout == "two-cols-title":
        description = item.get("description", item.get("content", ""))
        details = item.get("details", item.get("info", ""))

        return f"""---
layout: two-cols-title
columns: is-6
color: emerald-light
---

:: title ::
# {title}

:: left ::
{description}

:: right ::  
{details}
"""

    else:  # default layout
        content = item.get("content", item.get("description", ""))
        return f"""---
layout: default
---

# {title}

{content}
"""


def generate_api_slides(api_data, template_type="technical"):
    """Generate slides from API response data."""
    slides = []

    # Title slide
    api_info = api_data.get("info", {})
    title = api_info.get("title", "API Overview")
    version = api_info.get("version", "v1.0")

    title_slide = f"""---
theme: neversink
title: {title}
---

# {title}

**Version**: {version}  
**Generated**: {datetime.now().strftime("%B %d, %Y")}

:: note ::

Auto-generated from API documentation
"""
    slides.append(title_slide)

    # Endpoints slide
    endpoints = api_data.get("paths", {})
    if endpoints:
        endpoint_slide = """---
layout: default
color: navy
---

# Available Endpoints

"""
        for path, methods in list(endpoints.items())[:10]:  # Limit endpoints
            for method in methods.keys():
                endpoint_slide += f"- **{method.upper()}** `{path}`\n"

        slides.append(endpoint_slide)

    # Schema slides
    schemas = api_data.get("components", {}).get("schemas", {})
    for schema_name, schema_def in list(schemas.items())[:5]:  # Limit schemas
        properties = schema_def.get("properties", {})

        schema_slide = f"""---
layout: two-cols-title
columns: is-6
color: sky-light
---

:: title ::
# {schema_name} Schema

:: left ::
### Properties
"""
        for prop_name, prop_def in list(properties.items())[:8]:  # Limit properties
            prop_type = prop_def.get("type", "string")
            schema_slide += f"- **{prop_name}**: {prop_type}\n"

        schema_slide += """
:: right ::
### Example
```json
{
"""
        for prop_name in list(properties.keys())[:4]:  # Sample properties
            schema_slide += f'  "{prop_name}": "sample_value",\n'

        schema_slide += """}
```
"""
        slides.append(schema_slide)

    return slides


def generate_presentation(data, template_type="default", output_file="slides.md"):
    """Generate complete Slidev presentation."""
    slides = []

    # Determine data structure and generate appropriate slides
    if isinstance(data, dict):
        # Check if it's an API spec
        if "openapi" in data or "swagger" in data:
            slides = generate_api_slides(data, template_type)

        # Check if it's structured presentation data
        elif "slides" in data:
            for slide_data in data["slides"]:
                slide = generate_content_slide(slide_data)
                slides.append(slide)

        # Single object to slide
        else:
            slide = generate_content_slide(data)
            slides.append(slide)

    elif isinstance(data, list):
        # Add title slide
        title_slide = f"""---
theme: neversink
title: Data Presentation
---

# Data Overview

Generated from {len(data)} data items

---
layout: section
color: navy
---

# Data Analysis
<hr>
Insights from your data
"""
        slides.append(title_slide)

        # Generate chart slide if numeric data
        if data and any(
            k for k in data[0].keys() if str(data[0][k]).replace(".", "", 1).isdigit()
        ):
            chart_slide = generate_chart_slide("Data Distribution", data)
            slides.append(chart_slide)

        # Generate content slides
        for i, item in enumerate(data[:10]):  # Limit to prevent huge presentations
            slide = generate_content_slide(item)
            slides.append(slide)

    # Add end slide
    end_slide = (
        """---
layout: end
---

# Thank You

Questions & Discussion

---
layout: credits
color: dark
---

<div class="grid text-size-4 grid-cols-3 w-3/4 gap-y-10 auto-rows-min ml-auto mr-auto">
<div class="grid-item text-center col-span-3">
  **Data Sources & Tools**
</div>
<div class="grid-item text-right mr-4 col-span-1"><strong>Generated</strong></div>
<div class="grid-item col-span-2">Slidev + Neversink Theme<br/>Python + uv</div>
<div class="grid-item text-right mr-4 col-span-1"><strong>Date</strong></div>
<div class="grid-item col-span-2">"""
        + datetime.now().strftime("%B %d, %Y")
        + """</div>
</div>
"""
    )
    slides.append(end_slide)

    # Write slides to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(slides))

    print(f"✅ Generated presentation: {output_file}")
    print(f"📊 Created {len(slides)} slides")
    print(f"▶️  Run: npm run dev")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Slidev presentations from data"
    )
    parser.add_argument(
        "--data", "-d", required=True, help="Data source (JSON/CSV file or API URL)"
    )
    parser.add_argument(
        "--template",
        "-t",
        default="default",
        choices=["academic", "technical", "business", "default"],
        help="Presentation template type",
    )
    parser.add_argument(
        "--output", "-o", default="slides.md", help="Output slides file"
    )
    parser.add_argument(
        "--chart-type",
        default="bar",
        choices=["bar", "pie", "table"],
        help="Chart type for numeric data",
    )

    args = parser.parse_args()

    print(f"🚀 Generating Slidev presentation...")
    print(f"📄 Data source: {args.data}")
    print(f"🎨 Template: {args.template}")
    print(f"💾 Output: {args.output}")
    print()

    # Load and process data
    print("📥 Loading data...")
    data = load_data(args.data)
    print(f"✅ Loaded data successfully")

    # Generate presentation
    generate_presentation(data, args.template, args.output)

    print()
    print("💡 Next steps:")
    print("   1. Customize generated slides as needed")
    print("   2. Add images to public/images/")
    print("   3. Run 'npm run dev' to preview")


if __name__ == "__main__":
    main()
