import express from 'express';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;
const HOST = '0.0.0.0';

app.use(express.json());

// Serve static assets from public, root and docs directory
app.use(express.static(path.join(__dirname, 'public')));
app.use('/docs', express.static(path.join(__dirname, 'docs')));
app.use('/store-assets', express.static(path.join(__dirname, 'store-assets')));
app.use(express.static(__dirname));

// Optional lightweight JSON endpoints based on repo datasets
app.get('/api/codex', (req, res) => {
  const codexPath = path.join(__dirname, 'resource', 'CODEX.json');
  if (fs.existsSync(codexPath)) {
    try {
      const data = fs.readFileSync(codexPath, 'utf8');
      return res.json(JSON.parse(data.split('\n\nC#')[0]));
    } catch {
      return res.json({ error: 'Failed to read codex' });
    }
  }
  res.json({ factions: [], relics: [], operatives: [] });
});

app.get('/api/operation', (req, res) => {
  const opPath = path.join(__dirname, 'operation_sand_echo.json');
  if (fs.existsSync(opPath)) {
    try {
      const data = fs.readFileSync(opPath, 'utf8');
      return res.json(JSON.parse(data.split('\n\nvoice_lines')[0]));
    } catch {
      return res.json({ error: 'Failed to read operation' });
    }
  }
  res.json({ mission: 'operation_sand_echo' });
});

// Primary landing page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Cinematic Introduction & AI Voice Trailer page
app.get('/trailer', (req, res) => {
  res.sendFile(path.join(__dirname, 'trailer.html'));
});

// Wildcard fallback for HTML routing
app.get('*', (req, res) => {
  if (req.accepts('html')) {
    res.sendFile(path.join(__dirname, 'index.html'));
  } else {
    res.status(404).json({ error: 'Not found' });
  }
});

app.listen(PORT, HOST, () => {
  console.log(`Tactical Legends web app is running at http://${HOST}:${PORT}`);
});
