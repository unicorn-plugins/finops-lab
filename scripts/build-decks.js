#!/usr/bin/env node
/**
 * build-decks.js
 * Converts Marp deck .md files to .pptx using PptxGenJS
 *
 * Usage: node scripts/build-decks.js
 */

'use strict';

const fs = require('fs');
const path = require('path');

// Load pptxgenjs from global npm path
let PptxGenJS;
try {
  PptxGenJS = require('pptxgenjs');
} catch (e) {
  const globalRoot = 'C:/Users/hiond/.npm-global/node_modules';
  PptxGenJS = require(path.join(globalRoot, 'pptxgenjs'));
}

// ─── Constants ────────────────────────────────────────────────────────────────
const DECK_DIR = path.resolve(__dirname, '../out/ppt-scripts');
const IMG_DIR  = path.join(DECK_DIR, 'images');

const COLORS = {
  dark:    '2C2926',
  green:   '059669',
  teal:    '0D9488',
  grey:    '505060',
  white:   'FFFFFF',
  lightGreen: 'D1FAE5',
  coverTeal: '0D9488',
  coverBlue: '1A5E7E',
};

const FONT = 'Pretendard';

const DECKS = [
  { slug: 'why-maturity',  file: 'why-maturity-deck.md',  expectedSlides: 6, coverBg: COLORS.dark },
  { slug: 'inform',        file: 'inform-deck.md',         expectedSlides: 5, coverBg: COLORS.coverTeal },
  { slug: 'optimize',      file: 'optimize-deck.md',       expectedSlides: 6, coverBg: COLORS.green },
  { slug: 'operate',       file: 'operate-deck.md',        expectedSlides: 5, coverBg: COLORS.dark },
  { slug: 'review',        file: 'review-deck.md',         expectedSlides: 5, coverBg: COLORS.coverBlue },
];

// Slide dimensions in inches (1152×648 pt ≈ 16×9 in at 72pt/in)
const SLIDE_W = 16;
const SLIDE_H = 9;

// Layout margins in inches
const MARGIN_L = 0.5;
const MARGIN_T = 0.5;
const CONTENT_W = SLIDE_W - MARGIN_L * 2;

// ─── Parser ──────────────────────────────────────────────────────────────────

/**
 * Parse Marp markdown into { frontmatter: string, slides: SlideData[] }
 * SlideData: { isCover: bool, title: string, subtitle: string, body: string[], notes: string,
 *              table: { headers, rows } | null, image: string | null, coverSubtitle: string | null,
 *              coverPara: string | null }
 */
function parseDeck(mdText) {
  // Split off YAML frontmatter (first --- ... ---)
  const fmMatch = mdText.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!fmMatch) throw new Error('No frontmatter found');

  const body = fmMatch[2];

  // Split remaining content by slide separators (--- on its own line)
  // but NOT inside tables (lines starting with |)
  const rawSlides = body.split(/\n---\n/);

  const slides = rawSlides.map((raw, idx) => parseSlide(raw.trim(), idx === 0));
  return { slides };
}

