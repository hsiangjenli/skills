---
name: tech-slide
description: Create educational and technical presentation slides with structured layouts including covers, table of contents, section dividers, and key takeaways. Use when building technical tutorials, workshops, or educational content with Slidev.
---

# Tech Slide

Create consistent, educational technical presentations following best practices for learning materials.

## When to Use

- Technical tutorials and workshops
- Technology introductions and demos
- Educational course materials
- Conference talks with clear learning objectives
- Documentation presentations

## Slide Structure

Every tech-slide presentation follows this structure:

1. **Cover** - Title, author, contact info
2. **Table of Contents** - Overview of all sections
3. **Sections** - Topic groupings with section ToC slides
4. **Key Takeaways** - Summary of learning points

## Quick Start

### Step 1: Choose Your Color Scheme

**IMPORTANT**: Before creating slides, decide on your presentation's color scheme.

**Questions to ask:**
1. **Primary color?** (navy, emerald, violet, amber, pink, sky, etc.)
2. **Mode?** (light mode or dark mode)

**Color usage rules:**
- **Full-color slides**: Cover, Section dividers, Key Takeaways/End slides
- **Content slides**: White (light mode) or black (dark mode) background
- **Accents**: Use primary color for callouts, sticky notes, highlights

### Step 2: Create Presentation

```md
---
theme: neversink
colorSchema: auto  # or 'light' / 'dark'
title: Your Technical Topic
author: Your Name
email: your.email@example.com
---

# Cover - Use primary color
layout: cover + color: [PRIMARY]

# Table of Contents - White/black background
layout: default (no color)

# Section Dividers - Use primary color  
layout: section + color: [PRIMARY]

# Content Slides - White/black background
layout: default (no color)

# Key Takeaways - Use primary color
layout: two-cols-title + color: [PRIMARY]-light
```

## Slide Patterns

### 1. Cover Slide

First slide with presentation metadata.

**With Neversink theme (primary color):**
```md
---
layout: cover
color: navy  # USE PRIMARY COLOR
---

# Your Technical Topic
**Complete Guide to Understanding X**

**Author Name**  
<your.email@example.com>

:: note ::
Last updated: 2026-02-09
```

**Rules:**
- ✅ Always use your chosen primary color
- ✅ This is a full-color slide
- ❌ Don't use white/black background for cover

### 2. Table of Contents

Overview of all major sections.

**Rules:**
- ✅ Use white/black background (no color parameter)
- ✅ Simple and clean layout
- ❌ Don't add color - this is content

```md
---
layout: default
# NO COLOR PARAMETER - uses default white/black
---

# Table of Contents

1. 📚 Background & Motivation
2. 🔧 Core Concepts
3. 💻 Implementation Guide
4. 🎯 Best Practices
5. 🔑 Key Takeaways
```

**With Neversink side-title (NO COLOR):**
```md
---
layout: side-title
side: l
# NO COLOR - white/black background for ToC
---

:: title ::
# ToC

:: content ::
1. 📚 Background & Motivation
2. 🔧 Core Concepts
3. 💻 Implementation Guide
4. 🎯 Best Practices
5. 🔑 Key Takeaways
```

### 3. Section Divider Slides

Mark major topic transitions with context.

**Rules:**
- ✅ Use your primary color (full-color slide)
- ✅ Always same color for all section dividers
- ❌ Don't rotate colors between sections

**Pattern:** Show full ToC with current section highlighted, others dimmed.

```md
---
layout: section
color: navy  # USE PRIMARY COLOR (same for ALL sections)
---

# Section: Core Concepts
<hr>

<div>

<div style="opacity: 0.4">1. 📚 Background & Motivation</div>
<div style="font-weight: bold">2. 🔧 Core Concepts</div>
<div style="opacity: 0.4">3. 💻 Implementation Guide</div>
<div style="opacity: 0.4">4. 🎯 Best Practices</div>
<div style="opacity: 0.4">5. 🔑 Key Takeaways</div>

</div>
```

### 4. Content Slides

Regular content slides between section dividers.

**Rules:**
- ✅ Use white/black background (no color parameter)
- ✅ Keep simple and readable
- ✅ Use primary color for accents only (callouts, highlights)
- ❌ Don't use full-color backgrounds for content

```md
---
layout: default
# NO COLOR - white/black background
---

# Your Content Title

Content here with **bold**, *italic*, and ==highlighted== text.

- Bullet points
- More items

<div class="p-4 border-l-4 border-navy-500 bg-navy-50">
  💡 **Tip**: Use primary color for callouts
</div>
```

### 5. Key Takeaways

