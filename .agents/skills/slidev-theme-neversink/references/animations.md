# Neversink Animations & Transitions

Guide to adding animations, transitions, and interactive effects in Neversink presentations.

## Slide Transitions

### Built-in Transitions
Slidev provides several transition effects between slides:

```yaml
---
layout: default
transition: slide-left    # Slide from right to left
---

# Next slide
---
transition: slide-up      # Slide from bottom to top  
---

# Another slide
---
transition: fade-out      # Fade transition
---
```

### Available Transition Types
- `slide-left`, `slide-right`, `slide-up`, `slide-down`
- `fade`, `fade-out`
- `zoom`, `zoom-out`
- `none` (instant transition)

## Click Animations

### Step-by-step Reveals
Control content appearance with click progression:

```yaml
---
layout: default
---

# Progressive Content

<v-clicks>

- First point appears on first click
- Second point on second click  
- Third point on third click

</v-clicks>
```

### Individual Click Control
```md
# Slide Content

<v-click>

This appears on first click

</v-click>

<v-click>

This appears on second click

</v-click>

<v-click at="4">

This appears on fourth click (skipping third)

</v-click>
```

### Click-based Styling
```md
# Dynamic Styling

<div v-click-hide>This disappears after first click</div>

<div v-after>This appears after all clicks are done</div>

<div class="opacity-50" v-click="{ opacity: 100 }">
This becomes fully opaque on click
</div>
```

## Component Animations

### Speech Bubble Animations
```md
<SpeechBubble 
  position="l" 
  color="sky" 
  animation="float">
  This bubble gently floats up and down
</SpeechBubble>

<SpeechBubble 
  position="r" 
  color="pink" 
  animation="bounce">
  This bubble bounces subtly
</SpeechBubble>
```

### Draggable Elements with v-drag
```md
<!-- Static positioning -->
<StickyNote color="amber" v-drag="[100,200,250,150]">
Positioned at x:100, y:200
</StickyNote>

<!-- With rotation animation -->
<StickyNote color="green" v-drag="[300,100,200,120,15]">
Rotated 15 degrees
</StickyNote>

<!-- Multiple animated elements -->
<div class="relative h-full">
  <SpeechBubble 
    position="l" 
    color="sky" 
    animation="float" 
    v-drag="[50,150,280,100]">
    First floating bubble
  </SpeechBubble>
  
  <SpeechBubble 
    position="r" 
    color="amber" 
    animation="bounce" 
    v-drag="[400,250,280,100]">
    Second bouncing bubble  
  </SpeechBubble>
</div>
```

## CSS Animation Classes

### Custom Animations with UnoCSS/Tailwind
```md
<!-- Fade in animation -->
<div class="animate-fade-in">
Content that fades in
</div>

<!-- Slide in from left -->
<div class="animate-slide-in-left">
Content slides in from left
</div>

<!-- Pulse effect -->
<div class="animate-pulse">
Pulsing content
</div>

<!-- Bounce effect -->  
<div class="animate-bounce">
Bouncing content
</div>
```

### Combined with v-click
```md
<div v-click class="animate-fade-in-up">
Fades in and slides up on click
</div>

<div v-click="2" class="animate-zoom-in">  
Zooms in on second click
</div>
```

## Code Animation Patterns

### Highlighting Lines Progressively
```md
\```python {1|2-3|4-6|all}
def process_data(data):
    # First highlight line 1
    filtered = filter_invalid(data)  # Then lines 2-3
    processed = transform(filtered)
    validated = validate_results(processed)  # Then lines 4-6
    return validated  # Finally show all
\```
```

### Code Focus with Clicks
```md
\```typescript {1-3|5-8|10-12}
// Initial setup
const config = {
  timeout: 5000
};

// Processing logic  
async function process(data) {
  return await transform(data);
}

// Error handling
catch (error) {
  logger.error(error);
}
\```
```

## Advanced Animation Patterns

### Sequence Animations
Create complex sequences with multiple elements:

