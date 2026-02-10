# Tech-Slide Color System

Complete guide to using colors consistently in tech-slide presentations.

## Philosophy

**Simplicity & Clarity**: Tech presentations should focus on content, not visual complexity.

### Design Principles

1. **One Primary Color** - Establishes brand/theme identity
2. **Full-Color = Structure** - Cover, sections, conclusions use primary color
3. **No-Color = Content** - Learning content uses neutral white/black backgrounds
4. **Accents = Emphasis** - Primary color highlights important details

## Color Decision Process

### Step 1: Choose Primary Color

Select ONE color that represents your presentation's theme or topic.

| Color | When to Use | Feeling |
|-------|-------------|---------|
| **navy** | Technical, professional, enterprise | Trustworthy, stable |
| **emerald** | Environmental, growth, health | Fresh, sustainable |
| **violet** | Creative, innovative, artistic | Imaginative, unique |
| **amber** | Energy, learning, warmth | Enthusiastic, friendly |
| **pink** | Modern, approachable, design | Inclusive, contemporary |
| **sky** | Cloud, data, technology | Clear, efficient |
| **slate** | Minimal, sophisticated | Professional, clean |

**Recommendation**: Start with `navy` - it's versatile and professional.

### Step 2: Choose Color Mode

**Light Mode** (Recommended for most presentations)
- Content slides: White background
- Text: Dark text on light background
- Best for: Well-lit rooms, general audiences

**Dark Mode**
- Content slides: Black background
- Text: Light text on dark background
- Best for: Coding demos, dark rooms, developer audiences

```md
---
theme: neversink
colorSchema: light  # or 'dark' or 'auto'
---
```

### Step 3: Apply Systematically

Use this checklist for every presentation:

- [ ] Cover: `color: [PRIMARY]`
- [ ] ToC: No color
- [ ] Each Section Divider: `color: [PRIMARY]`
- [ ] All Content Slides: No color
- [ ] Key Takeaways: `color: [PRIMARY]-light`
- [ ] Accents/Callouts: `border-[PRIMARY]-500`, `bg-[PRIMARY]-50`

## Slide-by-Slide Color Guide

### 1. Cover Slide ✨ FULL-COLOR

**Purpose**: Make strong first impression, establish theme

```md
---
layout: cover
color: navy  # PRIMARY COLOR
---

# Your Presentation Title
**Subtitle or Description**

**Your Name**  
<your.email@example.com>

:: note ::
Conference Name | Date
```

**Color Variants by Mode:**
- Light mode: `navy`, `emerald`, `violet`, `amber`, `pink`, `sky`
- Dark mode: Same colors, theme adjusts automatically

### 2. Table of Contents 📋 WHITE/BLACK

**Purpose**: Provide clear navigation without distraction

```md
---
layout: default
# NO COLOR - white/black background
---

# Table of Contents

1. 📚 Background & Motivation
2. 🔧 Core Concepts
3. 💻 Implementation Guide
4. 🎯 Best Practices
5. 🔑 Key Takeaways
```

**Why no color?**
- Content should be scannable
- Reduces visual fatigue
- Maintains focus on structure

### 3. Section Dividers 🎯 FULL-COLOR

**Purpose**: Signal topic transitions, maintain context

```md
---
layout: section
color: navy  # SAME PRIMARY COLOR for ALL sections
---

# Section: Implementation Guide
<hr>

<div>

<div style="opacity: 0.4">1. 📚 Background & Motivation</div>
<div style="opacity: 0.4">2. 🔧 Core Concepts</div>
<div style="font-weight: bold">3. 💻 Implementation Guide</div>
<div style="opacity: 0.4">4. 🎯 Best Practices</div>
<div style="opacity: 0.4">5. 🔑 Key Takeaways</div>

</div>
```

**Critical Rule**: ❌ **DON'T rotate colors**

```md
❌ WRONG:
Section 1: color: emerald
Section 2: color: violet
Section 3: color: amber

✅ CORRECT:
Section 1: color: navy
Section 2: color: navy
Section 3: color: navy
```

### 4. Content Slides 📝 WHITE/BLACK

**Purpose**: Deliver learning content clearly

```md
---
layout: default
# NO COLOR - focus on content
---

# Topic: Core Principle

**Definition**: Explanation here

```python
# Code example
def example():
    pass
```

- **Key Point 1**: Detail
- **Key Point 2**: Detail
- **Key Point 3**: Detail
```

**Layouts that should have no color:**
- `layout: default`
- `layout: two-cols-title` (for content)
- `layout: image-left` / `image-right`
- `layout: top-title`
- Any slide focused on learning content

### 5. Key Takeaways 🔑 FULL-COLOR (Light Variant)

**Purpose**: Memorable conclusion, reinforce learning

```md
---
layout: two-cols-title
color: navy-light  # PRIMARY-light variant
---

:: title ::
# 🔑 Key Takeaways

:: left ::
#### Main Concepts
- **Concept A**: Summary
- **Concept B**: Summary
- **Concept C**: Summary

:: right ::
#### Next Steps
- 📖 Resources
- 💪 Exercises
- 🤝 Community
```

**Why `-light` variant?**
- Softer than section dividers
- Feels conclusive, not urgent
- Better for extended reading

### 6. Thank You / End Slide 🎉 WHITE/BLACK or LIGHT VARIANT

**Option A: White/Black (Recommended)**
```md
---
layout: default
# NO COLOR - clean ending
---

# Thank You! 🎉

<div class="text-center mt-16">
  ## Questions?
  **Your Name**  
  <your.email@example.com>
</div>
```

