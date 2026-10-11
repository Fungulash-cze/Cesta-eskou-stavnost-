const sharp = require('sharp');
const fs = require('fs');

async function createCard({ filename, title, subTitle, symbolFile, customCenterSvg }) {
  const W = 600;
  const H = 840;

  // 1. Prepare parchment background
  const bg = await sharp('Parchment bez pozadí.png')
    .resize(W, H, { fit: 'fill' })
    .toBuffer();

  // 2. Prepare symbol if available
  let symbolBuffer = null;
  if (symbolFile && fs.existsSync(symbolFile)) {
    symbolBuffer = await sharp(symbolFile)
      .resize(320, 320, { fit: 'inside' })
      .toBuffer();
  }

  // 3. Create SVG decorative overlay
  const overlaySvg = `
  <svg width="${W}" height="${H}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#b8860b"/>
        <stop offset="50%" stop-color="#ffd700"/>
        <stop offset="100%" stop-color="#8b6508"/>
      </linearGradient>
      <linearGradient id="bannerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#2a1f14" stop-opacity="0.95"/>
        <stop offset="100%" stop-color="#140d07" stop-opacity="0.95"/>
      </linearGradient>
      <linearGradient id="textAreaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#1f1810" stop-opacity="0.6"/>
        <stop offset="100%" stop-color="#120e09" stop-opacity="0.85"/>
      </linearGradient>
      <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.7"/>
      </filter>
    </defs>

    <!-- Outer Ornamental Border -->
    <rect x="18" y="18" width="${W - 36}" height="${H - 36}" rx="12" fill="none" stroke="#5a3d1c" stroke-width="4" opacity="0.85"/>
    <rect x="24" y="24" width="${W - 48}" height="${H - 48}" rx="8" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.9"/>
    <rect x="28" y="28" width="${W - 56}" height="${H - 56}" rx="6" fill="none" stroke="#3a2512" stroke-width="1" opacity="0.6"/>

    <!-- Corner Ornaments -->
    <g fill="#b8860b">
      <!-- Top Left -->
      <path d="M24,24 L48,24 L48,27 L27,27 L27,48 L24,48 Z"/>
      <circle cx="34" cy="34" r="3" fill="url(#goldGrad)"/>
      <!-- Top Right -->
      <path d="M${W-24},24 L${W-48},24 L${W-48},27 L${W-27},27 L${W-27},48 L${W-24},48 Z"/>
      <circle cx="${W-34}" cy="34" r="3" fill="url(#goldGrad)"/>
      <!-- Bottom Left -->
      <path d="M24,${H-24} L48,${H-24} L48,${H-27} L27,${H-27} L27,${H-48} L24,${H-48} Z"/>
      <circle cx="34" cy="${H-34}" r="3" fill="url(#goldGrad)"/>
      <!-- Bottom Right -->
      <path d="M${W-24},${H-24} L${W-48},${H-24} L${W-48},${H-27} L${W-27},${H-27} L${W-27},${H-48} L${W-24},${H-48} Z"/>
      <circle cx="${W-34}" cy="${H-34}" r="3" fill="url(#goldGrad)"/>
    </g>

    <!-- Header Banner -->
    <rect x="44" y="40" width="${W - 88}" height="76" rx="6" fill="url(#bannerGrad)" stroke="url(#goldGrad)" stroke-width="2" filter="url(#shadow)"/>
    <text x="${W / 2}" y="70" font-family="Cinzel, Georgia, serif" font-size="20" font-weight="bold" fill="#f5deb3" text-anchor="middle" letter-spacing="2" filter="url(#shadow)">
      ${title}
    </text>
    <text x="${W / 2}" y="98" font-family="Cinzel, Georgia, serif" font-size="12" font-weight="600" fill="#b8860b" text-anchor="middle" letter-spacing="3">
      ${subTitle}
    </text>

    <!-- Emblem Frame (circular/oval backing in upper center) -->
    <circle cx="${W / 2}" cy="285" r="165" fill="#1b140d" opacity="0.35" stroke="url(#goldGrad)" stroke-width="2" stroke-dasharray="6,4"/>
    <circle cx="${W / 2}" cy="285" r="150" fill="#2d2217" opacity="0.45" stroke="#4a331c" stroke-width="1.5"/>

    <!-- Custom center SVG decoration if any -->
    ${customCenterSvg || ''}

    <!-- Lower Plaque Backing for Text -->
    <rect x="48" y="520" width="${W - 96}" height="240" rx="6" fill="url(#textAreaGrad)" stroke="#4a331c" stroke-width="1.5" filter="url(#shadow)"/>
    <line x1="70" y1="520" x2="${W - 70}" y2="520" stroke="url(#goldGrad)" stroke-width="1.5"/>
    <line x1="70" y1="760" x2="${W - 70}" y2="760" stroke="url(#goldGrad)" stroke-width="1.5"/>

    <!-- Archival Seal at Bottom -->
    <g transform="translate(${W / 2}, 785)">
      <circle cx="0" cy="0" r="18" fill="#801010" stroke="#d4af37" stroke-width="1.5" filter="url(#shadow)"/>
      <circle cx="0" cy="0" r="14" fill="none" stroke="#d4af37" stroke-width="0.75" stroke-dasharray="2,2"/>
      <text x="0" y="4" font-family="serif" font-size="10" font-weight="bold" fill="#ffe4b5" text-anchor="middle">ČSR</text>
    </g>
    <text x="${W / 2}" y="818" font-family="serif" font-size="9" fill="#5a3d1c" text-anchor="middle" letter-spacing="1.5" font-weight="bold">
      ARCHIV ÚSTAVNÍHO DĚDICTVÍ • 1918–1938
    </text>
  </svg>
  `;

  const composites = [
    { input: Buffer.from(overlaySvg), top: 0, left: 0 }
  ];

  if (symbolBuffer) {
    // Center the symbol over the emblem frame (y: 285)
    const symMeta = await sharp(symbolBuffer).metadata();
    const symLeft = Math.round((W - symMeta.width) / 2);
    const symTop = Math.round(285 - symMeta.height / 2);
    composites.splice(0, 0, { input: symbolBuffer, top: symTop, left: symLeft });
  }

  await sharp(bg)
    .composite(composites)
    .png({ quality: 90, compressionLevel: 8 })
    .toFile(filename);

  console.log(`Generated card: ${filename}`);
}

