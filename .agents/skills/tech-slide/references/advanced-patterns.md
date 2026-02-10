# Advanced Tech-Slide Patterns

Complex navigation and structure patterns for advanced technical presentations.

## Multi-Level Table of Contents

### Hierarchical Sections

For presentations with nested topic structures:

```md
---
layout: default
---

# Table of Contents

### 1. 📚 Foundation
- 1.1 Prerequisites
- 1.2 Setup
- 1.3 Basic Concepts

### 2. 🔧 Core Topics
- 2.1 Topic A
  - 2.1.1 Subtopic A1
  - 2.1.2 Subtopic A2
- 2.2 Topic B

### 3. 💻 Advanced Topics
- 3.1 Advanced Pattern 1
- 3.2 Advanced Pattern 2

### 4. 🎯 Practice & Application
- 4.1 Exercises
- 4.2 Case Studies
```

### Subsection Navigation

Show current position within a section:

```md
---
layout: section
color: violet
---

# Section: Core Topics (2/5)
<hr>

<div style="opacity: 0.4">1. 📚 Foundation</div>

**2. 🔧 Core Topics**
  <div style="margin-left: 2rem;">
    <div style="opacity: 0.5">2.1 Topic A</div>
    <div style="font-weight: bold;">2.2 Topic B ← Current</div>
    <div style="opacity: 0.5">2.3 Topic C</div>
  </div>

<div style="opacity: 0.4">

3. 💻 Advanced Topics
4. 🎯 Practice & Application
5. 🔑 Key Takeaways

</div>
```

## Dynamic ToC Patterns

### Color-Coded Progress

Use different colors for completed, current, and upcoming:

```md
---
layout: default
---

# Progress Overview

<div class="text-lg">
  <div class="text-green-600">✓ 1. Background & Motivation</div>
  <div class="text-green-600">✓ 2. Core Concepts</div>
  <div class="text-blue-600 font-bold text-xl">→ 3. Implementation Guide</div>
  <div class="opacity-40">4. Best Practices</div>
  <div class="opacity-40">5. Key Takeaways</div>
</div>
```

### Visual Progress Bar

```md
# Course Progress

<div class="flex items-center gap-2 text-sm">
  <div class="flex-1 bg-green-500 h-2 rounded"></div>
  <div class="flex-1 bg-green-500 h-2 rounded"></div>
  <div class="flex-1 bg-blue-500 h-2 rounded"></div>
  <div class="flex-1 bg-gray-300 h-2 rounded"></div>
  <div class="flex-1 bg-gray-300 h-2 rounded"></div>
</div>

<div class="text-center mt-4 text-gray-600">
Section 3 of 5 — 60% Complete
</div>
```

### Icon-Based Navigation

```md
# Learning Journey

<div class="grid grid-cols-5 gap-4 text-center">
  <div>
    <div class="text-4xl mb-2">✅</div>
    <div class="text-xs">Background</div>
  </div>
  <div>
    <div class="text-4xl mb-2">✅</div>
    <div class="text-xs">Core Concepts</div>
  </div>
  <div>
    <div class="text-4xl mb-2 text-blue-600">📍</div>
    <div class="text-xs font-bold">Implementation</div>
  </div>
  <div class="opacity-40">
    <div class="text-4xl mb-2">⭕</div>
    <div class="text-xs">Best Practices</div>
  </div>
  <div class="opacity-40">
    <div class="text-4xl mb-2">⭕</div>
    <div class="text-xs">Takeaways</div>
  </div>
</div>
```

## Adaptive Section Dividers

### Compact Section Header

For shorter transitions:

```md
---
layout: default
---

<div class="absolute top-4 right-4 text-sm opacity-60">Section 3/5</div>

# 💻 Implementation Guide

<div class="flex gap-8 text-sm mt-4">
  <span class="opacity-40">1. Background</span>
  <span class="opacity-40">2. Concepts</span>
  <span class="font-bold text-blue-600">3. Implementation</span>
  <span class="opacity-40">4. Best Practices</span>
  <span class="opacity-40">5. Takeaways</span>
</div>

---

Content starts here...
```

### Full-Page Section with Preview

```md
---
layout: section
color: navy
---

# 🔧 Core Concepts
<hr>

<div>

<div style="opacity: 0.4">1. 📚 Background & Motivation</div>
<div style="font-weight: bold">2. 🔧 Core Concepts</div>
<div style="opacity: 0.4">3. 💻 Implementation Guide</div>
<div style="opacity: 0.4">4. 🎯 Best Practices</div>
<div style="opacity: 0.4">5. 🔑 Key Takeaways</div>

</div>

<div class="mt-8 text-base opacity-80">
In this section, we'll explore:
- Fundamental principles
- Key terminology
- Mental models
</div>
```

## Mini-ToC for Subsections

Show section-specific navigation at the start of each subsection:

