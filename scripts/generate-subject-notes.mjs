// Creates a `*-notes.mdx` notebook page for every subject page.
// Notebooks are plain MDX files committed to the repo — edit them directly,
// they are never overwritten once created. Safe to re-run after adding subjects.
//
// Usage: node scripts/generate-subject-notes.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(fileURLToPath(import.meta.url));
const docsDir = path.join(root, '..', 'src', 'content', 'docs');

// Subject pages live exactly here (mirrors astro.config.mjs sidebar sections).
const SUBJECT_DIRS = [
	'year-1-required/winter',
	'year-1-required/summer',
	'year-1-optional/winter',
	'year-1-optional/summer',
	'year-2-required/winter',
	'year-2-required/summer',
	'year-2-optional/winter',
	'optional/winter',
	'optional/summer',
];

function readTitle(filePath) {
	const text = fs.readFileSync(filePath, 'utf8');
	const fm = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
	if (!fm) return null;
	const line = fm[1].match(/^title:\s*(?:"([^"]*)"|'([^']*)'|(.+?))\s*$/m);
	if (!line) return null;
	return (line[1] ?? line[2] ?? line[3] ?? '').trim();
}

function prettyName(basename) {
	return basename
		.split('-')
		.map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w))
		.join(' ');
}

function notesPageContent({ basename, title }) {
	const safeTitle = title.replace(/"/g, "'");
	return `---
title: "${safeTitle} — My Notes"
description: "Personal study notes for ${safeTitle}."
sidebar:
  label: "My Notes"
  order: 2
---

## ${title} — My Notes

Personal notebook for **${title}**. This page is a plain MDX file stored in the
repo alongside the course overview — edit it directly, commit it, and your notes
are versioned and never lost.

[← Back to course overview](./${basename})

## Key concepts

- Takeaway 1
- Takeaway 2

## Lecture log

### Week 1

Notes…

## Exam tips

- What to revise, typical questions, pitfalls.

## Questions to revisit

- [ ] Open question 1

## Links & resources

- [Resource](https://example.com)
`;
}

let created = 0;
let skipped = 0;
for (const dir of SUBJECT_DIRS) {
	const absDir = path.join(docsDir, dir);
	if (!fs.existsSync(absDir)) continue;
	for (const file of fs.readdirSync(absDir)) {
		if (!file.endsWith('.mdx')) continue;
		if (file.endsWith('-notes.mdx')) continue;
		if (file === 'index.mdx') continue;
		const basename = file.replace(/\.mdx$/, '');
		const title = readTitle(path.join(absDir, file)) || prettyName(basename);
		const outPath = path.join(absDir, `${basename}-notes.mdx`);
		// Never touch an existing notebook — it may contain the user's notes.
		if (fs.existsSync(outPath)) {
			skipped++;
			continue;
		}
		fs.writeFileSync(outPath, notesPageContent({ basename, title }));
		created++;
	}
}
console.log(`Subject notes pages: ${created} created, ${skipped} already existed (left untouched).`);
