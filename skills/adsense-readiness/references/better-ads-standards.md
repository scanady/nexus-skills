# Better Ads Standards Reference

Google requires publishers to conform to the Better Ads Standards established by the Coalition for Better Ads. Violations can result in ads being filtered or accounts being penalized.

## Overview

The Better Ads Standards identify ad experiences that fall beneath a threshold of consumer acceptability. These standards are based on research involving over 66,000 consumers.

## Desktop Web Ad Experiences to Avoid

### 1. Pop-up Ads
- Ads that block the main content
- Appear after content begins loading
- Must be dismissed to access content

**Exception:** Cookie consent and age verification are allowed.

### 2. Auto-playing Video Ads with Sound
- Video ads that play automatically with sound on
- User must take action to mute or stop

**Allowed:** Auto-play video without sound is acceptable.

### 3. Prestitial Ads with Countdown
- Full-page ads that appear before content loads
- Display a countdown timer before dismissal

**Allowed:** Prestitials that can be dismissed immediately.

### 4. Large Sticky Ads
- Sticky ads that take up more than 30% of the screen
- Fixed position ads that are too prominent

### 5. Ad Density Higher Than 30%
- Pages where ads make up more than 30% of vertical height
- Applies to the main content area

### 6. Flashing Animated Ads
- Ads with rapidly flashing/animated backgrounds
- Strobing effects that distract from content

## Mobile Web Ad Experiences to Avoid

### 1. Pop-up Ads
- Same as desktop - blocks main content
- Especially problematic on smaller screens

### 2. Prestitial Ads
- Full-page ads before content loads
- With or without countdown timers

### 3. Ad Density Higher Than 30%
- Same as desktop
- Even more impactful on mobile screens

### 4. Flashing Animated Ads
- Same as desktop
- More distracting on handheld devices

### 5. Auto-playing Video Ads with Sound
- Same as desktop
- Particularly disruptive on mobile

### 6. Postitial Ads with Countdown
- Full-page ads that appear AFTER content
- Usually when navigating between pages
- Display countdown before allowing continuation

### 7. Full-screen Scrollover Ads
- Ads that cover content as user scrolls
- Require scrolling past them to access content

### 8. Large Sticky Ads
- Sticky ads taking more than 30% of screen
- More restrictive on mobile due to screen size

## Compliance Checklist

### Desktop
- [ ] No pop-up ads blocking content
- [ ] Video ads don't auto-play with sound
- [ ] No prestitial countdown timers
- [ ] Sticky ads ≤30% of screen height
- [ ] Ad density ≤30% of page height
- [ ] No flashing/strobing animated ads

### Mobile
- [ ] No pop-up ads
- [ ] No prestitial ads (any type)
- [ ] Ad density ≤30%
- [ ] No flashing animations
- [ ] No auto-playing video with sound
- [ ] No postitial countdown ads
- [ ] No full-screen scrollover ads
- [ ] Sticky ads ≤30% of screen height

## Testing Your Site

### Chrome's Ad Experience Report
1. Register site in Google Search Console
2. Access Ad Experience Report
3. Review any flagged ad experiences

### Manual Review
1. Visit your site on desktop and mobile
2. Check each ad placement
3. Measure sticky ad heights
4. Calculate ad density
5. Test video ad behavior
6. Check for pop-ups on page load

## Common Violations in Code

### Pop-up Patterns to Remove
```javascript
// Avoid: Modal dialogs triggered on page load
window.onload = function() {
  showAdModal(); // Violation
}

// Avoid: Timed pop-ups
setTimeout(showAdPopup, 5000); // Violation
```

### Auto-play Video Issues
```html
<!-- Violation: Auto-plays with sound -->
<video autoplay>
  
</video>

<!-- Allowed: Auto-plays muted -->
<video autoplay muted>
  
</video>
```

### Sticky Ad Size Check
```css
/* Violation: Sticky ad > 30% viewport height */
.sticky-ad {
  position: fixed;
  bottom: 0;
  height: 40vh; /* Too large */
}

/* Compliant: Sticky ad ≤ 30% */
.sticky-ad {
  position: fixed;
  bottom: 0;
  height: 90px; /* Fixed small size */
}
```

## Remediation Steps

### For Pop-ups
1. Remove on-load pop-up ad code
2. Convert to in-content ad placements
3. Use less intrusive ad formats

### For Prestitials
1. Remove prestitial ad code entirely
2. Consider in-content placements instead
3. If needed, ensure immediate dismissal option

### For Video Ads
1. Add `muted` attribute to autoplay videos
2. Or remove `autoplay` attribute
3. Let user initiate video playback

### For High Ad Density
1. Remove some ad units
2. Add more content between ads
3. Reduce ad sizes
4. Prioritize content visibility

### For Large Sticky Ads
1. Reduce sticky ad height
2. Convert to smaller format
3. Move to in-content placement

## Resources

- [Coalition for Better Ads](https://www.betterads.org/)
- [Better Ads Standards](https://www.betterads.org/standards/)
- [Google Ad Experience Report](https://www.google.com/webmasters/tools/ad-experience-unverified)