Final slide summarizing learning objectives.

**Rules:**
- ✅ Use `default` layout (no color or white/black background)
- ✅ Keep it simple with a single list
- ✅ Limit to 3-5 key points
- ✅ Make it memorable and actionable

```md
---
layout: default
---

# 🔑 Key Takeaways

Main learnings from this presentation:

- **Concept A**: Core understanding gained from this topic
- **Concept B**: Key skill or technique learned
- **Concept C**: Important principle or best practice
- **Next Steps**: Continue learning with documentation and practice
- **Community**: Join discussions and share your experience
```

## Complete Example

See [assets/templates/basic-tech-slide.md](assets/templates/basic-tech-slide.md) for full presentation template.

## Color System Summary

### Full-Color Slides (Use Primary Color)
1. **Cover** - `layout: cover` + `color: [PRIMARY]`
2. **Section Dividers** - `layout: section` + `color: [PRIMARY]`
3. **Key Takeaways** - `layout: two-cols-title` + `color: [PRIMARY]-light`
4. **Thank You/End** - Optional: use primary color

### White/Black Background Slides (No Color)
1. **Table of Contents** - `layout: default` (no color)
2. **All Content Slides** - `layout: default` or `two-cols-title` (no color)
3. **Regular Slides** - Any layout without color parameter

### Accent Usage (Primary Color)
Use your primary color for:
- Callout boxes borders: `border-navy-500`
- Callout backgrounds: `bg-navy-50` (light) or `bg-navy-900` (dark)
- Sticky notes: `<StickyNote color="navy-light">`
- Important highlights
- Links and interactive elements

**Example:**
```md
# Content Slide (white/black background)

<div class="p-4 border-l-4 border-navy-500 bg-navy-50">
  💡 **Tip**: This uses primary color as accent
</div>
```

## Advanced Patterns

### Thank You / End Slide

Final slide to close the presentation.

**Rules:**
- ✅ Use `section` layout with primary color for visual impact
- ✅ Center-align everything
- ✅ Keep it simple - just "Thank You"
- ✅ Optionally add QR code for feedback survey
- ❌ Don't add contact info or extra text

```md
---
layout: section
color: navy  # USE PRIMARY COLOR
---

<div style="text-align: center">

# Thank You! 🎉

</div>
```

**With optional QR code for survey:**
```md
---
layout: section
color: navy  # USE PRIMARY COLOR
---

<div style="text-align: center">

# Thank You! 🎉

<div style="margin-top: 3rem; display: flex; flex-direction: column; align-items: center">

<QRCode value="https://your-survey-link.com" :size="200" render-as="svg" />

<div style="margin-top: 1rem">

**Scan for feedback survey**

</div>

</div>

</div>
```

**Notes:**
- QR Code is commented out by default - uncomment when needed
- Replace `https://your-survey-link.com` with actual survey URL
- Adjust `:size` if needed (default 200 works well)

### Multi-level ToC

For complex presentations with subsections:

```md
# Section: Implementation Guide

<div style="opacity: 0.4">1-2. Previous sections</div>

**3. 💻 Implementation Guide**
  - 3.1 Setup Environment
  - 3.2 Basic Usage ← Current
  - 3.3 Advanced Features

<div style="opacity: 0.4">4-5. Upcoming sections</div>
```

### Progress Indicators

Show progress through section:

```md
---
layout: default
---

# Current Topic <span style="float: right; opacity: 0.6">Section 2/5 | Slide 12/45</span>

Content here...
```

### Interactive Key Takeaways

Reveal takeaways progressively:

```md
# Key Takeaways

<v-clicks>

- **First Key Point**: Explanation
- **Second Key Point**: Explanation  
- **Third Key Point**: Explanation

</v-clicks>
```

For more advanced techniques, see [references/advanced-patterns.md](references/advanced-patterns.md).

## Layout Format Rules

### Critical: two-cols-title Content Placement

**IMPORTANT**: When using `two-cols-title` layout, ALL content MUST be placed inside the `:: left ::` and `:: right ::` sections to maintain consistent spacing in PDF exports.

❌ **WRONG** - Content outside sections causes spacing issues:
```md
---
layout: two-cols-title
---

:: title ::
# My Title

This text is outside sections (BAD - causes PDF spacing issues)

:: left ::
Left content

:: right ::
Right content
```

✅ **CORRECT** - All content in sections:
```md
---
layout: two-cols-title
---

:: title ::
# My Title

:: left ::
All your left content here

:: right ::
All your right content here
```

**Why this matters:**
- Different layouts (`default` vs `two-cols-title`) have different CSS styling
- Content placement affects spacing in PDF exports
- Keeping content in designated sections ensures uniform spacing across all slides

