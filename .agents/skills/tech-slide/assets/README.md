# Tech-Slide Assets

This directory contains templates and assets for creating tech-slide presentations.

## Templates

### basic-tech-slide.md

Complete example presentation demonstrating all tech-slide patterns:
- Cover slide with title, author, email
- Table of Contents with all sections
- Section dividers with contextual ToC
- Multiple content slide types
- Key Takeaways summary

**Usage:**
```bash
# Copy template to your project
cp assets/templates/basic-tech-slide.md ./slides.md

# Edit with your content
# Run Slidev
pnpm run dev
```

## Creating New Templates

When creating new tech-slide templates:

1. **Always include these slides:**
   - Cover (title + author + email)
   - ToC (full section overview)
   - Section dividers (current section highlighted)
   - Key Takeaways (3-5 bullet points)

2. **Follow naming conventions:**
   - `[purpose]-tech-slide.md` (e.g., `workshop-tech-slide.md`)

3. **Color scheme recommendations:**
   - Cover: navy (or your chosen primary color)
   - ToC: No color (white/black background)
   - Sections: Same primary color for ALL sections
   - Takeaways: Primary-light (e.g., navy-light)
   - Accents: Primary color for callouts

4. **Section ToC pattern:**
   ```md
   <div>
   
   <div style="opacity: 0.4">Previous section 1</div>
   <div style="opacity: 0.4">Previous section 2</div>
   <div style="font-weight: bold">Current Section</div>
   <div style="opacity: 0.4">Upcoming section 1</div>
   <div style="opacity: 0.4">Upcoming section 2</div>
   
   </div>
   ```