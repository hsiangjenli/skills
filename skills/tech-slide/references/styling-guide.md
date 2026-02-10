# Tech-Slide Styling Guide

CSS utilities and styling patterns for consistent, professional tech presentations.

## Color System (IMPORTANT!)

Tech-slide follows a **unified color system** for clean, readable presentations.

### Core Principle: One Primary Color

**Choose ONE primary color** for your entire presentation. Common choices:
- `navy` - Professional, technical (recommended)
- `emerald` - Growth, sustainability  
- `violet` - Creative, innovative
- `amber` - Warm, energetic
- `pink` - Friendly, approachable
- `sky` - Clean, tech-focused

### Color Application Rules

#### Full-Color Slides (Use Primary Color)
These slides should use your primary color completely:

1. **Cover Slide**
   ```md
   ---
   layout: cover
   color: navy  # Your primary color
   ---
   ```

2. **Section Dividers** (ALL use same color)
   ```md
   ---
   layout: section
   color: navy  # Same primary color for ALL sections
   ---
   ```

3. **Key Takeaways / End Slides**
   ```md
   ---
   layout: two-cols-title
   color: navy-light  # Primary with -light variant
   ---
   ```

#### White/Black Background Slides (No Color)
These slides should NOT have color parameters:

1. **Table of Contents**
   ```md
   ---
   layout: default
   # NO COLOR PARAMETER
   ---
   ```

2. **All Content Slides**
   ```md
   ---
   layout: default
   # NO COLOR - keeps white (light mode) or black (dark mode)
   ---
   ```

3. **Two-Column Content**
   ```md
   ---
   layout: two-cols-title
   # NO COLOR for content slides
   ---
   ```

#### Accent Usage (Subtle Primary Color)
Use your primary color for highlights and callouts:

```md
<!-- Callout box with primary color accent -->
<div class="p-4 border-l-4 border-navy-500 bg-navy-50">
  💡 **Tip**: Important information
</div>

<!-- Highlighted text -->
<span class="text-navy-600 font-bold">Key term</span>

<!-- Sticky note (Neversink) -->
<StickyNote color="navy-light">
  Remember this!
</StickyNote>
```

### ❌ Common Mistakes to Avoid

1. **DON'T rotate colors between sections**
   ```md
   ❌ Section 1: color: emerald
   ❌ Section 2: color: violet
   ❌ Section 3: color: amber
   ```
   
2. **DON'T add color to content slides**
   ```md
   ❌ layout: default + color: sky
   ```
   
3. **DON'T use multiple primary colors**
   ```md
   ❌ Cover: navy, Sections: emerald, End: amber
   ```

### ✅ Correct Pattern Example

```md
# Presentation with Navy Primary Color

Cover: color: navy
ToC: (no color - white background)
Section 1: color: navy
Content slides: (no color - white background)
Section 2: color: navy
Content slides: (no color - white background)
Key Takeaways: color: navy-light
Thank You: (no color - white background with navy accents)
```

## Opacity Hierarchy

Use opacity to create visual hierarchy in navigation elements:

```md
<!-- Completed sections -->
<div style="opacity: 1; color: #10b981">✓ Completed Section</div>

<!-- Current section -->
<div style="opacity: 1; font-weight: bold">→ Current Section</div>

<!-- Upcoming sections (light dimming) -->
<div style="opacity: 0.6">Upcoming Section</div>

<!-- Future sections (heavy dimming) -->
<div style="opacity: 0.3">Future Section</div>
```

**Recommended opacity values:**
- `1.0` - Current/active item
- `0.8` - Important but secondary
- `0.6` - Context/background
- `0.4` - De-emphasized
- `0.3` - Very subtle

## UnoCSS Utility Classes

Slidev includes UnoCSS (similar to TailwindCSS). Use these classes in your slides:

### Typography

```md
<!-- Text sizes -->
<div class="text-xs">Extra small</div>
<div class="text-sm">Small</div>
<div class="text-base">Base</div>
<div class="text-lg">Large</div>
<div class="text-xl">Extra large</div>
<div class="text-2xl">2X large</div>
<div class="text-4xl">4X large</div>

<!-- Font weights -->
<div class="font-light">Light text</div>
<div class="font-normal">Normal text</div>
<div class="font-bold">Bold text</div>

<!-- Font styles -->
<div class="italic">Italic text</div>
<div class="not-italic">Not italic</div>
```

### Colors