```md
---
layout: full
---

<div class="h-full w-full relative">
  
  <!-- First element appears -->
  <div v-click="1" class="animate-fade-in">
    <h1>Step 1: Initial State</h1>
  </div>
  
  <!-- Second element slides in -->
  <SpeechBubble 
    v-click="2"
    position="l" 
    color="sky"
    class="animate-slide-in-left"
    v-drag="[100,200,300,100]">
    Step 2: Add explanation
  </SpeechBubble>
  
  <!-- Third element with delay -->
  <StickyNote 
    v-click="3"
    color="amber" 
    class="animate-bounce"
    v-drag="[400,300,200,120]">
    Step 3: Final note
  </StickyNote>
  
</div>
```

### Coordinated Component Animation 
```md
<!-- Dialogue sequence -->
<IceCream 
  v-click="1"
  :size="120" 
  mood="happy" 
  class="animate-slide-in-left"
  v-drag="[100,300,120,120]" />

<SpeechBubble 
  v-click="2"
  position="r" 
  color="pink" 
  animation="float"
  v-drag="[250,250,280,100]">
  Hello! Let me explain this concept.
</SpeechBubble>

<SpeechBubble 
  v-click="3"
  position="l" 
  color="sky"
  animation="bounce" 
  v-drag="[50,150,280,80]">
  That's very helpful, thanks!
</SpeechBubble>
```

## Interactive Animations

### Hover Effects
```md
<div class="hover:scale-110 transition-transform duration-300">
Scales on hover
</div>

<StickyNote 
  color="amber" 
  class="hover:rotate-3 transition-transform">
Tilts slightly on hover
</StickyNote>
```

### Click-triggered Animations
```md
<div @click="$slidev.nav.next()" class="cursor-pointer hover:animate-pulse">
Click me to advance slide
</div>
```

## Animation Best Practices

### Performance Guidelines

1. **Limit Simultaneous Animations**
   - Max 3-4 animated elements per slide
   - Avoid overlapping complex animations
   - Test on slower devices

2. **Animation Duration**
   - Keep transitions under 1 second
   - Use 0.3-0.5s for most UI animations
   - Longer animations (1-2s) only for emphasis

3. **CPU-Friendly Properties**
   - Prefer `transform` over `left/top`
   - Use `opacity` over `visibility`
   - Avoid animating `width/height` when possible

### Accessibility Considerations

1. **Motion Sensitivity**
   ```css
   @media (prefers-reduced-motion: reduce) {
     .animate-bounce { animation: none; }
     .animate-pulse { animation: none; }
   }
   ```

2. **Meaningful Animations**
   - Animations should enhance understanding
   - Avoid purely decorative animations
   - Provide alternative navigation paths

### Presentation Flow

1. **Timing Control**
   - Use click-based reveals for audience control
   - Automatic timings only for continuous concepts
   - Always provide manual advance options

2. **Visual Hierarchy**
   - Animate most important content first
   - Use consistent animation directions
   - End animations in logical reading order

## Example Animation Sequences

### Teaching Sequence
```md
---
layout: full
---

# Algorithm Explanation

<div v-click="1" class="animate-fade-in">

## Step 1: Initialize
```python
data = []
```

</div>

<div v-click="2" class="animate-slide-in-right">

## Step 2: Process
```python  
for item in input:
    data.append(process(item))
```

</div>

<div v-click="3" class="animate-zoom-in">

## Step 3: Return
```python
return data
```

</div>
```

### Interactive Demo Flow
```md
---
layout: full
---

<div class="relative h-full">

  <!-- Demo introduction -->
  <div v-click="1" class="text-center animate-fade-in">
    <h1>Live API Demo</h1>
  </div>

  <!-- Code appears -->
  <div v-click="2" class="animate-slide-in-left" style="position: absolute; top: 100px; left: 50px;">
    \```bash
    curl -X POST https://api.example.com/data
    \```
  </div>

  <!-- Response appears -->  
  <SpeechBubble 
    v-click="3"
    position="r" 
    color="green"
    class="animate-slide-in-right"
    v-drag="[400,200,300,150]">
    Expected response:
    ```json
    {"success": true, "data": [...]}
    ```
  </SpeechBubble>

  <!-- Commentary -->
  <StickyNote 
    v-click="4"
    color="amber" 
    class="animate-bounce"
    v-drag="[100,400,250,100]">
    Notice the fast response time!
  </StickyNote>

</div>
```