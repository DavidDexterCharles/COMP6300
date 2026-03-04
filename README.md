# COMP6300

Week 7 Lab: Implement React App

This repo uses the **production** way to build React apps: scaffold with a build tool, then run and build. The standard approach is **Vite** with the React template (fast, minimal, recommended over Create React App). From here you can later move to **Next.js** when you need a full-stack framework.

---

## Prerequisites

- **Node.js 20.19+ or 22.12+** (includes `npm` and `npx`). Vite requires this; Node 18 will fail with errors like `crypto.hash is not a function`. Check your version with `node -v`. If you need to upgrade, use the installer from [nodejs.org](https://nodejs.org/) or manage versions with **nvm** (below).

### Managing Node version with nvm

**nvm** (Node Version Manager) lets you install and switch between multiple Node.js versions on the same machine.

**Windows (nvm-windows)**

1. Download the latest **nvm-setup.exe** from [nvm-windows releases](https://github.com/coreybutler/nvm-windows/releases).
2. Run the installer. It will set up `nvm` and ask you to uninstall any existing Node.js so nvm can manage it.
3. Open a **new** Command Prompt or PowerShell. Run:
   ```bash
   nvm install 22
   nvm use 22
   node -v
   ```
   Use `20` instead of `22` if you prefer Node 20 LTS.

**macOS / Linux**

1. Install nvm (restart the terminal or run `source ~/.bashrc` or `source ~/.zshrc` afterward if needed):
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
   ```
2. Install and use a compatible Node version:
   ```bash
   nvm install 22
   nvm use 22
   node -v
   ```

**Useful nvm commands**

| Command                | Purpose                              |
| ---------------------- | ------------------------------------ |
| `nvm list`             | Show installed versions              |
| `nvm install 22`       | Install Node 22                      |
| `nvm use 22`           | Use Node 22 in this shell            |
| `nvm alias default 22` | Use Node 22 by default in new shells |

---

## 1. Scaffold the React app

From your project root (e.g. `COMP6300`), run:

```bash
npm create vite@latest my-app -- --template react
```

- **`npm create vite@latest`** — runs the Vite scaffolding tool (no global install).
- **`my-app`** — name of the new folder and project; change it if you like (e.g. `react-app`).
- **`-- --template react`** — use the React (JavaScript) template; use `react-ts` for TypeScript.

When prompted, you can accept defaults (or choose no to “Git” if the repo is already under Git).

This creates a folder (e.g. `my-app/`) with a full Vite + React setup.

---

## 2. Project layout (after scaffolding)

```
my-app/
├── node_modules/     (created by npm install)
├── public/
│   └── vite.svg
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx      (entry: mounts React into index.html)
│   ├── index.css     (global styles)
│   └── assets/
├── index.html        (single HTML shell; script loads src/main.jsx)
├── package.json
├── vite.config.js
└── README.md
```

---

## 3. Install dependencies and run

```bash
cd my-app
npm install
npm run dev
```

Then open the URL shown in the terminal (e.g. `http://localhost:5173`). You get hot reload while editing.

---

## 4. Build for production

```bash
npm run build
```

Output goes to **`dist/`**. Deploy the contents of `dist/` to any static host (e.g. Netlify, Vercel, or your own server). To preview the production build locally:

```bash
npm run preview
```

---

## 5. Summary of npm scripts

| Script            | Purpose                        |
| ----------------- | ------------------------------ |
| `npm run dev`     | Start dev server (hot reload)  |
| `npm run build`   | Build for production → `dist/` |
| `npm run preview` | Serve `dist/` locally          |

---

## Next steps

- Edit `src/App.jsx` and add components under `src/` as needed.
- When you need routing, SSR, or API routes, consider moving to **Next.js** and reusing your React components.