```md
<!-- Text colors -->
<div class="text-blue-600">Blue text</div>
<div class="text-green-600">Green text</div>
<div class="text-red-600">Red text</div>
<div class="text-gray-600">Gray text</div>

<!-- Background colors -->
<div class="bg-blue-100">Light blue background</div>
<div class="bg-blue-500">Blue background</div>
<div class="bg-blue-900">Dark blue background</div>
```

**Color scales:** 50, 100, 200, 300, 400, 500, 600, 700, 800, 900
**Available colors:** gray, red, orange, amber, yellow, lime, green, emerald, teal, cyan, sky, blue, indigo, violet, purple, fuchsia, pink, rose

### Spacing

```md
<!-- Margins -->
<div class="m-4">Margin all sides</div>
<div class="mt-4">Margin top</div>
<div class="mb-8">Margin bottom</div>
<div class="mx-auto">Horizontal center</div>

<!-- Padding -->
<div class="p-4">Padding all sides</div>
<div class="px-6">Padding horizontal</div>
<div class="py-2">Padding vertical</div>

<!-- Gaps (for flex/grid) -->
<div class="flex gap-4">Items with gaps</div>
<div class="grid gap-8">Grid with gaps</div>
```

**Spacing scale:** 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32

### Layout

```md
<!-- Flexbox -->
<div class="flex">Flex container</div>
<div class="flex items-center">Vertically centered</div>
<div class="flex justify-between">Space between</div>
<div class="flex-col">Column direction</div>

<!-- Grid -->
<div class="grid grid-cols-2 gap-4">Two columns</div>
<div class="grid grid-cols-3 gap-6">Three columns</div>
<div class="grid grid-cols-1 md:grid-cols-2">Responsive grid</div>
```

### Borders

```md
<!-- Border sides -->
<div class="border">All borders</div>
<div class="border-l-4">Left border, 4px</div>
<div class="border-t-2">Top border, 2px</div>

<!-- Border colors -->
<div class="border border-blue-500">Blue border</div>
<div class="border-2 border-green-600">Thick green border</div>

<!-- Rounded corners -->
<div class="rounded">Slightly rounded</div>
<div class="rounded-lg">Large rounded</div>
<div class="rounded-full">Fully rounded</div>
```

## Section-Specific Styling

### Cover Slide

```md
---
layout: cover
---

<div class="text-center">
  <h1 class="text-6xl font-bold mb-4">Main Title</h1>
  <h2 class="text-2xl opacity-80 mb-8">Subtitle</h2>
  <div class="text-lg">
    <strong>Author Name</strong><br>
    <span class="opacity-70">your.email@example.com</span>
  </div>
</div>
```

### Table of Contents

```md
<div class="text-xl space-y-3">
  <div class="flex items-center gap-3">
    <span class="text-3xl">📚</span>
    <span>Background & Motivation</span>
  </div>
  <div class="flex items-center gap-3">
    <span class="text-3xl">🔧</span>
    <span>Core Concepts</span>
  </div>
  <div class="flex items-center gap-3">
    <span class="text-3xl">💻</span>
    <span>Implementation Guide</span>
  </div>
</div>
```

### Section Dividers

```md
<div class="grid grid-cols-1 gap-3 text-lg max-w-xl mx-auto">
  <div class="opacity-30 flex items-center gap-2">
    <span class="text-2xl">1.</span>
    <span>Background & Motivation</span>
  </div>
  
  <div class="flex items-center gap-2 text-2xl font-bold text-blue-600">
    <span>2.</span>
    <span>Core Concepts</span>
    <span class="ml-2">←</span>
  </div>
  
  <div class="opacity-30 flex items-center gap-2">
    <span class="text-2xl">3.</span>
    <span>Implementation Guide</span>
  </div>
</div>
```

### Key Takeaways Cards

```md
<div class="grid grid-cols-3 gap-6 mt-8">
  <div class="p-6 border-2 border-blue-500 rounded-lg bg-blue-50">
    <div class="text-4xl mb-4">🎯</div>
    <h3 class="font-bold text-lg mb-2">Concept A</h3>
    <p class="text-sm opacity-80">Brief explanation here</p>
  </div>
  
  <div class="p-6 border-2 border-green-500 rounded-lg bg-green-50">
    <div class="text-4xl mb-4">💪</div>
    <h3 class="font-bold text-lg mb-2">Skill B</h3>
    <p class="text-sm opacity-80">Brief explanation here</p>
  </div>
  
  <div class="p-6 border-2 border-amber-500 rounded-lg bg-amber-50">
    <div class="text-4xl mb-4">⚡</div>
    <h3 class="font-bold text-lg mb-2">Practice C</h3>
    <p class="text-sm opacity-80">Brief explanation here</p>
  </div>
</div>
```

