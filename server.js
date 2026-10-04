import express from 'express';
import path from 'path';
import fs from 'fs';
import { exec } from 'child_process';
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

// Python Engine Battle Simulation Endpoint
app.post('/api/battle/simulate', (req, res) => {
  exec('python3 main.py --json-sim', { cwd: __dirname }, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({ error: 'Python simulation failed', details: stderr });
    }
    try {
      const data = JSON.parse(stdout);
      res.json(data);
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse simulation output', raw: stdout });
    }
  });
});

// Squad roster from Python Engine
app.get('/api/squad', (req, res) => {
  exec('python3 SquadMember.py', { cwd: __dirname }, (error, stdout) => {
    if (!error && stdout.includes('{')) {
      try {
        const jsonPart = stdout.substring(stdout.indexOf('{'));
        return res.json(JSON.parse(jsonPart));
      } catch {}
    }
    res.json({ squad: "Oistarian Recon", status: "Active" });
  });
});

// Python Engine Status
app.get('/api/python/health', (req, res) => {
  exec('python3 main.py --test', { cwd: __dirname }, (error, stdout) => {
    res.json({
      status: error ? 'error' : 'online',
      tests_passed: !error,
      system: 'Tactical Legends Python Engine',
      output: stdout.split('\n').filter(Boolean)
    });
  });
});

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
