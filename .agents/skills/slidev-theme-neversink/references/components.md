# Neversink Interactive Components

Guide to custom components that make presentations interactive and engaging.

## Core Components

### StickyNote

Draggable sticky note component with color theming.

#### Basic Usage
```md
<StickyNote color="amber-light" textAlign="left" width="200px">
Your **markdown** note content here.
</StickyNote>
```

#### Properties
- `color`: Any Neversink color scheme (`amber-light`, `sky`, `pink-light`, etc.)
- `width`: Fixed width (recommended for draggable notes)
- `textAlign`: `left`, `center`, `right`
- `title`: Optional title text
- `customTitle`: CSS classes for title styling
- `custom`: CSS classes for note body styling

#### Advanced Example
```md
<StickyNote 
  color="emerald-light" 
  width="250px" 
  title="Important Note"
  customTitle="font-size-6"
  custom="font-size-3"
  v-drag="[100,200,250,180]">
  
This note has custom styling and positioning.
</StickyNote>
```

### SpeechBubble

Animated speech bubbles for dialogue and explanations.

#### Basic Usage
```md
<SpeechBubble position="l" color="sky" shape="round">
Hello! I'm a **speech bubble** with markdown support.
</SpeechBubble>
```

#### Properties  
- `position`: Arrow direction - `l`, `r`, `bl`, `br`, `t`, `b`
- `color`: Neversink color scheme
- `shape`: `round` (recommended) or `square`
- `animation`: `float`, `bounce`, or none
- `width`: Optional fixed width

#### Positioning Guide
- `l`: Arrow points left (bubble to right of target)
- `r`: Arrow points right (bubble to left of target)  
- `bl`: Arrow points bottom-left (bubble above-right)
- `br`: Arrow points bottom-right (bubble above-left)

#### Animation Example
```md
<SpeechBubble 
  position="r" 
  color="pink-light" 
  animation="float"
  v-drag="[300,150,280,100]">

I'm floating and draggable!
</SpeechBubble>
```

### Admonition & AdmonitionType

Callout boxes for important information.

#### Custom Admonitions
```md
<Admonition title="Custom Title" color="teal-light" width="300px">
Custom admonition with your content and color scheme.
</Admonition>
```

#### Predefined Types
```md
<AdmonitionType type="note">
This is informational content in blue styling.
</AdmonitionType>

<AdmonitionType type="important">
Critical information in red styling.
</AdmonitionType>

<AdmonitionType type="warning">
Caution message in yellow styling.
</AdmonitionType>

<AdmonitionType type="tip">
Helpful suggestion in green styling.
</AdmonitionType>

<AdmonitionType type="caution">
Be careful message with custom styling options.
</AdmonitionType>
```

#### Custom Styling
```md
<AdmonitionType 
  type="caution" 
  custom="text-lg" 
  customTitle="font-size-6">
Large text with big title.
</AdmonitionType>
```

### IceCream

Kawaii mascot character for playful presentations.

#### Usage
```md
<IceCream 
  :size="150" 
  mood="lovestruck" 
  color="#FDA7DC" 
  v-drag="[400,300,85,150]" />
```

#### Properties
- `size`: Pixel size (number)
- `mood`: Character expression (see theme docs for options)
- `color`: Hex color code
- `v-drag`: Position array `[x, y, width, height]`

## Positioning System

### v-drag Directive

Make any element draggable and positioned absolutely.

#### Syntax
```md
v-drag="[x, y, width, height, rotation]"
```

- `x`: X position in pixels from left
- `y`: Y position in pixels from top  
- `width`: Element width in pixels
- `height`: Element height in pixels
- `rotation`: Rotation in degrees (optional)

#### Examples
```md
<!-- Basic positioning -->
<div v-drag="[100, 200, 300, 150]">
Positioned content block
</div>

<!-- With rotation -->
<StickyNote color="pink" v-drag="[50,50,200,100,-15]">
Tilted sticky note
</StickyNote>

<!-- Multiple positioned elements -->
<div class="h-full w-full">
  <SpeechBubble position="l" color="sky" v-drag="[100,100,250,80]">
    First bubble
  </SpeechBubble>
  
  <SpeechBubble position="r" color="amber" v-drag="[400,200,250,80]">
    Second bubble
  </SpeechBubble>
</div>
```

## Component Combinations

### Interactive Dialogue
```md
---
layout: full
---

<IceCream :size="120" mood="happy" color="#FDA7DC" v-drag="[100,300,120,120]" />

<SpeechBubble position="r" color="pink-light" v-drag="[250,250,280,100]">
Hello! I'm here to **explain** this concept.
</SpeechBubble>

<SpeechBubble position="l" color="sky-light" v-drag="[50,150,280,80]">
That's very helpful, thanks!
</SpeechBubble>
```

### Annotated Diagram
```md
---
layout: full  
---

<!-- Background image or diagram -->
<img src="/diagram.png" class="w-full h-full object-contain" />

<!-- Annotations -->
<StickyNote color="amber-light" v-drag="[100,100,200,120]">
**Step 1**: Initialize the process
</StickyNote>

<StickyNote color="green-light" v-drag="[400,200,200,120]">  
**Step 2**: Process the data
</StickyNote>

<StickyNote color="blue-light" v-drag="[300,400,200,120]">
**Step 3**: Generate output
</StickyNote>
```

### Information Hierarchy
```md
<div class="space-y-4">
  <AdmonitionType type="important">
  Critical information users must see first.
  </AdmonitionType>

  <AdmonitionType type="note">
  Supplementary information for context.
  </AdmonitionType>
  
  <AdmonitionType type="tip">
  Helpful suggestions for best practices.
  </AdmonitionType>
</div>

<StickyNote color="yellow-light" width="250px">
**Quick Reference**: Key points to remember
</StickyNote>
```

## Best Practices

### Color Coordination
- Match component colors to slide color schemes
- Use contrasting colors for emphasis
- Limit to 3-4 colors per slide for visual coherence

### Positioning Strategy
- Use `v-drag` sparingly - too many positioned elements create chaos
- Group related components visually
- Leave breathing room between interactive elements
- Test positioning on different screen sizes

### Content Guidelines  
- Keep component text concise
- Use markdown formatting for emphasis
- Ensure text remains readable against component backgrounds
- Consider animation timing in presentation flow

### Performance Considerations
- Limit draggable elements to 5-6 per slide
- Avoid nested animations  
- Test component performance in presentation mode
- Use fixed widths for draggable components to prevent layout shift

## Accessibility Notes

- Ensure sufficient color contrast for text readability
- Provide alternative navigation paths for interactive content  
- Test components without animations for motion-sensitive audiences
- Include descriptive text for complex visual components