function parseSlide(raw, isFirstSlide) {
  // Check for cover class directive
  const isCover = /<!--\s*_class:\s*cover\s*-->/.test(raw) || isFirstSlide;

  // Extract HTML comments (speaker notes) — but NOT Marp directives like _class
  const noteMatches = [...raw.matchAll(/<!--(?!\s*_)([\s\S]*?)-->/g)];
  const notes = noteMatches
    .map(m => m[1].replace(/^[\s\n]*Speaker Notes:\s*/i, '').trim())
    .join('\n\n')
    .trim();

  // Remove all HTML comments from the text for parsing
  const clean = raw.replace(/<!--[\s\S]*?-->/g, '').trim();

  // Extract image reference: ![alt](images/xxx.png)
  const imgMatch = clean.match(/!\[([^\]]*)\]\(images\/([^)]+)\)/);
  const image = imgMatch ? imgMatch[2] : null;

  // Remove image markdown from clean text
  const cleanNoImg = clean.replace(/!\[([^\]]*)\]\([^)]+\)/g, '').trim();

  // Extract HTML inline elements (badges, div tags) — just get their text content
  const cleanNoHtml = cleanNoImg.replace(/<[^>]+>/g, '').trim();

  // Parse lines
  const lines = cleanNoHtml.split('\n').map(l => l.trimEnd()).filter(l => l.length > 0);

  // Find title (# H1) and subtitle (## H2)
  let title = '';
  let subtitle = '';
  let coverPara = '';
  const bodyLines = [];
  const tableLines = [];
  let inTable = false;

  for (const line of lines) {
    if (line.startsWith('# ')) {
      title = line.replace(/^#\s+/, '');
    } else if (line.startsWith('## ')) {
      subtitle = line.replace(/^##\s+/, '');
    } else if (line.startsWith('### ')) {
      bodyLines.push({ type: 'h3', text: line.replace(/^###\s+/, '') });
    } else if (line.startsWith('| ') || line.startsWith('|---') || line.startsWith('|:')) {
      tableLines.push(line);
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      bodyLines.push({ type: 'bullet', text: line.replace(/^[-*]\s+/, '') });
    } else if (line.startsWith('**') && line.endsWith('**') && !line.includes('\n')) {
      bodyLines.push({ type: 'bold', text: line.replace(/\*\*/g, '') });
    } else if (line.trim().length > 0) {
      // Paragraph text
      if (isCover && line.startsWith('<p>')) {
        coverPara = line.replace(/<\/?p>/g, '');
      } else if (line.trim().length > 0 && !line.startsWith('<')) {
        bodyLines.push({ type: 'para', text: line });
      }
    }
  }

  // Parse table
  let table = null;
  if (tableLines.length >= 2) {
    table = parseTable(tableLines);
  }

  return { isCover, title, subtitle, coverPara, bodyLines, table, image, notes };
}

function parseTable(lines) {
  // Filter out separator rows (|---|---|)
  const dataLines = lines.filter(l => !/^\|[\s\-:|]+\|$/.test(l) && !/^[\s\-]+$/.test(l));

  const parseRow = (line) => {
    return line.split('|')
      .filter((_, i, arr) => i > 0 && i < arr.length - 1)
      .map(cell => stripMarkdown(cell.trim()));
  };

  if (dataLines.length === 0) return null;

  const headers = parseRow(dataLines[0]);
  const rows = dataLines.slice(1).map(parseRow);

  return { headers, rows };
}

/** Strip basic markdown bold/em/code from text */
function stripMarkdown(text) {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/_([^_]+)_/g, '$1')
    .trim();
}

// ─── Slide Builder ────────────────────────────────────────────────────────────

function addCoverSlide(pptx, slideData, coverBg) {
  const slide = pptx.addSlide();

  // Dark background
  slide.background = { fill: coverBg };

  // Title
  if (slideData.title) {
    slide.addText(slideData.title, {
      x: MARGIN_L, y: 2.5, w: CONTENT_W, h: 1.2,
      fontFace: FONT,
      fontSize: 40,
      bold: true,
      color: COLORS.white,
      wrap: true,
      valign: 'middle',
    });
  }

  // Subtitle (## heading on cover)
  if (slideData.subtitle) {
    slide.addText(slideData.subtitle, {
      x: MARGIN_L, y: 3.9, w: CONTENT_W, h: 0.7,
      fontFace: FONT,
      fontSize: 22,
      bold: false,
      color: COLORS.lightGreen,
      wrap: true,
    });
  }

  // Cover paragraph
  if (slideData.coverPara) {
    slide.addText(slideData.coverPara, {
      x: MARGIN_L, y: 4.8, w: CONTENT_W, h: 0.5,
      fontFace: FONT,
      fontSize: 14,
      color: 'D1FAE5',
      wrap: true,
    });
  }

  // Speaker notes
  if (slideData.notes) {
    slide.addNotes(slideData.notes);
  }
}

function addContentSlide(pptx, slideData) {
  const slide = pptx.addSlide();

  // White background
  slide.background = { fill: COLORS.white };

  // Slide title (## heading)
  const titleText = slideData.subtitle || slideData.title;
  if (titleText) {
    slide.addText(titleText, {
      x: MARGIN_L, y: MARGIN_T, w: CONTENT_W, h: 0.65,
      fontFace: FONT,
      fontSize: 26,
      bold: true,
      color: COLORS.dark,
      wrap: true,
    });

    // Green accent line under title
    slide.addShape(pptx.ShapeType.rect, {
      x: MARGIN_L, y: MARGIN_T + 0.65, w: CONTENT_W, h: 0.03,
      fill: { color: COLORS.green },
      line: { color: COLORS.green, width: 0 },
    });
  }

  const contentY = MARGIN_T + 0.75;
  const hasImage = !!slideData.image;
  const contentW = hasImage ? CONTENT_W * 0.52 : CONTENT_W;
  const imageX = MARGIN_L + CONTENT_W * 0.54;
  const imageW = CONTENT_W * 0.46;

  // Image (right side if present)
  if (hasImage) {
    const imgPath = path.join(IMG_DIR, slideData.image);
    if (fs.existsSync(imgPath)) {
      slide.addImage({
        path: imgPath,
        x: imageX, y: contentY, w: imageW, h: SLIDE_H - contentY - 0.3,
        sizing: { type: 'contain', w: imageW, h: SLIDE_H - contentY - 0.3 },
      });
    }
  }

  // Table
  if (slideData.table) {
    const { headers, rows } = slideData.table;
    const tableH = Math.min(0.35 * (rows.length + 1), SLIDE_H - contentY - 0.2);

    const tableData = [
      headers.map(h => ({
        text: h,
        options: {
          bold: true,
          fontSize: 11,
          fontFace: FONT,
          color: COLORS.dark,
          fill: { color: 'E2EEF9' },
          align: 'left',
        }
      })),
      ...rows.map(row => row.map(cell => ({
        text: cell,
        options: {
          fontSize: 11,
          fontFace: FONT,
          color: COLORS.grey,
          align: 'left',
        }
      })))
    ];

    // Make sure each row has same column count as headers
    const colCount = headers.length;
    const normalizedData = tableData.map(row => {
      while (row.length < colCount) row.push({ text: '', options: { fontSize: 11, fontFace: FONT, color: COLORS.grey } });
      return row.slice(0, colCount);
    });

    slide.addTable(normalizedData, {
      x: MARGIN_L, y: contentY, w: contentW, h: tableH,
      rowH: 0.32,
      border: { type: 'solid', color: 'E2E8F0', pt: 0.5 },
      fill: { color: COLORS.white },
    });

    // Bullets below table if any
    const bulletY = contentY + tableH + 0.05;
    const bullets = slideData.bodyLines.filter(l => l.type === 'bullet' || l.type === 'bold' || l.type === 'para');
    if (bullets.length > 0 && bulletY < SLIDE_H - 0.3) {
      addBullets(slide, bullets, MARGIN_L, bulletY, contentW, SLIDE_H - bulletY - 0.2);
    }
  } else if (slideData.bodyLines.length > 0) {
    // Bullets / paragraphs only
    const bullets = slideData.bodyLines.filter(l => l.type === 'bullet' || l.type === 'bold' || l.type === 'para' || l.type === 'h3');
    if (bullets.length > 0) {
      addBullets(slide, bullets, MARGIN_L, contentY, contentW, SLIDE_H - contentY - 0.3);
    }
  }

  if (slideData.notes) {
    slide.addNotes(slideData.notes);
  }
}

function addBullets(slide, lines, x, y, w, h) {
  const textLines = lines.map(line => {
    if (line.type === 'h3') {
      return {
        text: line.text,
        options: {
          fontSize: 14,
          bold: true,
          color: COLORS.teal,
          bullet: false,
          breakLine: true,
        }
      };
    } else if (line.type === 'bold') {
      return {
        text: line.text,
        options: {
          fontSize: 13,
          bold: true,
          color: COLORS.dark,
          bullet: false,
          breakLine: true,
        }
      };
    } else if (line.type === 'bullet') {
      return {
        text: stripMarkdown(line.text),
        options: {
          fontSize: 13,
          color: COLORS.grey,
          bullet: { type: 'bullet', indent: 15 },
          breakLine: true,
        }
      };
    } else {
      return {
        text: stripMarkdown(line.text),
        options: {
          fontSize: 13,
          color: COLORS.grey,
          bullet: false,
          breakLine: true,
        }
      };
    }
  });

  slide.addText(textLines, {
    x, y, w, h,
    fontFace: FONT,
    valign: 'top',
    wrap: true,
    paraSpaceAfter: 4,
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function buildDeck(deckDef) {
  const mdPath = path.join(DECK_DIR, deckDef.file);
  const outPath = path.join(DECK_DIR, `${deckDef.slug}-deck.pptx`);

  console.log(`\n[BUILD] ${deckDef.file} → ${deckDef.slug}-deck.pptx`);

  const mdText = fs.readFileSync(mdPath, 'utf8');
  const { slides } = parseDeck(mdText);
  console.log(`  Parsed ${slides.length} slides (expected ${deckDef.expectedSlides})`);

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'HBT16x9', width: SLIDE_W, height: SLIDE_H });
  pptx.layout = 'HBT16x9';
  pptx.author = 'HBT FinOps Team';
  pptx.subject = deckDef.slug;

  slides.forEach((slideData, idx) => {
    if (slideData.isCover && idx === 0) {
      addCoverSlide(pptx, slideData, deckDef.coverBg);
    } else {
      addContentSlide(pptx, slideData);
    }
  });

  await pptx.writeFile({ fileName: outPath });
  console.log(`  Written: ${outPath}`);

  const stat = fs.statSync(outPath);
  console.log(`  Size: ${(stat.size / 1024).toFixed(1)} KB`);

  return { slug: deckDef.slug, file: `${deckDef.slug}-deck.pptx`, slides: slides.length, sizeKB: (stat.size / 1024).toFixed(1) };
}

async function main() {
  console.log('=== HBT FinOps Deck Builder ===');
  const results = [];

  for (const deck of DECKS) {
    try {
      const result = await buildDeck(deck);
      results.push({ ...result, status: 'OK' });
    } catch (err) {
      console.error(`  ERROR building ${deck.slug}: ${err.message}`);
      results.push({ slug: deck.slug, file: `${deck.slug}-deck.pptx`, slides: 0, sizeKB: 0, status: `ERROR: ${err.message}` });
    }
  }

  console.log('\n=== Results ===');
  console.log('| 파일명 | 슬라이드 수 | 파일 크기 | 상태 |');
  console.log('|--------|-----------|---------|------|');
  results.forEach(r => {
    console.log(`| ${r.file} | ${r.slides} | ${r.sizeKB} KB | ${r.status} |`);
  });
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