**Option B: Light Color (Alternative)**
```md
---
layout: cover
color: navy-light
---

# Thank You!

**Your Name**  
<your.email@example.com>
```

## Accent Colors & Highlights

Use your primary color sparingly for emphasis within content slides.

### Callout Boxes

```md
<!-- Info callout with primary color -->
<div class="p-4 border-l-4 border-navy-500 bg-navy-50 my-4">
  <div class="flex items-start gap-3">
    <div class="text-2xl">💡</div>
    <div>
      <div class="font-bold mb-1">Pro Tip</div>
      <div class="text-sm">Important information here</div>
    </div>
  </div>
</div>
```

**Color codes:**
- Border: `border-[PRIMARY]-500`
- Background: `bg-[PRIMARY]-50` (light mode) or `bg-[PRIMARY]-900` (dark mode)
- Text: `text-[PRIMARY]-600`

### Highlighted Text

```md
Important <span class="text-navy-600 font-bold">key term</span> in sentence.
```

### Sticky Notes (Neversink Theme)

```md
<StickyNote color="navy-light" x="400" y="200">
  Remember this key point!
</StickyNote>
```

### Code Highlights

```md
```python{2}
def example():
    return "This line is highlighted"  # Uses theme colors
```
```

## Color Psychology by Topic

Choose your primary color based on presentation topic:

### Technical / Enterprise
- **navy**: Reliability, professionalism
- **slate**: Minimalism, sophistication

### Development / Data
- **sky**: Clarity, technology
- **violet**: Innovation, creativity

### Environment / Health
- **emerald**: Growth, sustainability
- **green**: Nature, wellness

### Education / Training
- **amber**: Energy, learning
- **orange**: Enthusiasm, friendliness

### Design / Creative
- **pink**: Modern, approachable
- **purple**: Artistic, imaginative

## Dark Mode Adaptations

When using `colorSchema: dark`:

### Automatic Adjustments
- Content backgrounds: Black instead of white
- Text: Light instead of dark
- Colors: Automatically adjusted for contrast

### Manual Overrides (if needed)
```md
<!-- Light mode -->
<div class="bg-navy-50 text-navy-900">Light mode callout</div>

<!-- Dark mode -->
<div class="dark:bg-navy-900 dark:text-navy-100">Dark mode callout</div>
```

## Complete Examples

### Example 1: Navy Theme (Professional)

```md
---
theme: neversink
colorSchema: light
---

Slide 1 (Cover): color: navy ✨
Slide 2 (ToC): no color 📋
Slide 3 (Section 1): color: navy 🎯
Slides 4-8 (Content): no color 📝
Slide 9 (Section 2): color: navy 🎯
Slides 10-15 (Content): no color 📝
Slide 16 (Key Takeaways): color: navy-light 🔑
Slide 17 (Thank You): no color 🎉
```

### Example 2: Emerald Theme (Sustainable Tech)

```md
---
theme: neversink
colorSchema: light
---

Slide 1 (Cover): color: emerald ✨
Slide 2 (ToC): no color 📋
Slide 3 (Section 1): color: emerald 🎯
Slides 4-10 (Content): no color 📝
  - Accent: border-emerald-500, bg-emerald-50
Slide 11 (Section 2): color: emerald 🎯
Slides 12-18 (Content): no color 📝
Slide 19 (Key Takeaways): color: emerald-light 🔑
Slide 20 (Thank You): no color 🎉
```

### Example 3: Violet Theme (Creative Innovation)

```md
---
theme: neversink
colorSchema: dark
---

Slide 1 (Cover): color: violet ✨
Slide 2 (ToC): no color (black background) 📋
Slide 3 (Section 1): color: violet 🎯
Slides 4-7 (Content): no color (black background) 📝
  - Accent: border-violet-500, bg-violet-900
Slide 8 (Section 2): color: violet 🎯
Slides 9-12 (Content): no color (black background) 📝
Slide 13 (Key Takeaways): color: violet-light 🔑
Slide 14 (Thank You): no color (black background) 🎉
```

## Quick Reference Checklist

Before finalizing your presentation:

- [ ] ✅ ONE primary color chosen
- [ ] ✅ All cover slides use primary color
- [ ] ✅ All section dividers use SAME primary color
- [ ] ✅ ToC has NO color
- [ ] ✅ All content slides have NO color
- [ ] ✅ Key Takeaways uses primary-light
- [ ] ✅ Accents use primary color (border/bg)
- [ ] ✅ No color rotation between sections
- [ ] ✅ ColorSchema set (light/dark/auto)
- [ ] ✅ Consistent throughout entire deck

## Troubleshooting

### "My presentation looks too colorful"
❌ Problem: Using different colors for each section
✅ Solution: Use same primary color for ALL sections

### "Content slides are hard to read"
❌ Problem: Adding color to content slides
✅ Solution: Remove color parameter, use white/black background

### "Presentation lacks visual interest"
✅ Solution: Use more graphics, diagrams, code examples - NOT more colors

### "Need to distinguish between sections"
✅ Solution: Use section divider slides with ToC showing progress
✅ Alternative: Use slide numbers or breadcrumbs

## Summary

**Three Rules for Tech-Slide Colors:**

1. **One Color**: Choose ONE primary color for entire presentation
2. **Structure = Color**: Cover + Sections + End use primary color
3. **Content = Neutral**: All learning content uses white/black background

**Result**: Clean, professional, learner-focused presentations that let content shine.
