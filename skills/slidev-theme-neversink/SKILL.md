---
name: slidev-theme-neversink
description: Create and present web-based slides for developers using Markdown, Vue components, code highlighting, animations, and interactive features with the Neversink theme. Use for technical presentations, academic talks, conference presentations, or educational materials when users mention Slidev, Neversink theme, web presentations, or creating slides with code examples and animations.
---

# Slidev Theme Neversink

Create educational and academic presentations using the Neversink theme - a bright, flat, minimal Slidev theme with advanced layouts, color schemes, and interactive components.

## Quick Start

Basic Neversink presentation setup:

```md
---
theme: neversink
colorSchema: auto
title: Your Presentation Title
---

# Your Title Slide

Your subtitle or author information

---
layout: default
---

# Content Slide

Your content here with **bold**, *italic*, and ==highlighted== text.
```

## Core Capabilities

### 1. Layout System
Choose from 15+ specialized layouts for different content types:
- `cover` - Title slides with optional notes
- `side-title` - Side-positioned titles with content areas  
- `two-cols-title` - Header with two-column layout
- `top-title-two-cols` - Top title with two-column content
- `image-left/right` - Image with content positioning
- `section` - Section dividers with emphasis
- `quote` - Styled quotations with attribution
- `credits` - Movie-style scrolling credits
- `full` - Custom layouts with complete control

For complete layout reference, see [layouts.md](references/layouts.md).

### 2. Color Schemes
Monochromatic color pairs for visual coherence:
- **Neutrals**: `black`, `white`, `dark`, `light`, `gray`
- **Colors**: Available in regular and `-light` variants
- **Examples**: `sky`, `amber`, `emerald`, `pink`, `navy`

Apply colors in frontmatter: `color: sky-light`

### 3. Interactive Components
- **StickyNote**: Draggable sticky notes with color schemes
- **SpeechBubble**: Animated speech bubbles with positioning 
- **Admonition**: Callout boxes for notes, warnings, tips
- **IceCream**: Kawaii mascot character
- **v-drag**: Make any element draggable for custom layouts

For component examples, see [components.md](references/components.md).

### 4. Code & Animation Features
- Syntax highlighting with code focus
- Step-by-step code reveals
- Animated transitions between slides
- Live web content with iframe layouts

## Workflow Decision Tree

**New Presentation**
→ Use presentation templates in [assets/templates/](assets/templates/)
→ Academic: `academic-template.md`
→ Technical: `technical-template.md` 
→ Business: `business-template.md`

**Existing Slidev Presentation**
→ Add `theme: neversink` to frontmatter
→ Convert layouts using guidance in [layouts.md](references/layouts.md)

**Specific Features**
→ **Code demonstrations**: Use technical template with code highlighting
→ **Interactive elements**: Add components from [components.md](references/components.md)
→ **Color theming**: Apply schemes from [colors.md](references/colors.md)
→ **Advanced layouts**: Use `full` layout with custom positioning

## Common Examples

**Academic Presentation**
```bash
# Setup new presentation
npm install slidev-theme-neversink
# Use academic template from assets/templates/
```

**Technical Code Demo**
```md
---
layout: two-cols-title
color: navy
---

:: title ::
# API Integration Example

:: left ::
```python
# Code example with syntax highlighting
def fetch_data(url):
    response = requests.get(url)
    return response.json()
```

:: right ::
<StickyNote color="amber-light">
Remember to handle errors!
</StickyNote>
```

**Interactive Presentation**
```md
---
layout: full
---

<SpeechBubble position="l" color="sky" animation="float">
Your explanation here
</SpeechBubble>

<div v-drag="[100,200,300,150]">
Draggable content
</div>
```

## Resources

### scripts/
Ready-to-use utilities for Neversink presentations:
- `setup_presentation.py` - Initialize new Neversink presentation with theme setup
- `convert_layouts.py` - Convert existing Slidev layouts to Neversink equivalents
- `validate_colors.py` - Check color scheme consistency across slides

### references/
Detailed documentation loaded as needed:
- `layouts.md` - Complete layout reference with examples and frontmatter options
- `colors.md` - Color scheme guide with visual examples and use cases
- `components.md` - Interactive component library with code examples
- `animations.md` - Animation and transition patterns
- `frontmatter.md` - Configuration options and settings reference

### assets/
Ready-to-use templates and examples:
- `templates/academic-template.md` - Academic presentation starter
- `templates/technical-template.md` - Technical demo starter  
- `templates/business-template.md` - Business presentation starter
- `examples/` - Sample slides demonstrating each layout type
- `components/` - Copy-paste component examples

## Installation

Ensure Slidev is installed, then add the theme:
```bash
npm install slidev-theme-neversink
```

Add to your slides.md frontmatter:
```yaml
---
theme: neversink
---
```

## Advanced Usage

For complex presentations requiring custom layouts, animations, or extensive interactivity, consult the reference files for detailed implementation patterns and best practices.
