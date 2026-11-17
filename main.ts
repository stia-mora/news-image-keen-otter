// news-image-20261117 entry: "THE WORLD IN ONE DAY" (Node 22, stdlib only).
//
// The artwork lives in entry.png next to this file (1024x1024, drawn with
// PIL by draw.py). This program's only job is to place an exact copy of it
// at <output dir>/entry.png, so the judge sees the same bytes every run.
//
// The output directory comes from MAKEFUN_OUTPUT_DIR; without it we fall
// back to /output, the directory the grader mounts.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (looked in ${here})`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target}`);
