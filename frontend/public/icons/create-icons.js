// Simple script to create basic PWA icons
const fs = require('fs');
const path = require('path');

const sizes = [72, 96, 128, 144, 152, 192, 384, 512];

// Create simple SVG icon
const createSVGIcon = (size) => {
  return `<svg width="${size}" height="${size}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${size}" height="${size}" fill="#667eea"/>
    <circle cx="${size/2}" cy="${size/2}" r="${size/3}" fill="#ffffff"/>
    <text x="${size/2}" y="${size/2 + 8}" text-anchor="middle" fill="#667eea" font-family="Arial, sans-serif" font-size="${size/8}" font-weight="bold">AI</text>
  </svg>`;
};

// Create placeholder PNG files (in a real app, you'd use proper image processing)
sizes.forEach(size => {
  const svgContent = createSVGIcon(size);
  const filename = `icon-${size}x${size}.png`;
  
  // For now, just create a placeholder text file
  // In production, you'd convert SVG to PNG
  fs.writeFileSync(path.join(__dirname, filename), svgContent);
  console.log(`Created ${filename}`);
});

console.log('Icon generation complete');