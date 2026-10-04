import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const targets = ['public', 'dist'];

for (const target of targets) {
  const targetDir = path.join(__dirname, target);
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  // Copy individual root files
  ['index.html', 'trailer.html', '404.html', '.nojekyll', 'operation_sand_echo.json'].forEach(file => {
    const src = path.join(__dirname, file);
    if (fs.existsSync(src)) {
      fs.copyFileSync(src, path.join(targetDir, file));
    }
  });

  // Ensure 404.html exists in target
  const indexSrc = path.join(__dirname, 'index.html');
  const target404 = path.join(targetDir, '404.html');
  if (!fs.existsSync(target404) && fs.existsSync(indexSrc)) {
    fs.copyFileSync(indexSrc, target404);
  }

  // Copy images (*.jpeg, *.jpg, *.png)
  const files = fs.readdirSync(__dirname);
  files.filter(f => f.endsWith('.jpeg') || f.endsWith('.jpg') || f.endsWith('.png')).forEach(img => {
    fs.copyFileSync(path.join(__dirname, img), path.join(targetDir, img));
  });

  // Copy directories
  ['docs', 'store-assets', 'resource'].forEach(dir => {
    const srcDir = path.join(__dirname, dir);
    const destDir = path.join(targetDir, dir);
    if (fs.existsSync(srcDir)) {
      fs.cpSync(srcDir, destDir, { recursive: true });
    }
  });

  console.log(`[build] Successfully populated ${target}/`);
}
