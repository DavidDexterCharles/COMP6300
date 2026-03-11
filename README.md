# COMP6300

Week 8 Lab: Implement React App

This repo uses the **production** way to build React apps: scaffold with a build tool, then run and build. The standard approach is **Vite** with the React template (fast, minimal, recommended over Create React App), plus **Tailwind CSS** for styling. From here you can later move to **Next.js** when you need a full-stack framework.

---

## Prerequisites

- **Node.js 20.19+ or 22.12+** (includes `npm` and `npx`). Vite requires this; Node 18 will fail with errors like `crypto.hash is not a function`. Check your version with `node -v`. If you need to upgrade, use the installer from [nodejs.org](https://nodejs.org/) or manage versions with **nvm** (below).

### Managing Node version with nvm

**nvm** (Node Version Manager) lets you install and switch between multiple Node.js versions on the same machine.

**Windows (nvm-windows)**

1. Download the latest **nvm-setup.exe** from [nvm-windows releases](https://github.com/coreybutler/nvm-windows/releases).
2. Run the installer. It will set up `nvm` and ask you to uninstall any existing Node.js so nvm can manage it.
3. Open a **new** Command Prompt or PowerShell (As Administrator). Run:
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

When prompted, you can accept defaults (or choose no to "Git" if the repo is already under Git).

This creates a folder (e.g. `my-app/`) with a full Vite + React setup.

---

## 2. Install dependencies (including Tailwind CSS v4)

From your project root, run:

```bash
cd my-app
npm install
npm install -D tailwindcss @tailwindcss/vite
```

**Tailwind v4** does not use `tailwindcss init` or `tailwind.config.js`. Configure it as follows.

**1. Add the Vite plugin** — In `my-app/vite.config.js`, add the Tailwind plugin:

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

**2. Import Tailwind in CSS** — Clear out index.css and At the top of `my-app/src/index.css`, add:

```css
@import "tailwindcss";

/* your existing or custom global styles below */
```

Tailwind v4 auto-detects content (no `content` array). Optional: use `@theme { ... }` in CSS for custom design tokens. You do **not** need `postcss.config.js` or `tailwind.config.js` when using the Vite plugin.

---

## 3. Project layout (after scaffolding and Tailwind setup)

```
my-app/
├── node_modules/
├── public/
│   └── vite.svg
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   ├── index.css          ← @import "tailwindcss"; here
│   └── components/        ← you will add this folder
├── index.html
├── package.json
├── vite.config.js         ← Tailwind added via @tailwindcss/vite
└── README.md
```

---

## 4. Run the dev server

```bash
cd my-app
npm run dev
```

Open the URL shown in the terminal (e.g. `http://localhost:5173`). You get hot reload while editing.

---

## 5. Build for production

```bash
npm run build
```

Output goes to **`dist/`**. Deploy the contents of `dist/` to any static host. To preview the production build locally:

```bash
npm run preview
```

---

## 6. Summary of npm scripts

| Script            | Purpose                        |
| ----------------- | ------------------------------ |
| `npm run dev`     | Start dev server (hot reload)  |
| `npm run build`   | Build for production → `dist/` |
| `npm run preview` | Serve `dist/` locally          |

---

## 7. Lab: Course list app

Follow these steps to clear the default Vite content and build a small course list app. Use **hardcoded data** only (no local storage or backend). You will implement:

- **Course** — a card for one course (code + title).
- **CourseListing** — tiles/cards left to right; create, read, update, delete courses; Create and Edit use small modals.
- **CourseSearch** — search/filter by course code or title.

`App.jsx` stays minimal: it only imports and renders a single component that contains the course list, search, and listing.

---

### 7.1 Clear out the default React app

1. **`src/App.jsx`** — Remove the default Vite markup (logo, “Vite + React” content, etc.). You will replace it with a minimal root that only imports and renders the course app component (see 7.5).
2. **`src/App.css`** — Remove or simplify default styles; layout and cards will use Tailwind.
3. **`src/index.css`** — Keep the `@import "tailwindcss";` you added in step 2; add any extra global styles only if needed.

---

### 7.2 Data model and sample data

Each course has:

- **Course Code** (e.g. `COMP 6501`)
- **Course Title** (e.g. `Research Methods, Entrepreneurship and Intellectual Property`)
- **Category**: `"Core"` or `"Elective"` (for display/grouping)

Use a simple **`id`** (number or string) for each course so you can update and delete by id. Store the list in state (e.g. in the component that wraps `CourseListing`). Use the following **hardcoded** initial data (no local storage):

**Core courses**

| Course Code | Course Title                                                 |
| ----------- | ------------------------------------------------------------ |
| COMP 6501   | Research Methods, Entrepreneurship and Intellectual Property |
| COMP 6925   | Applied Operations Research                                  |
| STAT 6105   | Probability and Statistical Methods for Data Analytics       |
| STAT 6106   | Statistical Inference for Data Analytics                     |
| COMP 6930   | Machine Learning and Data Mining                             |
| COMP 6940   | Big Data and Visual Analytics                                |
| STAT 6005   | Research Project                                             |

**Elective courses**

| Course Code | Course Title                              |
| ----------- | ----------------------------------------- |
| COMP 6300   | Advanced Internet Technologies            |
| COMP 6401   | Advanced Algorithms                       |
| COMP 6802   | Distributed and Parallel Database Systems |
| COMP 6905   | Cloud Technologies                        |
| STAT 6160   | Data Analysis                             |
| STAT 6170   | Multivariate Analysis                     |
| STAT 6181   | Computational Statistics I                |
| STAT 6182   | Computational Statistics II               |

Example structure for one course in code:

```js
{ id: 1, code: "COMP 6501", title: "Research Methods, Entrepreneurship and Intellectual Property", category: "Core" }
```

Initialize state with an array of such objects for all courses above.

---

### 7.3 Components to implement

**1. Course (course card)**

- A **card** that displays one course: **Course Code** and **Course Title** (and optionally category).
- Props: e.g. `course` (object with `code`, `title`, `category`) and optionally `onEdit`, `onDelete` so the parent can handle edit/delete when the user clicks buttons on the card.

**2. CourseListing**

- Shows the list of courses as **tiles/cards in a row** (left to right), each tile being a `Course` card.
- **Create**: a “Create” button that opens a **small modal** to enter Course Code and Course Title (and optionally category); on submit, add the new course to the list.
- **Read**: display all courses (or the filtered list from search).
- **Update**: “Edit” on a card opens a **small modal** with the current code and title; on save, update that course in the list.
- **Delete**: remove a course from the list (e.g. “Delete” button on the card).
- The list can be held in state in this component or in a parent; for this lab, updating state is enough (no persistence).

**3. CourseSearch**

- A **search/filter** control (e.g. text input).
- When the user types, **filter** the courses by course code and/or title (e.g. case-insensitive match).
- Either pass the search term up to a parent that holds the list and filters there, or pass the full list down and filter inside `CourseSearch` and pass the filtered list to the listing—as long as the listing shows only matching courses while the user searches.

---

### 7.4 Keep App.jsx minimal

- **App.jsx** should stay minimal: import a single component that contains all course logic (state, search, listing, create/edit/delete).
- That component (e.g. `CourseManager` or `CourseApp`) holds:
  - The courses state (initialized with the hardcoded data).
  - The search term state.
  - The filtered list (or filter logic).
  - Handlers for create, update, delete.
  - It renders **CourseSearch** at the top and **CourseListing** below (with the filtered list and handlers passed as props as needed).

---

### 7.5 File structure (suggestion)

```
src/
├── App.jsx              ← minimal: import CourseManager and render it
├── App.css
├── main.jsx
├── index.css
└── components/
    ├── CourseManager.jsx  ← state, search term, filter, handlers; renders CourseSearch + CourseListing
    ├── Course.jsx         ← card for one course (code + title)
    ├── CourseListing.jsx  ← tiles left-to-right, Create/Edit modals, Delete
    └── CourseSearch.jsx   ← search input, filter by code/title
```

---

### 7.6 Copy-paste implementation

Use a **lighter theme** (e.g. light background, subtle borders) and **Tailwind CSS** for all layout and styling. **Paste in this order** so the app does not break: create the component files first (1–4), then update `App.jsx` and `App.css` (5–6).

**1. `src/components/Course.jsx`** (card for one course):

```jsx
export default function Course({ course, onEdit, onDelete }) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
      <div className="font-medium text-slate-800">{course.code}</div>
      <div className="text-sm text-slate-600 mt-1">{course.title}</div>
      {course.category && (
        <span className="inline-block mt-2 text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600">
          {course.category}
        </span>
      )}
      <div className="mt-3 flex gap-2">
        <button
          type="button"
          onClick={() => onEdit(course)}
          className="text-sm px-3 py-1.5 rounded bg-slate-200 text-slate-700 hover:bg-slate-300"
        >
          Edit
        </button>
        <button
          type="button"
          onClick={() => onDelete(course.id)}
          className="text-sm px-3 py-1.5 rounded bg-red-100 text-red-700 hover:bg-red-200"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
```

**2. `src/components/CourseSearch.jsx`**:

```jsx
export default function CourseSearch({ value, onChange }) {
  return (
    <div className="mb-6">
      <input
        type="text"
        placeholder="Search by course code or title..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full max-w-md px-4 py-2 border border-slate-300 rounded-lg bg-white text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:border-transparent"
      />
    </div>
  );
}
```

**3. `src/components/CourseListing.jsx`** (tiles, Create/Edit modals, Delete):

```jsx
import { useState } from "react";
import Course from "./Course";

export default function CourseListing({
  courses,
  onCreate,
  onUpdate,
  onDelete,
}) {
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState(null);

  function openCreate() {
    setEditingCourse(null);
    setModalOpen(true);
  }

  function openEdit(course) {
    setEditingCourse(course);
    setModalOpen(true);
  }

  function closeModal() {
    setModalOpen(false);
    setEditingCourse(null);
  }

  function handleSubmit(e) {
    e.preventDefault();
    const form = e.target;
    const code = form.code.value.trim();
    const title = form.title.value.trim();
    const category = form.category?.value?.trim() || "Core";
    if (!code || !title) return;
    if (editingCourse) {
      onUpdate(editingCourse.id, { code, title, category });
    } else {
      onCreate({ code, title, category });
    }
    closeModal();
  }

  return (
    <>
      <div className="flex flex-wrap gap-4">
        <button
          type="button"
          onClick={openCreate}
          className="h-[120px] w-[280px] flex items-center justify-center rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 text-slate-500 hover:border-slate-400 hover:bg-slate-100 transition-colors"
        >
          + Create course
        </button>
        {courses.map((course) => (
          <div key={course.id} className="w-[280px]">
            <Course course={course} onEdit={openEdit} onDelete={onDelete} />
          </div>
        ))}
      </div>

      {modalOpen && (
        <div
          className="fixed inset-0 bg-black/40 flex items-center justify-center z-10"
          onClick={closeModal}
        >
          <div
            className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-lg font-semibold text-slate-800 mb-4">
              {editingCourse ? "Edit course" : "Create course"}
            </h2>
            <form onSubmit={handleSubmit}>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Course code
              </label>
              <input
                name="code"
                defaultValue={editingCourse?.code}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded mb-3"
              />
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Course title
              </label>
              <input
                name="title"
                defaultValue={editingCourse?.title}
                required
                className="w-full px-3 py-2 border border-slate-300 rounded mb-3"
              />
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Category
              </label>
              <select
                name="category"
                defaultValue={editingCourse?.category ?? "Core"}
                className="w-full px-3 py-2 border border-slate-300 rounded mb-4"
              >
                <option value="Core">Core</option>
                <option value="Elective">Elective</option>
              </select>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={closeModal}
                  className="px-4 py-2 rounded bg-slate-200 text-slate-700 hover:bg-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded bg-slate-700 text-white hover:bg-slate-800"
                >
                  {editingCourse ? "Save" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
```

**4. `src/components/CourseManager.jsx`** (state, filter, and layout):

```jsx
import { useState, useMemo } from "react";
import CourseSearch from "./CourseSearch";
import CourseListing from "./CourseListing";

const INITIAL_COURSES = [
  {
    id: 1,
    code: "COMP 6501",
    title: "Research Methods, Entrepreneurship and Intellectual Property",
    category: "Core",
  },
  {
    id: 2,
    code: "COMP 6925",
    title: "Applied Operations Research",
    category: "Core",
  },
  {
    id: 3,
    code: "STAT 6105",
    title: "Probability and Statistical Methods for Data Analytics",
    category: "Core",
  },
  {
    id: 4,
    code: "STAT 6106",
    title: "Statistical Inference for Data Analytics",
    category: "Core",
  },
  {
    id: 5,
    code: "COMP 6930",
    title: "Machine Learning and Data Mining",
    category: "Core",
  },
  {
    id: 6,
    code: "COMP 6940",
    title: "Big Data and Visual Analytics",
    category: "Core",
  },
  { id: 7, code: "STAT 6005", title: "Research Project", category: "Core" },
  {
    id: 8,
    code: "COMP 6300",
    title: "Advanced Internet Technologies",
    category: "Elective",
  },
  {
    id: 9,
    code: "COMP 6401",
    title: "Advanced Algorithms",
    category: "Elective",
  },
  {
    id: 10,
    code: "COMP 6802",
    title: "Distributed and Parallel Database Systems",
    category: "Elective",
  },
  {
    id: 11,
    code: "COMP 6905",
    title: "Cloud Technologies",
    category: "Elective",
  },
  { id: 12, code: "STAT 6160", title: "Data Analysis", category: "Elective" },
  {
    id: 13,
    code: "STAT 6170",
    title: "Multivariate Analysis",
    category: "Elective",
  },
  {
    id: 14,
    code: "STAT 6181",
    title: "Computational Statistics I",
    category: "Elective",
  },
  {
    id: 15,
    code: "STAT 6182",
    title: "Computational Statistics II",
    category: "Elective",
  },
];

export default function CourseManager() {
  const [courses, setCourses] = useState(INITIAL_COURSES);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredCourses = useMemo(() => {
    if (!searchTerm.trim()) return courses;
    const term = searchTerm.toLowerCase().trim();
    return courses.filter(
      (c) =>
        c.code.toLowerCase().includes(term) ||
        c.title.toLowerCase().includes(term),
    );
  }, [courses, searchTerm]);

  function handleCreate(course) {
    setCourses((prev) => [
      ...prev,
      { ...course, id: Math.max(0, ...prev.map((c) => c.id)) + 1 },
    ]);
  }

  function handleUpdate(id, updates) {
    setCourses((prev) =>
      prev.map((c) => (c.id === id ? { ...c, ...updates } : c)),
    );
  }

  function handleDelete(id) {
    setCourses((prev) => prev.filter((c) => c.id !== id));
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold text-slate-800 mb-6">
        Course list
      </h1>
      <CourseSearch value={searchTerm} onChange={setSearchTerm} />
      <CourseListing
        courses={filteredCourses}
        onCreate={handleCreate}
        onUpdate={handleUpdate}
        onDelete={handleDelete}
      />
    </div>
  );
}
```

**5. `src/App.jsx`** (minimal entry):

```jsx
import "./App.css";
import CourseManager from "./components/CourseManager";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <CourseManager />
    </div>
  );
}

export default App;
```

**6. `src/App.css`** — keep minimal or empty; e.g.:

```css
/* Add any app-specific overrides here if needed */
```

---

### 7.7 Wiring summary

- **App.jsx** only renders `CourseManager` inside a light background (`bg-slate-50`).
- **CourseManager** holds courses state (initialized with the hardcoded list), search term, filtered list, and create/update/delete handlers. It renders **CourseSearch** and **CourseListing**.
- **CourseSearch** is a single input; its value and `onChange` are controlled by `CourseManager`.
- **CourseListing** receives `courses` (filtered), `onCreate`, `onUpdate`, `onDelete`. It shows a “Create course” tile plus a grid of **Course** cards (left to right). Create and Edit open a small modal with code, title, and category; Submit calls `onCreate` or `onUpdate` and closes the modal. Delete calls `onDelete(id)`.

When done, you should be able to view all courses, search by code or title, and add, edit, and delete courses (changes only in memory, no persistence).

---

### 7.8 Activity: Extra code matching slides.md

The teaching slides in **`slides.md`** (at the repo root) reference extra code that illustrates routing, the `children` prop, and arrow-function components. **Complete the following steps yourself** so your app matches the slides. The starter codebase does not include this code — you will add routing (Home + About), the `Card` and `CategoryBadge` components, and update `Course` to use them.

**A. Routing (Home + About)**

1. **Install the router** (from `my-app/`):

   ```bash
   npm install react-router-dom
   ```

2. **Wrap the app with `BrowserRouter`** — In `src/main.jsx`, add the import and wrap `<App />`:

   ```jsx
   import { StrictMode } from "react";
   import { createRoot } from "react-dom/client";
   import { BrowserRouter } from "react-router-dom";
   import "./index.css";
   import App from "./App.jsx";

   createRoot(document.getElementById("root")).render(
     <StrictMode>
       <BrowserRouter>
         <App />
       </BrowserRouter>
     </StrictMode>,
   );
   ```

3. **Create the About page** — Create `src/pages/About.jsx`:

   ```jsx
   export default function About() {
     return (
       <div className="max-w-2xl mx-auto p-6">
         <h1 className="text-2xl font-semibold text-slate-800 mb-4">About</h1>
         <p className="text-slate-600 mb-4">
           This app is a <strong>Course Manager</strong> for viewing and
           managing a list of courses. You can search by course code or title,
           create new courses, edit existing ones, and delete courses. The
           course list is shown on the Home page; this About page describes what
           the app does.
         </p>
         <p className="text-slate-600">
           It is built with React and used as a teaching example for components,
           state, props, events, and routing.
         </p>
       </div>
     );
   }
   ```

4. **Update `src/App.jsx`** to add a nav bar and routes:

   ```jsx
   import "./App.css";
   import { Routes, Route, Link } from "react-router-dom";
   import CourseManager from "./components/CourseManager";
   import About from "./pages/About";

   function App() {
     return (
       <div className="min-h-screen bg-slate-50">
         <nav className="border-b border-slate-200 bg-white px-6 py-3 flex gap-4">
           <Link
             to="/"
             className="text-slate-700 hover:text-slate-900 font-medium"
           >
             Home
           </Link>
           <Link
             to="/about"
             className="text-slate-700 hover:text-slate-900 font-medium"
           >
             About
           </Link>
         </nav>
         <Routes>
           <Route path="/" element={<CourseManager />} />
           <Route path="/about" element={<About />} />
         </Routes>
       </div>
     );
   }

   export default App;
   ```

   Home (`/`) shows the course list; About (`/about`) shows the description.

**B. CategoryBadge and Card (for slides examples)**

5. **Create `src/components/CategoryBadge.jsx`** (arrow-function component example):

   ```jsx
   /** Arrow-function component example: receives props and returns JSX. */
   const CategoryBadge = ({ label }) => (
     <span className="inline-block mt-2 text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600">
       {label}
     </span>
   );

   export default CategoryBadge;
   ```

6. **Create `src/components/Card.jsx`** (illustrates the `children` prop):
   ```jsx
   /**
    * Card illustrates the special `children` prop:
    * content between opening and closing tags is passed as children.
    */
   export default function Card({ title, children }) {
     return (
       <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow">
         <h2 className="font-medium text-slate-800 text-base mb-1">{title}</h2>
         {children}
       </div>
     );
   }
   ```

**C. Use Card and CategoryBadge in Course**

7. **Update `src/components/Course.jsx`** to use `Card` and `CategoryBadge` (replacing the single outer `div` and inline category span):

   ```jsx
   import Card from "./Card";
   import CategoryBadge from "./CategoryBadge";

   export default function Course({ course, onEdit, onDelete }) {
     return (
       <Card title={course.code}>
         <div className="text-sm text-slate-600 mt-1">{course.title}</div>
         {course.category && <CategoryBadge label={course.category} />}
         <div className="mt-3 flex gap-2">
           <button
             type="button"
             onClick={() => onEdit(course)}
             className="text-sm px-3 py-1.5 rounded bg-slate-200 text-slate-700 hover:bg-slate-300"
           >
             Edit
           </button>
           <button
             type="button"
             onClick={() => onDelete(course.id)}
             className="text-sm px-3 py-1.5 rounded bg-red-100 text-red-700 hover:bg-red-200"
           >
             Delete
           </button>
         </div>
       </Card>
     );
   }
   ```

After these steps, the app has routing (Home / About), and the course card uses `Card` (children) and `CategoryBadge` (arrow-function component), matching the examples in `slides.md`.

---
