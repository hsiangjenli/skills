# Neversink Frontmatter Reference

Complete guide to slide configuration options in Neversink theme.

## Basic Frontmatter Structure

Every slide starts with YAML frontmatter between `---` markers:

```yaml
---
layout: layout-name
color: color-scheme  
# Additional options specific to layout
---
```

## Universal Options

Available on all layouts:

### `layout` (required on non-first slides)
Specifies the slide layout. See [layouts.md](layouts.md) for complete list.

### `color` (optional)
Color scheme for the slide. See [colors.md](colors.md) for available schemes.
```yaml
color: navy           # Regular color
color: amber-light    # Light variant
```

### `slide_info` (optional, default: true)
Show/hide slide numbers and navigation info.
```yaml
slide_info: false     # Hide slide numbers
```

### `title` (optional)
Alternative title for browser tab and exports.
```yaml
title: "Custom Title for This Slide"
```

## Layout-Specific Options

### Two-Column Layouts

#### `columns`
Controls left column width in 12-column grid system.
```yaml
columns: is-6         # Equal columns (6/12 and 6/12)
columns: is-4         # Left smaller (4/12 and 8/12)
columns: is-8         # Left larger (8/12 and 4/12)
```

Available values: `is-2`, `is-3`, `is-4`, `is-5`, `is-6`, `is-7`, `is-8`, `is-9`, `is-10`

#### `align`
Controls text alignment for different areas.
```yaml
align: l-lt-rt        # Left header, left-top left column, right-top right column
```

Format: `header-leftcol-rightcol`
- **Position**: `l` (left), `c` (center), `r` (right)
- **Vertical**: `t` (top), `m` (middle), `b` (bottom)

Examples:
- `l-cm-rm`: Left header, center-middle left, right-middle right
- `c-lt-lt`: Center header, left-top both columns
- `r-rb-lb`: Right header, right-bottom both columns

### Side Title Layouts

#### `side`
Position of the title area.
```yaml
side: l              # Title on left, content on right
side: r              # Title on right, content on left  
```

#### `titlewidth`
Width of the title area.
```yaml
titlewidth: is-3     # Title takes 3/12 of width
titlewidth: is-4     # Title takes 4/12 of width
titlewidth: is-5     # Title takes 5/12 of width
```

#### `titlepos` 
Position of title area (for `two-cols-title` layout).
```yaml
titlepos: t          # Title at top (default)
titlepos: b          # Title at bottom
```

### Media Layouts

#### `image`
Path to image file for image layouts.
```yaml
image: /images/photo.jpg
image: https://example.com/image.png
```

#### `url`
Website URL for iframe layouts.
```yaml
url: https://example.com
```

### Quote Layout

#### `author`
Quote attribution.
```yaml
author: "Author Name"
author: "Author Name, Title"
```

#### `quotesize` & `authorsize`
Text size using Tailwind classes.
```yaml
quotesize: text-lg    # Large quote text
authorsize: text-sm   # Small author text
```

### Credits Layout

#### `speed`
Scrolling speed (higher = faster).
```yaml
speed: 2.0           # Default speed
speed: 4.0           # Faster scrolling
speed: 1.0           # Slower scrolling
```

#### `loop`
Enable/disable looping animation.
```yaml
loop: true           # Loop continuously
loop: false          # Scroll once (default)
```

## Presentation-Level Configuration

Configure in the first slide for entire presentation:

### Theme Settings
```yaml
---
theme: neversink
colorSchema: auto     # auto, light, or dark
routerMode: hash      # URL routing mode
title: "Presentation Title"
---
```

### Custom Variables
```yaml
---
theme: neversink
neversink_string: "Custom Footer Text"  # Appears in slide footer
download: true        # Enable download button
exportFilename: "my-slides"             # Export filename
---
```

### Font and Styling
```yaml
---
theme: neversink
fonts:
  sans: 'Inter'       # Custom font family
  mono: 'Fira Code'   # Code font family
---
```

## Common Frontmatter Patterns

### Academic Presentation Slide
```yaml
---
layout: two-cols-title
columns: is-6
align: l-lt-lt  
color: navy
title: "Research Results"
---
```

### Technical Demo Slide
```yaml
---
layout: side-title
side: l
titlewidth: is-3
align: rm-lm
color: dark
slide_info: false
---
```

### Business Pitch Slide
```yaml
---
layout: top-title-two-cols
columns: is-6
align: c-lt-rt
color: blue-light
---
```

### Interactive Workshop Slide
```yaml
---
layout: full
color: light
title: "Interactive Exercise"
---
```

### Section Break
```yaml
---
layout: section
color: emerald
---
```

## Advanced Configuration

### Click Animations
Control step-by-step reveals:
```yaml
---
layout: default
clicks: 3            # Number of click steps
---
```

### Custom CSS Classes
Add custom styling:
```yaml
---
layout: default
class: my-custom-class
---
```

### Slide Transitions
```yaml
---
layout: default
transition: slide-left    # Custom transition effect
---
```

## Best Practices

### Consistency
- Use same color family throughout presentation
- Maintain consistent alignment patterns
- Keep slide_info setting consistent

### Performance  
- Minimize frontmatter options per slide
- Use image layouts instead of background images when possible
- Test complex configurations on target devices

### Accessibility
- Ensure color schemes provide sufficient contrast
- Include meaningful titles for screen readers
- Test with slide_info disabled for cleaner projection

### Maintenance
- Document custom frontmatter choices in presentation README
- Use comments in YAML for complex configurations
- Keep frontmatter options alphabetized within slides for consistency