## Progress Indicators

### Progress Bar

```md
<div class="flex gap-2 w-full max-w-md mx-auto">
  <div class="h-2 flex-1 bg-green-500 rounded"></div>
  <div class="h-2 flex-1 bg-green-500 rounded"></div>
  <div class="h-2 flex-1 bg-blue-500 rounded"></div>
  <div class="h-2 flex-1 bg-gray-300 rounded"></div>
  <div class="h-2 flex-1 bg-gray-300 rounded"></div>
</div>
<div class="text-center text-sm mt-2 opacity-60">
  Section 3 of 5
</div>
```

### Circular Progress

```md
<div class="flex justify-center gap-4">
  <div class="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center text-white">
    ✓
  </div>
  <div class="w-12 h-12 rounded-full bg-green-500 flex items-center justify-center text-white">
    ✓
  </div>
  <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white">
    3
  </div>
  <div class="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center">
    4
  </div>
  <div class="w-12 h-12 rounded-full bg-gray-300 flex items-center justify-center">
    5
  </div>
</div>
```

## Callout Boxes

### Info Callout

```md
<div class="p-4 border-l-4 border-blue-500 bg-blue-50 my-4">
  <div class="flex items-start gap-3">
    <div class="text-2xl">ℹ️</div>
    <div>
      <div class="font-bold mb-1">Information</div>
      <div class="text-sm">Additional context or explanation</div>
    </div>
  </div>
</div>
```

### Warning Callout

```md
<div class="p-4 border-l-4 border-amber-500 bg-amber-50 my-4">
  <div class="flex items-start gap-3">
    <div class="text-2xl">⚠️</div>
    <div>
      <div class="font-bold mb-1">Warning</div>
      <div class="text-sm">Important consideration or caveat</div>
    </div>
  </div>
</div>
```

### Tip Callout

```md
<div class="p-4 border-l-4 border-green-500 bg-green-50 my-4">
  <div class="flex items-start gap-3">
    <div class="text-2xl">💡</div>
    <div>
      <div class="font-bold mb-1">Pro Tip</div>
      <div class="text-sm">Best practice or helpful hint</div>
    </div>
  </div>
</div>
```

## Responsive Design

```md
<!-- Hide on small screens, show on medium+ -->
<div class="hidden md:block">Desktop only content</div>

<!-- Show on small screens, hide on medium+ -->
<div class="block md:hidden">Mobile only content</div>

<!-- Responsive columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  Responsive grid
</div>

<!-- Responsive text sizes -->
<h1 class="text-2xl md:text-4xl lg:text-6xl">
  Responsive heading
</h1>
```

## Animation Classes

```md
<!-- Fade in -->
<div class="animate-fade-in">Fades in</div>

<!-- Slide in from left -->
<div class="animate-slide-in-left">Slides from left</div>

<!-- Bounce -->
<div class="animate-bounce">Bounces</div>

<!-- With v-click -->
<div v-click class="transition duration-500">
  Smooth transition on click
</div>
```

## Custom CSS

Add custom styles in frontmatter:

```md
---
layout: default
---

<style>
.highlight-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.section-number {
  font-size: 120px;
  font-weight: 900;
  opacity: 0.1;
  position: absolute;
  top: 1rem;
  right: 2rem;
}
</style>

<div class="section-number">02</div>
<div class="highlight-box">Custom styled content</div>
```

## Best Practices

1. **Consistency**: Use same opacity values throughout presentation
2. **Contrast**: Ensure sufficient contrast for readability (WCAG AA: 4.5:1)
3. **Spacing**: Use consistent spacing scale (4, 8, 16, 24, 32px)
4. **Colors**: Stick to 2-3 main colors plus neutrals
5. **Typography**: Use 2-3 font sizes for hierarchy
6. **Animations**: Keep subtle; don't distract from content

## Theme-Specific Considerations

When using Neversink theme, prefer:
- Frontmatter color options: `color: navy`
- Built-in layouts over custom styling
- Theme components (StickyNote, SpeechBubble)

When using default theme:
- Rely more on custom CSS and utility classes
- Use HTML/CSS for layout control
- Reference Slidev's global CSS variables
