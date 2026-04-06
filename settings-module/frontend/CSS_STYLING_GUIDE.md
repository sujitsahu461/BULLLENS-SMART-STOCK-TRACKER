# 🎨 Settings Sidebar - CSS & Styling Guide

## Color Palette

### Background Colors

| Element | Hex | Tailwind | Usage |
|---------|-----|----------|-------|
| Main BG | #0f172a | `bg-slate-900` | Page background gradient |
| Card BG | #1e293b | `bg-slate-800` | Card backgrounds |
| Active Card | #1e293b/20% | `bg-slate-800/20` | Hover state |
| Border | #334155/30% | `border-slate-600/30` | Card borders |

### Text Colors

| Element | Hex | Tailwind | Usage |
|---------|-----|----------|-------|
| Primary Text | #f1f5f9 | `text-white` | Titles, main text |
| Secondary Text | #cbd5e1 | `text-gray-300` | Subtitles on hover |
| Muted Text | #94a3b8 | `text-gray-400` | Descriptions, placeholders |

### Accent Colors (Per Setting)

| Setting | Color | Tailwind Gradient |
|---------|-------|-------------------|
| Profile | Blue | `from-blue-500 to-blue-600` |
| Predictions | Green | `from-green-500 to-green-600` |
| Market | Purple | `from-purple-500 to-purple-600` |
| Notifications | Orange | `from-orange-500 to-orange-600` |
| Appearance | Pink | `from-pink-500 to-pink-600` |
| Watchlist | Yellow | `from-yellow-500 to-yellow-600` |
| Security | Red | `from-red-500 to-red-600` |
| Help | Cyan | `from-cyan-500 to-cyan-600` |
| Logout | Red | `from-red-600/20 to-red-600/20` |

---

## Typography

### Font Family

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
             'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 
             'Helvetica Neue', sans-serif;
```

### Type Hierarchy

| Element | Tailwind Class | Size | Weight | Usage |
|---------|---|------|--------|-------|
| User Name | `text-xl font-bold` | 20px | 700 | Header title |
| Subtitle | `text-sm text-gray-400` | 14px | 400 | User info tagline |
| Setting Title | `font-semibold text-white` | 16px | 600 | Option title |
| Setting Desc | `text-sm text-gray-400` | 14px | 400 | Option description |
| Version | `text-xs text-gray-500` | 12px | 400 | Footer text |

---

## Spacing & Layout

### Container

```jsx
<div className="max-w-md mx-auto">  // Max width: 28rem (448px)
  <div className="mb-8">            // Margin: 32px
```

### Padding

| Element | Tailwind | Pixels |
|---------|----------|--------|
| Page | `p-6` | 24px padding all |
| Settings Item | `p-4` | 16px padding all |
| Icon Box | `p-3` | 12px padding |
| Gap between elements | `gap-4` | 16px |
| Margin between sections | `mb-6` | 24px |

### Gaps

```jsx
<div className="gap-4">      // 16px gap
<div className="flex gap-4"> // Between icon & content
<div className="space-y-3">  // 12px vertical gap between items
```

---

## Border Radius

| Element | Tailwind | Pixels | Applied |
|---------|----------|--------|---------|
| Search Bar | `rounded-lg` | 8px | Input field |
| Settings Card | `rounded-xl` | 16px | Each setting button |
| Icon Container | `rounded-lg` | 8px | Icon background |
| User Avatar | `rounded-full` | 999px | Profile picture |

---

## Effects & Transitions

### Hover Effects

```jsx
// Settings Card Hover
className={`
  ... 
  hover:bg-slate-700/50              // Background change on hover
  hover:border-slate-500/50          // Border highlight
  transition-all duration-200        // Smooth 200ms transition
`}

// Icon Hover
className={`
  bg-slate-600/50 
  group-hover:bg-slate-600           // Darker on hover
  transition-all                     // Smooth animation
`}

// Text Hover
className={`
  text-gray-300 
  group-hover:text-white             // Lighter on hover
  transition-colors                  // Color transition
`}
```

### Active State

```jsx
// Active Setting Card
className={`
  bg-gradient-to-r 
  from-blue-600/20 to-purple-600/20  // Gradient overlay (20% opacity)
  border border-blue-500/30          // Blue border (30% opacity)
`}

// Active Icon
className={`
  bg-gradient-to-br 
  ${setting.color}                   // Using category color gradient
`}
```

### Transitions

| Property | Duration | Function |
|----------|----------|----------|
| All | `duration-200` | 200ms ease |
| Colors | `transition-colors` | Smooth color change |
| Opacity | `opacity-0 group-hover:opacity-100` | Show/hide arrow |

---

## Responsive Design

### Breakpoints (Tailwind Default)

| Breakpoint | Width |
|-----------|-------|
| Default (Mobile) | < 640px |
| `sm` | ≥ 640px |
| `md` | ≥ 768px |
| `lg` | ≥ 1024px |
| `xl` | ≥ 1280px |

### Container Query

```jsx
<div className="max-w-md mx-auto">  // Max 448px, centered
  {/* Content scales within this container */}