async function main() {
  // 1. Karta Šlechta
  await createCard({
    filename: 'karta slechta.png',
    title: 'ZRUŠENÍ ŠLECHTICTVÍ',
    subTitle: 'ZÁKON Č. 61/1918 SB. • 10. PROSINCE 1918',
    symbolFile: 'korunka.png',
    customCenterSvg: `
      <!-- Red diagonal cancellation ribbon behind or over symbol -->
      <line x1="190" y1="390" x2="410" y2="180" stroke="#c41e24" stroke-width="10" opacity="0.85" stroke-linecap="round"/>
      <text x="300" y="425" font-family="Cinzel, serif" font-size="13" font-weight="bold" fill="#e0a845" text-anchor="middle" letter-spacing="2">
        ROVNOST OBČANŮ PŘED ZÁKONEM
      </text>
    `
  });

  // 2. Karta Washingtonská deklarace
  await createCard({
    filename: 'karta washington.png',
    title: 'WASHINGTONSKÁ DEKLARACE',
    subTitle: 'PROHLÁŠENÍ NEZÁVISLOSTI • 18. ŘÍJNA 1918',
    symbolFile: 'Parchment bez pozadí.png',
    customCenterSvg: `
      <g transform="translate(300, 275)">
        <circle cx="0" cy="0" r="110" fill="#20150b" stroke="#d4af37" stroke-width="3"/>
        <!-- Masaryk silhouette / Eagle Seal motif -->
        <path d="M-40,-50 L40,-50 L50,-30 L30,40 L0,65 L-30,40 L-50,-30 Z" fill="#8c6239" opacity="0.6"/>
        <path d="M-30,-20 C0,-60 0,-60 30,-20 C20,30 0,50 0,50 C0,50 -20,30 -30,-20 Z" fill="#d4af37" opacity="0.85"/>
        <circle cx="0" cy="-10" r="16" fill="#f5deb3"/>
        <text x="0" y="28" font-family="serif" font-size="14" font-weight="bold" fill="#fff" text-anchor="middle">T. G. M.</text>
        <text x="0" y="80" font-family="serif" font-size="11" font-weight="bold" fill="#ffd700" text-anchor="middle" letter-spacing="1">DEMOKRATICKÁ REPUBLIKA</text>
      </g>
    `
  });

  // 3. Karta Martinská deklarace (Bratia Slováci)
  await createCard({
    filename: 'karta bratia slovaci.png',
    title: 'MARTINSKÁ DEKLARACE',
    subTitle: 'DEKLARÁCIA SLOVENSKÉHO NÁRODA • 30. OKTÓBRA 1918',
    symbolFile: 'kriz.png',
    customCenterSvg: `
      <g transform="translate(300, 420)">
        <text x="0" y="0" font-family="Cinzel, serif" font-size="13" font-weight="bold" fill="#e0a845" text-anchor="middle" letter-spacing="2">
          JEDNOTA ČECHŮ A SLOVÁKŮ
        </text>
      </g>
    `
  });

  // 4. Karta Senát
  await createCard({
    filename: 'senat karta fin.png',
    title: 'VOLEBNÍ PRÁVO DO SENÁTU',
    subTitle: 'ÚSTAVA Č. 121/1920 SB. • § 20 • VĚKOVÝ CENZUS 45 LET',
    symbolFile: 'senat symbol fin.png',
    customCenterSvg: `
      <g transform="translate(300, 420)">
        <text x="0" y="0" font-family="Cinzel, serif" font-size="13" font-weight="bold" fill="#e0a845" text-anchor="middle" letter-spacing="2">
          SENÁT NÁRODNÍHO SHROMÁŽDĚNÍ
        </text>
      </g>
    `
  });

  // 5. Karta Volební povinnost
  await createCard({
    filename: 'volby karta fin.png',
    title: 'VOLEBNÍ POVINNOST',
    subTitle: 'ZÁKON Č. 123/1920 SB. • POVINNÁ ÚČAST U VOLEB',
    symbolFile: 'volby symbol fin.png',
    customCenterSvg: `
      <g transform="translate(300, 420)">
        <text x="0" y="0" font-family="Cinzel, serif" font-size="13" font-weight="bold" fill="#e0a845" text-anchor="middle" letter-spacing="2">
          DEMOKRATICKÁ ODPOVĚDNOST OBČANA
        </text>
      </g>
    `
  });

  console.log('All 5 cards created successfully!');
}

main().catch(err => {
  console.error('Error generating cards:', err);
  process.exit(1);
});
