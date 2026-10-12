"""
Script to upgrade all 14 remaining recommended papers to the beginner-friendly standard:
- Acronym & Plain English Glossary
- Explain Like I'm 5 (ELI5) with real-world physical analogies & ASCII visual
- Structured metadata, discoveries, what it adds/doesn't add
- Comparison against our research paper
- Visual Architecture Specification (Clean ASCII + High-Fidelity SVG link)
- Actionable Takeaways
- Dedicated SVG vector diagram in research/docs/assets/papers/
"""
import os

svg_dir = "research/docs/assets/papers"
os.makedirs(svg_dir, exist_ok=True)

def generate_svg(filename, title, subtitle, box1_title, box1_text, box2_title, box2_text, box3_title, box3_text, bottom_text, badge_color="#0284c7"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 650" width="100%" height="100%" style="background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>

    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{badge_color}" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>

    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1e293b" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>

    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000000" flood-opacity="0.5"/>
    </filter>

    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#64748b" />
    </marker>
  </defs>

  <!-- Background -->
  <rect width="1100" height="650" fill="url(#bgGrad)" />

  <!-- Subtle grid lines -->
  <g stroke="#ffffff" stroke-opacity="0.03" stroke-width="1">
    <line x1="0" y1="100" x2="1100" y2="100" />
    <line x1="0" y1="200" x2="1100" y2="200" />
    <line x1="0" y1="300" x2="1100" y2="300" />
    <line x1="0" y1="400" x2="1100" y2="400" />
    <line x1="0" y1="500" x2="1100" y2="500" />
    <line x1="200" y1="0" x2="200" y2="650" />
    <line x1="400" y1="0" x2="400" y2="650" />
    <line x1="600" y1="0" x2="600" y2="650" />
    <line x1="800" y1="0" x2="800" y2="650" />
  </g>

  <!-- Header Section -->
  <g transform="translate(50, 40)">
    <rect x="0" y="0" width="38" height="38" rx="8" fill="{badge_color}" />
    <text x="19" y="25" fill="#ffffff" font-size="18" font-weight="bold" text-anchor="middle">🔍</text>
    <text x="50" y="20" fill="#f8fafc" font-size="22" font-weight="bold">{title}</text>
    <text x="50" y="38" fill="#94a3b8" font-size="13">{subtitle}</text>
  </g>

  <!-- Card 1: Input / Problem -->
  <g transform="translate(50, 120)">
    <rect width="280" height="380" rx="12" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="280" height="42" rx="12" fill="#1e293b"/>
    <text x="20" y="26" fill="#38bdf8" font-size="14" font-weight="bold">STAGE 1: {box1_title}</text>
    <foreignObject x="20" y="60" width="240" height="300">
      <div xmlns="http://www.w3.org/1999/xhtml" style="color: #cbd5e1; font-size: 13px; line-height: 1.6;">
        {box1_text}
      </div>
    </foreignObject>
  </g>

  <!-- Flow Arrow 1 -> 2 -->
  <line x1="340" y1="310" x2="400" y2="310" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)" />

  <!-- Card 2: Mechanism / Processing -->
  <g transform="translate(410, 120)">
    <rect width="280" height="380" rx="12" fill="url(#cardGrad)" stroke="{badge_color}" stroke-width="1.8" filter="url(#shadow)"/>
    <rect x="0" y="0" width="280" height="42" rx="12" fill="{badge_color}" fill-opacity="0.2"/>
    <text x="20" y="26" fill="#f8fafc" font-size="14" font-weight="bold">STAGE 2: {box2_title}</text>
    <foreignObject x="20" y="60" width="240" height="300">
      <div xmlns="http://www.w3.org/1999/xhtml" style="color: #cbd5e1; font-size: 13px; line-height: 1.6;">
        {box2_text}
      </div>
    </foreignObject>
  </g>

  <!-- Flow Arrow 2 -> 3 -->
  <line x1="700" y1="310" x2="760" y2="310" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)" />

  <!-- Card 3: Output / Resolution -->
  <g transform="translate(770, 120)">
    <rect width="280" height="380" rx="12" fill="url(#cardGrad)" stroke="#10b981" stroke-width="1.5" filter="url(#shadow)"/>
    <rect x="0" y="0" width="280" height="42" rx="12" fill="#10b981" fill-opacity="0.15"/>
    <text x="20" y="26" fill="#34d399" font-size="14" font-weight="bold">STAGE 3: {box3_title}</text>
    <foreignObject x="20" y="60" width="240" height="300">
      <div xmlns="http://www.w3.org/1999/xhtml" style="color: #cbd5e1; font-size: 13px; line-height: 1.6;">
        {box3_text}
      </div>
    </foreignObject>
  </g>

  <!-- Bottom Synthesis Bar -->
  <g transform="translate(50, 530)">
    <rect width="1000" height="75" rx="10" fill="#1e293b" stroke="#475569" stroke-width="1" />
    <text x="25" y="30" fill="#38bdf8" font-size="13" font-weight="bold">CORE TAKEAWAY FOR OUR RESEARCH PAPER:</text>
    <text x="25" y="52" fill="#e2e8f0" font-size="13">{bottom_text}</text>
  </g>
</svg>'''

print("SVG helper initialized.")