</div>
```

### Responsive Classes Used

```jsx
className="w-full"                // Full width on mobile
className="max-w-md"              // Constrain width on desktop
className="mx-auto"               // Center container
className="p-6"                   // Padding all widths
className="flex items-center"     // Flexbox responsive
```

---

## Hover State Animations

### Button Hover Group

```jsx
<button className="group">
  {/* Container changes */}
  <div className="
    hover:bg-slate-700/50
    hover:border-slate-500/50
    transition-all duration-200
  ">
  
  {/* Icon changes */}
  <div className="group-hover:bg-slate-600">
  
  {/* Text changes */}
  <h3 className="group-hover:text-blue-300">
  
  {/* Arrow appears */}
  <div className="opacity-0 group-hover:opacity-100">
</button>
```

---

## Search Bar Styling

```jsx
<input
  className="
    w-full                          // Full width
    pl-10 pr-4 py-3                 // Padding (left for icon)
    bg-slate-700/50                 // Semi-transparent background
    border border-slate-600         // Border color
    rounded-lg                      // Border radius
    text-white                      // Text color
    placeholder-gray-400            // Placeholder color
    focus:outline-none              // Remove default outline
    focus:border-blue-500           // Blue border on focus
    focus:ring-2 focus:ring-blue-500/20  // Glow effect
    transition                      // Smooth transition
  "
/>
```

---

## Icon Styling

### Icon Container

```jsx
<div className="
  mt-1                             // Align with text
  p-3                              // Inner padding
  rounded-lg                       // Border radius
  transition-all                   // Smooth animation
  bg-gradient-to-br ${setting.color}  // Dynamic gradient
">
  <IconComponent className="w-5 h-5 text-white" />
</div>
```

### Icon Sizes

| Size | Tailwind | Pixels |
|------|----------|--------|
| Large | `w-8 h-8` | 32px |
| Medium | `w-6 h-6` | 24px |
| Small | `w-5 h-5` | 20px |
| Tiny | `w-4 h-4` | 16px |

---

## Card/Button Styling

### Base Button

```jsx
<button className="
  w-full                           // Full width
  p-4                              // Padding
  rounded-xl                       // Rounded corners
  transition-all duration-200      // Smooth transition
  group                            // Enable group selectors
  text-left                        // Left-align text
">
```

### Inactive State

```jsx
className={`
  bg-slate-700/30                  // 30% opacity gray
  border border-slate-600/30       // Subtle border
  hover:bg-slate-700/50            // Darker on hover
  hover:border-slate-500/50        // Highlight border
`}
```

### Active State

```jsx
className={`
  bg-gradient-to-r 
  from-blue-600/20 to-purple-600/20  // Gradient highlight
  border border-blue-500/30          // Blue border
`}
```

---

## Divider Styling

```jsx
<div className="
  h-px                             // 1px height
  bg-gradient-to-r                 // Horizontal gradient
  from-transparent                 // Start transparent
  via-slate-600                    // Middle color
  to-transparent                   // End transparent
  my-6                             // Vertical margin (24px)
" />
```

---

## Custom CSS (index.css)

### Font Smoothing

```css
* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Body Styles

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', ...;
  background-color: #0f172a;
  color: #f1f5f9;
}
```

### Smooth Scroll

```css
html {
  scroll-behavior: smooth;
}
```

### Custom Scrollbar

```css
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #1e293b;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}
```

---

## Opacity Utilities

| Usage | Tailwind | Opacity |
|-------|----------|---------|
| Icon hover | `group-hover:opacity-100` | 100% |
| Background | `bg-slate-700/50` | 50% |
| Background | `bg-slate-700/30` | 30% |
| Border | `border-blue-500/30` | 30% |
| Text | `text-gray-400` | ~60% |

---

## Gradient Examples

### Background Gradients

```jsx
// Page background
className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900"

// Icon background (dynamic per setting)
className={`bg-gradient-to-br ${setting.color}`}
// Example: "${from-blue-500 to-blue-600}"

// Divider
className="bg-gradient-to-r from-transparent via-slate-600 to-transparent"

// Active card
className="bg-gradient-to-r from-blue-600/20 to-purple-600/20"
```

---

## Customization Checklist

- [ ] Change primary color (blue → custom)
- [ ] Adjust dark theme opacity (50% → 60%)
- [ ] Update icon sizes for different screens
- [ ] Modify border radius (16px → 12px)
- [ ] Adjust spacing/padding values
- [ ] Create additional color variants
- [ ] Add animations for entry/exit
- [ ] Customize scrollbar colors
- [ ] Update fonts (system → Google Fonts)
- [ ] Add dark/light theme toggle

---

## Performance Notes

✅ **CSS-first approach** - No JS animations  
✅ **Tailwind utilities** - No custom CSS bloat  
✅ **GPU acceleration** - `transform` & `opacity` only  
✅ **Minimal repaints** - Hover states use `background` property  
✅ **Optimized bundle** - ~2-3KB of Tailwind CSS

---

## Browser Support

| Browser | Support |
|---------|---------|
| Chrome | ✅ Full |
| Firefox | ✅ Full |
| Safari | ✅ Full |
| Edge | ✅ Full |
| IE 11 | ⚠️ Partial |

---

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Lucide Icons](https://lucide.dev)  
- [MDN CSS Guide](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Web.dev Performance](https://web.dev/performance/)
