# Neversink Layout Reference

Complete guide to all available layouts in the Slidev Neversink theme.

## Layout Categories

### Title & Cover Layouts

#### `cover`
Full-screen title slide with optional note section.
```md
---
layout: cover
color: amber  # optional
---

# Your Presentation Title

**Author Name**  
_Organization_ <a href="https://example.com">🔗</a>

:: note ::
Optional note at bottom
```

#### `intro`
Simplified title slide with less decoration.
```md
---
layout: intro
color: emerald-light
---

# Presentation Title
**Author Name**  
_Organization_

Brief description or subtitle text.
```

### Content Layouts

#### `default`
Standard content slide with markdown support.
```md
---
layout: default
color: sky  # optional
---

# Slide Title

Content with **bold**, *italic*, and ==highlighted== text.

- Bullet points
- More items
```

#### `section`
Section divider with emphasis and colored hr.
```md
---
layout: section
color: navy
---

# Section Title
<hr>
Optional description text
```

### Two-Column Layouts

#### `two-cols-title`
Header with customizable two-column layout below.
```md
---
layout: two-cols-title
columns: is-6        # Left column width (1-11)
align: l-lt-lt       # Header-Left-Right alignment
color: violet
---

:: title ::
# Header Content

:: left ::
Left column content

:: right ::
Right column content
```

##### Column Options (`columns`)
- `is-2` to `is-10` - Sets left column width
- Remaining space goes to right column
- `is-6` = equal columns

##### Alignment (`align`)
Format: `header-left-right`
- Position: `l`(left), `c`(center), `r`(right)  
- Vertical: `t`(top), `m`(middle), `b`(bottom)
- Example: `l-cm-rt` = left header, center-middle left, right-top right

#### `top-title-two-cols`
Top title with two columns below.
```md
---
layout: top-title-two-cols
columns: is-6
align: l-lt-lt
color: amber-light
---

:: title ::
# Title At Top

:: left ::
Left content

:: right ::
Right content
```

### Side Title Layouts

#### `side-title`
Title positioned on left or right side.
```md
---
layout: side-title
side: l              # 'l' or 'r'
titlewidth: is-4     # Title area width
align: rm-lm         # Title-Content alignment
color: pink-light
---

:: title ::
# Side Title

:: content ::
Main content area
```

#### `top-title`
Title at top with content below.
```md
---
layout: top-title
color: navy
align: l             # Title alignment
---

:: title ::
# Top Title

:: content ::
Content area below title
```

### Media Layouts

#### `image-left` / `image-right`
Image with content positioning.
```md
---
layout: image-right
image: /path/to/image.png
slide_info: false    # Hide slide numbers
---

# Content Title
Content appears opposite to image
```

#### `image`
Full-screen image layout.
```md
---
layout: image
image: /path/to/image.png
title: Optional Title
---
```

### Web Content Layouts

#### `iframe-left` / `iframe-right` / `iframe`
Live web content embedding.
```md
---
layout: iframe-right
url: https://example.com
slide_info: false
---

# Website Demo
Live website content on right
```

### Special Layouts

#### `quote`
Styled quotation with attribution.
```md
---
layout: quote
color: sky-light
quotesize: text-lg    # Quote text size  
authorsize: text-sm   # Author text size
author: "Author Name"
---

"Your quote text here with proper styling and attribution handling."
```

#### `credits`
Movie-style scrolling credits.
```md
---
layout: credits
color: navy
speed: 2.0           # Scroll speed
loop: true           # Loop animation
---

<div class="grid text-size-4 grid-cols-3">
  <!-- Credits content in grid format -->
</div>
```

#### `full`
Complete control with no default structure.
```md
---
layout: full
---

<div class="h-full w-full">
  <!-- Custom layout with absolute positioning -->
  <StickyNote v-drag="[100,200,300,150]">
    Custom positioned content
  </StickyNote>
</div>
```

#### `fact`
Special emphasis layout for key facts.
```md
---
layout: fact
color: emerald
---

# Key Statistic
Large emphasis content
```

#### `end`
Conclusion slide styling.
```md
---
layout: end
---

# Thank You
Questions?
```

## Layout Selection Guide

**Title slides**: `cover` (formal) or `intro` (casual)
**Content**: `default` (simple) or `two-cols-title` (structured)  
**Comparisons**: `two-cols-title` or `top-title-two-cols`
**Sections**: `section` for breaks
**Media**: `image-right/left` for visual content
**Demos**: `iframe-right/left` for live websites
**Custom**: `full` for complete control
**Special**: `quote` (quotations), `credits` (acknowledgments)

## Common Frontmatter Options

```yaml
---
layout: layout-name
color: scheme-name     # Color scheme (optional)
slide_info: false      # Hide slide numbers (optional)
align: l-cm-rt         # Alignment (layout-specific)
columns: is-6          # Column widths (two-col layouts)
side: l                # Side positioning (side layouts)
---
```