### Consistent Spacing Tips

1. **Choose spacing solution**: Either add descriptions after h1 (recommended) or use CSS to unify spacing
2. **Title descriptions**: Use on `default` layout only, not in `two-cols-title` title sections
3. **Empty lines**: Keep consistent number of blank lines after headings within same layout type
4. **Element order**: Place similar elements (code blocks, lists) in same order for predictable spacing
5. **Two-column layouts**: Always use `two-cols-title` layout instead of manual `<div class="grid grid-cols-2">` for consistency

### Spacing Best Practice

**Problem**: Different elements (lists, code blocks, tables, quotes) have different default margins when placed directly after h1.

**Solution 1: Add Description (Recommended)**

✅ Add a brief sentence after h1 to provide context AND ensure consistent spacing:

```md
# Title One
Brief description of this section.

- List items

---
# Title Two
Brief description of this section.

```python
code block
\`\`\`
```

**Benefits:**
- Uniform spacing across all slides
- Provides valuable context
- Better readability

**Solution 2: CSS Override (If No Descriptions Wanted)**

If you need h1 directly followed by content without descriptions, add CSS to your slides:

```md
---
theme: neversink
---

<style>
/* Ensure consistent spacing after h1 regardless of element type */
.slidev-layout h1 + p,
.slidev-layout h1 + ul,
.slidev-layout h1 + ol,
.slidev-layout h1 + pre,
.slidev-layout h1 + blockquote,
.slidev-layout h1 + table,
.slidev-layout h1 + div,
.slidev-layout h1 + .v-clicks,
.slidev-layout h1 + .v-click {
  margin-top: 2rem !important;
}
</style>

---
# Title
- List directly after h1
```

**Benefits:**
- Clean h1 without descriptions
- Consistent spacing via CSS
- Works for all element types

**Choose based on your needs:**
- Educational content → Use Solution 1 (descriptions provide learning value)
- Minimal slides → Use Solution 2 (CSS only)

### Layout Selection Guide

**Use `two-cols-title` for:**
- Side-by-side comparisons (Before/After, Do's/Don'ts)
- Text + diagram combinations
- Code + explanation pairs
- Any content needing two columns

❌ **Do NOT use manual grid:**
```md
# Wrong - Manual grid
<div class="grid grid-cols-2 gap-8">
  <div>Left content</div>
  <div>Right content</div>
</div>
```

✅ **Use layout instead:**
```md
---
layout: two-cols-title
---

:: title ::
# My Title

:: left ::
Left content

:: right ::
Right content
```

## Color Decision Workflow

**STEP 1: Choose Primary Color**
Select ONE color for your entire presentation:
- `navy` - Professional, technical (recommended)
- `emerald` - Growth, eco-friendly
- `violet` - Creative, innovative
- `amber` - Warm, energetic
- `pink` - Friendly, modern
- `sky` - Clear, tech-focused

**STEP 2: Choose Mode**
- **Light mode**: White backgrounds for content, lighter color variants
- **Dark mode**: Black backgrounds for content, darker color variants

**STEP 3: Apply Consistently**

| Slide Type | Color | Example |
|------------|-------|---------|
| Cover | Primary color | `color: navy` |
| ToC | No color (white/black) | (no color parameter) |
| Section Dividers | Primary color | `color: navy` |
| Content Slides | No color (white/black) | (no color parameter) |
| Key Takeaways | Primary-light | `color: navy-light` |
| Accents | Primary color | `border-navy-500` |

**Example: Navy theme**
```md
Cover: color: navy
Sections: color: navy (all sections same)
Key Takeaways: color: navy-light
Content: no color
Accents: border-navy-500, bg-navy-50
```

## Best Practices

1. **ONE primary color throughout** - Don't rotate colors between sections
2. **Clean content slides** - Use white/black backgrounds, not colors
3. **Keep ToC consistent** - Use same numbering/emojis throughout
4. **Section dividers every 8-12 slides** - Prevent information overload
5. **Limit to 3-5 major sections** - Stay focused on core learning objectives
6. **Key Takeaways = 3-5 points** - More is forgettable
7. **Use visual hierarchy** - Bold current section, dim others with opacity 0.3-0.5
8. **Include contact info** - Make it easy for learners to reach out

## Resources

- `assets/templates/` - Ready-to-use presentation templates with unified color scheme
- `references/color-system.md` - Detailed color system guide
- `references/advanced-patterns.md` - Complex ToC and section patterns
- `references/styling-guide.md` - CSS and UnoCSS utilities for tech-slides