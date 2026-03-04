# COMP6300

Week 7 Lab: Implement React App

This repo starts with **simple React in HTML** (no build step) here we keep things minimal.

---

## Basic React: Imperative vs declarative (start here)

To see the difference between **imperative** (plain JS, direct DOM) and **declarative** (React) UIs, use two single-file examples. No Node, no build — just open the HTML files in a browser (or serve them with any static server).

### Folder for the basic examples

```
react-basics/
├── imperative.html     ← Plain HTML + vanilla JS (imperative)
├── declarative.html    ← HTML + React via CDN (declarative)
└── declarative2.html   ← Same idea, illustrates passing parameters to handlers
```

### 1. Imperative: plain HTML + vanilla JavaScript

One file: **`react-basics/imperative.html`**. You **tell the browser exactly what to do**: get elements, create nodes, set text, attach listeners.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Imperative counter</title>
  </head>
  <body>
    <h1>Imperative (plain JS)</h1>
    <p>Count: <span id="count">0</span></p>
    <button id="inc">+1</button>
    <button id="dec">-1</button>

    <script>
      let count = 0;
      const countEl = document.getElementById("count");
      const incBtn = document.getElementById("inc");
      const decBtn = document.getElementById("dec");

      function updateUI() {
        countEl.textContent = count;
      }

      incBtn.addEventListener("click", function () {
        count++;
        updateUI();
      });
      decBtn.addEventListener("click", function () {
        count--;
        updateUI();
      });

      updateUI();
    </script>
  </body>
</html>
```

You manually: read/write the DOM, keep `count` in a variable, and sync the `<span>` with `updateUI()`.

### 2. Declarative: same UI with React (in HTML, no build)

One file: **`react-basics/declarative.html`**. You **describe what the UI should look like** for a given state; React updates the DOM for you.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Declarative counter (React)</title>
    <script
      crossorigin
      src="https://unpkg.com/react@18/umd/react.development.js"
    ></script>
    <script
      crossorigin
      src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"
    ></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  </head>
  <body>
    <div id="root"></div>

    <script type="text/babel">
      const { useState } = React;

      function Counter() {
        const [count, setCount] = useState(0);
        return (
          <div>
            <h1>Declarative (React)</h1>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+1</button>
            <button onClick={() => setCount(count - 1)}>-1</button>
          </div>
        );
      }

      const root = ReactDOM.createRoot(document.getElementById("root"));
      root.render(<Counter />);
    </script>
  </body>
</html>
```

Here you only declare: “when `count` is X, show this.” React handles DOM updates. This is **React in HTML** — no npm or bundler; next step later is a proper React app, then Next.js.

### 3. Passing parameters: `declarative2.html`

File **`react-basics/declarative2.html`** extends the counter with **named functions** and shows how to **pass parameters** to event handlers.

- **Named function, no parameters:** You can replace an inline handler with a named function and pass it directly to `onClick`:

  ```js
  function increment() {
    setCount(count + 1);
  }
  // ...
  <button onClick={increment}>+1</button>;
  ```

  Same behaviour as `onClick={() => setCount(count + 1)}`, but clearer when the logic grows.

- **Passing a parameter:** To pass an argument (e.g. increment by 2), you must wrap the call in an arrow function. Otherwise React would call your function immediately on render instead of on click:

  ```js
  function incrementBy(value) {
    setCount(count + value);
  }
  // ...
  <button onClick={() => incrementBy(2)}>+2</button>;
  ```

  So: no args → `onClick={increment}`; with args → `onClick={() => incrementBy(2)}`.

### How to run the basic examples

- **Option A:** Open `imperative.html`, `declarative.html`, or `declarative2.html` directly in the browser (file://). For the React files, Babel loads from CDN so you need internet.
- **Option B:** From the repo root run:

  ```bash
  npx --yes serve .
  ```

  This runs the **serve** package (a small static file server) without installing it globally: **npx** fetches and runs the package, **--yes** skips the install prompt, and **.** means “serve the current directory.” You’ll get a local URL (e.g. `http://localhost:3000`). Then open e.g. `http://localhost:3000/react-basics/imperative.html`, `.../declarative.html`, and `.../declarative2.html`.

  **Don’t have `npx`?** `npx` is included with **Node.js** (it ships with npm). Install Node.js from [nodejs.org](https://nodejs.org/) (LTS is fine). After installation, restart your terminal and run `npx --yes serve .` again.

---
