# Neversink Color Schemes

Comprehensive guide to the Tailwind-based monochromatic color system in Neversink.

## Color System Overview

Neversink uses monochromatic pairs that provide both background and text colors for visual coherence. Each color comes in regular and `-light` variants.

## Available Color Schemes

### Neutral Colors

#### Black & White
- `black` - Pure black background, white text
- `white` - Pure white background, black text  
- `dark` - Dark gray (800) background, light gray (100) text
- `light` - Light gray (100) background, dark gray (800) text

#### Grays
- `slate` / `slate-light` - Cool gray tones
- `gray` / `gray-light` - True gray 
- `zinc` / `zinc-light` - Warm gray
- `neutral` / `neutral-light` - Balanced gray
- `stone` / `stone-light` - Warm beige-gray

### Color Palettes

#### Warm Colors
- `red` / `red-light` - Bold, attention-grabbing
- `orange` / `orange-light` - Energetic, creative
- `amber` / `amber-light` - Warm, academic
- `yellow` / `yellow-light` - Bright, optimistic

#### Cool Colors  
- `lime` / `lime-light` - Fresh, natural
- `green` / `green-light` - Growth, success
- `emerald` / `emerald-light` - Sophisticated green
- `teal` / `teal-light` - Calming, professional
- `cyan` / `cyan-light` - Technical, modern

#### Blues
- `sky` / `sky-light` - Bright, friendly
- `blue` / `blue-light` - Trust, corporate
- `indigo` / `indigo-light` - Deep, serious
- `navy` / `navy-light` - Professional, academic

#### Purples & Pinks
- `violet` / `violet-light` - Creative, artistic
- `purple` / `purple-light` - Royal, luxury  
- `pink` / `pink-light` - Playful, approachable
- `rose` / `rose-light` - Elegant, soft
- `fuchsia` / `fuchsia-light` - Bold, modern

## Usage Examples

### Slide Color Application
```md
---
layout: cover
color: navy
---
# Professional Title
```

### Component Color Matching
```md
<StickyNote color="amber-light">
Matches amber-light slide theme
</StickyNote>

<SpeechBubble color="sky">  
Bright blue bubble
</SpeechBubble>
```

## Color Selection Guide

### By Presentation Type

**Academic/Research**
- `navy`, `indigo`, `slate` - Professional, serious
- `amber-light`, `emerald-light` - Warm, approachable

**Technical/Developer**  
- `dark`, `navy`, `slate` - Clean, focused
- `cyan`, `blue`, `green` - Tech-friendly

**Creative/Design**
- `violet`, `pink`, `rose` - Artistic, expressive  
- `amber`, `orange` - Warm, inspiring

**Business/Corporate**
- `blue`, `navy`, `neutral` - Trustworthy, professional
- `emerald`, `teal` - Growth, stability

**Educational/Training**
- `sky-light`, `green-light`, `amber-light` - Friendly, accessible
- `orange`, `lime` - Energetic, engaging

### By Content Type

**Title Slides**: Bolder colors (`navy`, `emerald`, `amber`)
**Content Slides**: Lighter variants (`sky-light`, `green-light`)  
**Section Breaks**: High contrast (`dark`, `navy`, `indigo`)
**Code Demos**: Neutral backgrounds (`dark`, `slate`, `gray`)
**Interactive Elements**: Bright accents (`pink`, `cyan`, `lime`)

### Color Combinations

**Professional Palette**
- Title: `navy`
- Content: `slate-light`
- Accents: `blue`

**Warm Academic**  
- Title: `amber`
- Content: `amber-light`
- Accents: `orange`

**Modern Tech**
- Title: `dark` 
- Content: `gray-light`
- Accents: `cyan`

**Creative Friendly**
- Title: `violet`
- Content: `pink-light`  
- Accents: `rose`

## Component Color Matching

### Sticky Notes
```md
<!-- Match slide color -->
---
color: emerald-light
---

<StickyNote color="emerald-light">
Cohesive with slide theme
</StickyNote>
```

### Speech Bubbles
```md
<!-- Contrasting accent -->
---  
color: navy
---

<SpeechBubble color="amber">
Stands out against navy background
</SpeechBubble>
```

### Admonitions
```md
<!-- Information hierarchy -->
<AdmonitionType type="note">        <!-- Blue -->
<AdmonitionType type="important">    <!-- Red -->
<AdmonitionType type="warning">      <!-- Yellow -->
<AdmonitionType type="tip">          <!-- Green -->
```

## Color Psychology

### Blue Family (`sky`, `blue`, `navy`)
- **Emotion**: Trust, stability, professionalism
- **Use for**: Corporate, academic, technical content
- **Avoid**: Creative presentations, emotional content

### Green Family (`lime`, `green`, `emerald`, `teal`)  
- **Emotion**: Growth, harmony, freshness
- **Use for**: Environmental, health, success stories
- **Avoid**: Warning messages, financial loss topics

### Red Family (`red`, `rose`, `pink`)
- **Emotion**: Energy, passion, urgency
- **Use for**: Calls to action, important points, creative work
- **Avoid**: Calming content, detailed technical information

### Purple Family (`violet`, `purple`, `fuchsia`)
- **Emotion**: Creativity, luxury, innovation  
- **Use for**: Artistic content, premium products, creative industries
- **Avoid**: Conservative business, traditional academics

### Neutral Family (`black`, `white`, `gray`, `slate`)
- **Emotion**: Clean, professional, timeless
- **Use for**: Any content, backgrounds, text-heavy slides
- **Avoid**: When brand colors are required

## Best Practices

1. **Consistency**: Use 2-3 related colors maximum per presentation
2. **Hierarchy**: Darker colors for titles, lighter for content  
3. **Contrast**: Ensure text remains readable on colored backgrounds
4. **Context**: Match colors to audience expectations and content type
5. **Testing**: Preview slides in presentation mode to verify legibility