```md
---
layout: default
---

# Topic 2.3: Advanced Patterns

<div class="text-sm border-l-4 border-blue-500 pl-4 mb-8">
  <div class="opacity-60 mb-1">Section 2: Core Topics</div>
  <div class="opacity-40">2.1 Topic A ↑</div>
  <div class="opacity-40">2.2 Topic B ↑</div>
  <div class="font-bold">2.3 Advanced Patterns ← You are here</div>
  <div class="opacity-40">2.4 Topic D ↓</div>
</div>

Content begins...
```

## Breadcrumb Navigation

```md
---
layout: default
---

<div class="text-sm opacity-60 mb-4">
Home > Core Concepts > Topic A > Subtopic A2
</div>

# Subtopic A2: Implementation Details

Content...
```

## Chapter-Style Sections

For book-like presentations:

```md
---
layout: section
color: navy
---

<div class="text-6xl font-bold opacity-20 absolute top-8 right-8">02</div>

# Chapter 2
## Core Concepts
<hr>

<div class="grid grid-cols-5 gap-2 mt-8 text-xs text-center">
  <div class="opacity-40 p-2 border rounded">Ch 1<br>Background</div>
  <div class="p-2 border-2 border-blue-500 rounded font-bold">Ch 2<br>Core Concepts</div>
  <div class="opacity-40 p-2 border rounded">Ch 3<br>Implementation</div>
  <div class="opacity-40 p-2 border rounded">Ch 4<br>Best Practices</div>
  <div class="opacity-40 p-2 border rounded">Ch 5<br>Takeaways</div>
</div>
```

## Collapsible Key Takeaways

Interactive summary with progressive disclosure:

```md
---
layout: default
---

# 🔑 Key Takeaways

<v-clicks>

### 💡 Core Understanding
- **Principle 1**: Explanation
- **Principle 2**: Explanation

### 🛠️ Practical Skills
- **Skill 1**: What you can now do
- **Skill 2**: What you can now do

### 📈 Next Level
- **Advanced Topic 1**: Where to go next
- **Resource 2**: Additional learning

</v-clicks>
```

## Multi-Format Key Takeaways

### Visual Card Layout

```md
---
layout: default
---

# 🔑 Key Takeaways

<div class="grid grid-cols-3 gap-4 mt-8">

<div class="p-4 border-2 border-blue-500 rounded">
  <div class="text-2xl mb-2">🎯</div>
  <div class="font-bold mb-2">Main Concept</div>
  <div class="text-sm">Brief explanation of the key learning</div>
</div>

<div class="p-4 border-2 border-green-500 rounded">
  <div class="text-2xl mb-2">💪</div>
  <div class="font-bold mb-2">Key Skill</div>
  <div class="text-sm">What you can now accomplish</div>
</div>

<div class="p-4 border-2 border-amber-500 rounded">
  <div class="text-2xl mb-2">⚡</div>
  <div class="font-bold mb-2">Best Practice</div>
  <div class="text-sm">Important principle to remember</div>
</div>

</div>
```

### Two-Column Summary

```md
---
layout: two-cols-title
color: amber-light
---

:: title ::
# 🔑 What You've Learned

:: left ::

### Technical Skills ⚙️
- Skill 1
- Skill 2
- Skill 3

### Conceptual Understanding 🧠
- Concept 1
- Concept 2
- Concept 3

:: right ::

### Best Practices ✨
- Practice 1
- Practice 2
- Practice 3

### Resources for Next Steps 📚
- [Documentation](https://...)
- [Tutorial Series](https://...)
- [Community Forum](https://...)
```

## Contextualized Section Headers

Add "Why This Matters" context:

```md
---
layout: section
color: navy
---

# Section: Implementation Guide
<hr>

<div class="text-base opacity-80 max-w-2xl mx-auto text-center mt-4">
Now that you understand the concepts, let's put them into practice with hands-on implementation.
</div>

<div>

<div style="opacity: 0.4">1. 📚 Background & Motivation</div>
<div style="opacity: 0.4">2. 🔧 Core Concepts</div>
<div style="font-weight: bold">3. 💻 Implementation Guide</div>
<div style="opacity: 0.4">4. 🎯 Best Practices</div>
<div style="opacity: 0.4">5. 🔑 Key Takeaways</div>

</div>
```

## Time-Based Navigation

Show estimated time for each section:

```md
# Table of Contents

<div class="grid grid-cols-1 gap-3">
  <div class="flex justify-between">
    <span>1. 📚 Background & Motivation</span>
    <span class="opacity-60 text-sm">~10 min</span>
  </div>
  <div class="flex justify-between">
    <span>2. 🔧 Core Concepts</span>
    <span class="opacity-60 text-sm">~20 min</span>
  </div>
  <div class="flex justify-between">
    <span>3. 💻 Implementation Guide</span>
    <span class="opacity-60 text-sm">~30 min</span>
  </div>
  <div class="flex justify-between">
    <span>4. 🎯 Best Practices</span>
    <span class="opacity-60 text-sm">~15 min</span>
  </div>
  <div class="flex justify-between">
    <span>5. 🔑 Key Takeaways</span>
    <span class="opacity-60 text-sm">~5 min</span>
  </div>
</div>

<div class="text-center mt-6 text-sm opacity-60">
Total Duration: ~80 minutes
</div>
```
