# React: From Foundations to Mid-Level — Teaching Slides

**Audience:** Masters students  
**Duration:** ~3 hours  
**Codebase:** This repo (`my-app`) — Course Manager app

Use this document as the source for slide content. Code examples are taken from or aligned with the Course Manager app in `my-app/`.

---

## Table of Contents

1. [React at a Glance](#1-react-at-a-glance)
2. [Components](#2-components)
3. [Props](#3-props)
4. [Destructuring](#4-destructuring)
5. [useState — Local State](#5-usestate--local-state)
6. [Event Handling](#6-event-handling)
7. [Component Lifecycle & useEffect](#7-component-lifecycle--useeffect)
8. [Spread Operator in React](#8-spread-operator-in-react)
9. [Lifting State & Composition](#9-lifting-state--composition)
10. [useMemo — Derived State](#10-usememo--derived-state)
11. [Calling APIs with fetch](#11-calling-apis-with-fetch)
12. [App Context and Global State](#12-app-context-and-global-state)
13. [Routing](#13-routing)
14. [Patterns & Best Practices](#14-patterns--best-practices)

---

## 1. React at a Glance

### What is React?

- **Library** for building user interfaces (not a full framework).
- **Declarative:** The UI is described in terms of *what* it should look like for a given state; React updates the DOM.
- **Component-based:** UIs are built from reusable, composable components.
- **Single source of truth:** State lives in one place; the UI is a function of state.

### Entry point (this codebase)

```jsx
// main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

- **`createRoot` + `render`** — The React 18+ way to mount the app. The DOM node (here `document.getElementById("root")`) is passed to `createRoot`, which returns a *root* object. Calling `root.render(<App />)` tells React to take over that DOM node and render the component tree inside it. React then manages updates: when state or props change, it re-renders only what’s needed and updates the real DOM (this is the “virtual DOM” idea). In React 17 and earlier, the API was `ReactDOM.render(<App />, document.getElementById("root"))`; the new API enables React 18 features like concurrent rendering and is the one to use going forward.
- **`StrictMode`** — A development-only wrapper that helps write safer code. It doesn’t render any extra UI.
  - In development, React intentionally *double-invokes* certain functions (e.g. component bodies and some lifecycle logic) so that side effects and impure code become visible.
  - **Why double-invoke?** If a component body does side effects during render (e.g. mutates a global variable — changing something outside the component, like `window.someCounter = (window.someCounter || 0) + 1`; or writes to `localStorage`; or triggers a network request), running it twice makes the bug obvious: duplicate requests, wrong counts, or inconsistent state.
  - **Where to put mutations and side effects:** React’s model is that the component function should be *pure* for a given props/state (same in, same out). Any mutation or side effect — e.g. updating a global, writing to storage, or fetching data — should live in **`useEffect`** (or similar), not in the render path. That way React controls when they run (after commit, with cleanup), and StrictMode’s double-invoke won’t run them twice in the same way.
  - Double-invoking doesn’t change behaviour in production; it only helps find code that breaks the pure-render assumption.
  - StrictMode also warns about deprecated APIs (e.g. legacy string refs, old lifecycle methods) and highlights potential problems with concurrent rendering.
  - In production builds, StrictMode has no effect, so it’s safe to leave it in the tree.

### Component tree in this app

```
App
└── CourseManager (state: courses, searchTerm)
    ├── CourseSearch (controlled input)
    └── CourseListing (modal, list)
        └── Course (per card) × N
```

---

## 2. Components

### What is a component?

- A **function** (or class) that returns **JSX**. In practice a function is written that describes the UI for a given set of inputs (props and state). React calls that function whenever it needs to render or re-render that part of the tree. The return value is JSX — a syntax that looks like HTML but compiles to `React.createElement` calls, i.e. plain JavaScript objects describing elements and components. So a component is really “a recipe for a piece of UI”: same inputs should give the same output (ideally pure), and React handles when to run the recipe and how to apply the result to the DOM. Classes are the older style; function components (with hooks) are the standard today.
- Name must start with a capital letter so React treats it as a component, not an HTML tag. For example, `<Course />` is treated as the `Course` component; `<course />` would be treated as a lowercase HTML element (invalid in HTML5 and not the intended component). Same for `<CourseListing />` vs `<courselisting />`.

### Function components (used everywhere in this app)

**Example from the codebase — `Course.jsx`:**

```jsx
export default function Course({ course, onEdit, onDelete }) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg ...">
      <div className="font-medium text-slate-800">{course.code}</div>
      <div className="text-sm text-slate-600 mt-1">{course.title}</div>
      {/* ... */}
    </div>
  );
}
```

- **One component, one responsibility:** `Course` only renders one course card.
- **Reusable:** Rendered in a `.map()` in `CourseListing` for each course. Example from the codebase:

  ```jsx
  {courses.map((course) => (
    <div key={course.id} className="w-[280px]">
      <Course course={course} onEdit={openEdit} onDelete={onDelete} />
    </div>
  ))}
  ```

  Each item gets a unique `key` (here `course.id`) so React can track list items correctly across re-renders.

### Another example — `CourseSearch.jsx`

```jsx
export default function CourseSearch({ value, onChange }) {
  return (
    <div className="mb-6">
      <input
        type="text"
        placeholder="Search by course code or title..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="..."
      />
    </div>
  );
}
```

- Presentational: receives `value` and `onChange` from the parent; doesn’t own state.

### Key ideas

- **Composition:** Small components are composed into larger ones (`Course` inside `CourseListing` inside `CourseManager`).
- **Default export:** `export default function Course` — imported as `import Course from "./Course"`.

---

## 3. Props

### What are props?

- **Props** = inputs passed from parent to child. They are **read-only**.
- Flow is **one-way:** parent → child. Children never mutate props.

### Passing props (parent → child)

**In `CourseListing.jsx`:**

```jsx
<Course course={course} onEdit={openEdit} onDelete={onDelete} />
```

- `course`: data (object).
- `onEdit`, `onDelete`: functions (callbacks). The child calls them to communicate back.

### Receiving props (child)

**In `Course.jsx`:**

```jsx
export default function Course({ course, onEdit, onDelete }) {
  return (
    // ...
    <button onClick={() => onEdit(course)}>Edit</button>
    <button onClick={() => onDelete(course.id)}>Delete</button>
  );
}
```

- The child doesn’t know *where* the data lives or *how* edit/delete work — it just calls the callbacks.

### Props can be anything

| Type       | Example in this app                          |
|-----------|----------------------------------------------|
| Primitive | `value={searchTerm}`, `onChange={setSearchTerm}` |
| Object    | `course={course}`                            |
| Function  | `onEdit={openEdit}`, `onDelete={onDelete}`   |
| Array     | `courses={filteredCourses}`                   |

### Children (special prop)

```jsx
function Card({ title, children }) {
  return (
    <div>
      <h2>{title}</h2>
      {children}
    </div>
  );
}

<Card title="Course">Content here</Card>
```

- `children` is the content between opening and closing tags.

---

## 4. Destructuring

### Why destructure?

- Cleaner code and explicit “API” of the component.
- Used for **props** and **state** throughout this app.

### Destructuring props

**Without destructuring:**

```jsx
function Course(props) {
  return <div>{props.course.code} — {props.course.title}</div>;
}
```

**With destructuring (as in `Course.jsx`):**

```jsx
function Course({ course, onEdit, onDelete }) {
  return (
    <div>
      <div>{course.code}</div>
      <div>{course.title}</div>
      <button onClick={() => onEdit(course)}>Edit</button>
      <button onClick={() => onDelete(course.id)}>Delete</button>
    </div>
  );
}
```

### Destructuring with defaults

**In `CourseListing.jsx` (form handling):**

```jsx
const category = form.category?.value?.trim() || "Core";
```

**Typical pattern for optional props:**

```jsx
function Badge({ label, variant = "default" }) {
  return <span className={variant}>{label}</span>;
}
```

### Nested destructuring (when useful)

```jsx
const { course: { code, title, category } } = props;
// or in parameter list:
function CourseCard({ course: { code, title, category } }) { ... }
```

---

## 5. useState — Local State

### What is state?

- **State** = data that can change over time. When state updates, React re-renders the component.
- **useState** is the main hook for local (component-level) state.

### Signature

```js
const [value, setValue] = useState(initialValue);
```

- `value`: current state.
- `setValue`: function to update it. **Always use the setter;** don’t mutate state directly.

### Example — `CourseManager.jsx`

```jsx
const [courses, setCourses] = useState(INITIAL_COURSES);
const [searchTerm, setSearchTerm] = useState("");
```

- `courses`: list of courses (array).
- `searchTerm`: controlled input value (string).

### Example — `CourseListing.jsx`

```jsx
const [modalOpen, setModalOpen] = useState(false);
const [editingCourse, setEditingCourse] = useState(null);
```

- Boolean for modal visibility, object or `null` for “which course we’re editing.”

### Updating state correctly

**Wrong (mutation):**

```js
courses.push(newCourse);  // ❌ Don’t mutate
setCourses(courses);      // React may not re-render
```

**Right (new reference):**

```jsx
// CourseManager.jsx — add new course
function handleCreate(course) {
  setCourses((prev) => [
    ...prev,
    { ...course, id: Math.max(0, ...prev.map((c) => c.id)) + 1 },
  ]);
}
```

- **Functional updates:** `setCourses((prev) => ...)` when the new state depends on the previous state (avoids stale closures).

### Functional updates

Use when the next state depends on the previous:

```jsx
// Increment
setCount((prev) => prev + 1);

// Toggle
setModalOpen((prev) => !prev);

// Update one item in list (CourseManager.jsx)
function handleUpdate(id, updates) {
  setCourses((prev) =>
    prev.map((c) => (c.id === id ? { ...c, ...updates } : c))
  );
}
```

---

## 6. Event Handling

### Syntax and conventions

- **In JSX:** use `onEventName` (camelCase), e.g. `onClick`, `onChange`, `onSubmit`.
- **Handler:** a function reference or an inline function is passed. The function should not be invoked in place: use `onClick={doSomething}` not `onClick={doSomething()}` (unless the intent is to run it immediately).

### onClick

**From `Course.jsx`:**

```jsx
<button onClick={() => onEdit(course)}>Edit</button>
<button onClick={() => onDelete(course.id)}>Delete</button>
```

- Inline arrow function so we can pass arguments (`course`, `course.id`).

**From `CourseListing.jsx`:**

```jsx
<button type="button" onClick={openCreate}>+ Create course</button>
<div onClick={closeModal}>  {/* backdrop */}
  <div onClick={(e) => e.stopPropagation()}>  {/* modal content */}
```

- `e.stopPropagation()`: prevents the backdrop click from firing when clicking inside the modal.

### onChange (controlled inputs)

**From `CourseSearch.jsx`:**

```jsx
<input
  value={value}
  onChange={(e) => onChange(e.target.value)}
/>
```

- **Controlled component:** `value` comes from state; every keystroke updates state via `onChange`. Single source of truth.

### onSubmit (forms)

**From `CourseListing.jsx`:**

```jsx
function handleSubmit(e) {
  e.preventDefault();  // Don’t do full page submit
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

<form onSubmit={handleSubmit}>
```

- **e.preventDefault():** essential for single-page behaviour.
- Read values from `e.target` (the form) or individual fields.

### Event object

- **e.target:** DOM element that received the event (e.g. input, button).
- **e.preventDefault():** prevent default browser action (e.g. form submit, link navigation).
- **e.stopPropagation():** stop event bubbling (e.g. modal content click).

---

## 7. Component Lifecycle & useEffect

### From “lifecycle” to “render + effects”

- Class components had lifecycle methods (`componentDidMount`, `componentDidUpdate`, etc.).
- With function components we think in terms of:
  - **Render:** function runs, returns JSX.
  - **Effects:** side effects (fetch, subscriptions, DOM) via **useEffect**.

### useEffect signature

```js
useEffect(() => {
  // effect code
  return () => { /* optional cleanup */ };
}, [dep1, dep2]);  // dependency array
```

- **Runs after** the component has committed to the DOM (after paint).
- **Dependencies:** when the list changes, the effect runs again. Omit = run after every render. `[]` = run once (mount only).

### Run once on mount (e.g. fetch initial data)

```jsx
useEffect(() => {
  fetch("/api/courses")
    .then((res) => res.json())
    .then((data) => setCourses(data));
}, []);  // empty = only on mount
```

### Run when a value changes

```jsx
useEffect(() => {
  document.title = `${count} courses`;
}, [count]);
```

### Cleanup (e.g. subscriptions, timers)

```jsx
useEffect(() => {
  const id = setInterval(() => setCount((c) => c + 1), 1000);
  return () => clearInterval(id);  // cleanup on unmount or when deps change
}, []);
```

### This codebase

- The app currently uses **initial state** (`INITIAL_COURSES`) and no `useEffect`. A `useEffect` with `[]` can be added to load courses from an API on mount (see “Calling APIs with fetch” below).

---

## 8. Spread Operator in React

### Spreading objects (updating state immutably)

**From `CourseManager.jsx`:**

```jsx
// Add new course (spread existing array, add new object)
setCourses((prev) => [
  ...prev,
  { ...course, id: Math.max(0, ...prev.map((c) => c.id)) + 1 },
]);

// Update one course (new array, spread old course + updates)
setCourses((prev) =>
  prev.map((c) => (c.id === id ? { ...c, ...updates } : c))
);

// Delete (filter gives new array; no spread needed)
setCourses((prev) => prev.filter((c) => c.id !== id));
```

- **`...prev`:** new array with all previous items.
- **`{ ...course, id: newId }`:** new object, overriding `id`.
- **`{ ...c, ...updates }`:** merge updates into a copy of the course.

### Spreading props (pass-through)

```jsx
<input {...inputProps} className="extra-class" />
// Merges inputProps into the input; className can override.
```

### Why not mutate?

- React uses reference equality to decide when to re-render. New array/object references trigger updates; mutating in place does not.

---

## 9. Lifting State & Composition

### Lifting state up

- When **several components need the same state**, put that state in their **common ancestor** and pass it down (and pass setters/callbacks).

**In this app:**

- `CourseManager` owns `courses` and `searchTerm`.
- `CourseSearch` gets `value={searchTerm}` and `onChange={setSearchTerm}` (controlled).
- `CourseListing` gets `courses`, `onCreate`, `onUpdate`, `onDelete`.
- `Course` gets one `course` and callbacks. It doesn’t own any list state.

### Data flow diagram

```
CourseManager [courses, setCourses, searchTerm, setSearchTerm]
    │
    ├─► CourseSearch: value, onChange  (controlled input)
    │
    └─► CourseListing: courses, onCreate, onUpdate, onDelete
            │
            └─► Course: course, onEdit, onDelete  (per item)
```

### Composition vs prop drilling

- **Composition:** pass components as props or `children` to avoid passing many props through intermediate components.
- If the same props are passed through many layers, **Context** can be used instead (see below).

---

## 10. useMemo — Derived State

### When to use

- **Expensive computation** that depends on some state/props.
- **Stable reference** for objects/arrays passed to children that rely on referential equality (e.g. `React.memo` or effect deps).

### Example — `CourseManager.jsx`

```jsx
const filteredCourses = useMemo(() => {
  if (!searchTerm.trim()) return courses;
  const term = searchTerm.toLowerCase().trim();
  return courses.filter(
    (c) =>
      c.code.toLowerCase().includes(term) ||
      c.title.toLowerCase().includes(term),
  );
}, [courses, searchTerm]);
```

- Filtering runs only when `courses` or `searchTerm` change.
- Without `useMemo`, a new array would be created every render (fine here, but useMemo becomes important for heavier work or when passing to memoized children).

### Rule of thumb

- Don’t use `useMemo` for every small computation. Use it when:
  - The computation is costly, or
  - A stable reference is needed for dependencies or memoized children.

---

## 11. Calling APIs with fetch

### Basic pattern

- Request data in **useEffect** (e.g. on mount).
- Store result in state; show loading/error in the UI.

### Load courses on mount (one way to extend this app)

```jsx
// In CourseManager or a custom hook
const [courses, setCourses] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  setLoading(true);
  setError(null);
  fetch("/api/courses")
    .then((res) => {
      if (!res.ok) throw new Error("Failed to load courses");
      return res.json();
    })
    .then((data) => setCourses(Array.isArray(data) ? data : []))
    .catch((err) => setError(err.message))
    .finally(() => setLoading(false));
}, []);
```

### Using async/await

```jsx
useEffect(() => {
  let cancelled = false;
  async function load() {
    setLoading(true);
    try {
      const res = await fetch("/api/courses");
      if (!res.ok) throw new Error("Failed to load");
      const data = await res.json();
      if (!cancelled) setCourses(Array.isArray(data) ? data : []);
    } catch (err) {
      if (!cancelled) setError(err.message);
    } finally {
      if (!cancelled) setLoading(false);
    }
  }
  load();
  return () => { cancelled = true; };  // avoid setState after unmount
}, []);
```

### POST/PUT/DELETE (create, update, delete)

```jsx
async function createCourse(course) {
  const res = await fetch("/api/courses", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(course),
  });
  if (!res.ok) throw new Error("Create failed");
  const created = await res.json();
  setCourses((prev) => [...prev, created]);
}
```

### Teaching points

- Always handle **loading** and **error** state.
- Use **cleanup** (e.g. a `cancelled` flag) so that `setState` is not called after unmount.
- Check `res.ok` and parse `res.json()` once.

---

## 12. App Context and Global State

### When to use Context

- Same data or functions needed by **many components** at different levels (theme, auth, “current user”, API client).
- Avoids **prop drilling** (passing props through many layers).

### Creating context

```jsx
// contexts/CourseContext.jsx
import { createContext, useContext, useState } from "react";

const CourseContext = createContext(null);

export function CourseProvider({ children }) {
  const [courses, setCourses] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const value = {
    courses,
    setCourses,
    searchTerm,
    setSearchTerm,
    createCourse: (course) => setCourses((prev) => [...prev, { ...course, id: Date.now() }]),
    updateCourse: (id, updates) =>
      setCourses((prev) => prev.map((c) => (c.id === id ? { ...c, ...updates } : c))),
    deleteCourse: (id) => setCourses((prev) => prev.filter((c) => c.id !== id)),
  };

  return (
    <CourseContext.Provider value={value}>
      {children}
    </CourseContext.Provider>
  );
}

export function useCourses() {
  const ctx = useContext(CourseContext);
  if (!ctx) throw new Error("useCourses must be used within CourseProvider");
  return ctx;
}
```

### Providing context (e.g. in `App.jsx`)

```jsx
import { CourseProvider } from "./contexts/CourseContext";

function App() {
  return (
    <CourseProvider>
      <div className="min-h-screen bg-slate-50">
        <CourseManager />
      </div>
    </CourseProvider>
  );
}
```

### Consuming context in any child

```jsx
// Inside CourseListing or any deep child
import { useCourses } from "../contexts/CourseContext";

function CourseListing() {
  const { courses, createCourse, updateCourse, deleteCourse, searchTerm, setSearchTerm } = useCourses();
  // no need to receive these as props
}
```

### Best practices

- **Split contexts** by concern (e.g. AuthContext, CourseContext) so only consumers that need a value re-render when it changes.
- **Stable value:** memoize the context value with `useMemo` if it’s an object/array to avoid unnecessary re-renders.
- For complex app-wide state, consider **state management** (e.g. Redux, Zustand) later; Context is fine for theme, auth, and moderate state.

---

## 13. Routing

### Why routing?

- Multiple “pages” or views (e.g. list vs detail) with a URL.
- **react-router-dom** is the standard library.

### Setup (conceptual — add to this app when adding routes)

```bash
npm install react-router-dom
```

```jsx
// main.jsx
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
);
```

### Defining routes (e.g. in `App.jsx`)

```jsx
import { Routes, Route } from "react-router-dom";
import CourseManager from "./components/CourseManager";
import CourseDetail from "./components/CourseDetail";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Routes>
        <Route path="/" element={<CourseManager />} />
        <Route path="/courses/:id" element={<CourseDetail />} />
      </Routes>
    </div>
  );
}
```

### Navigation

```jsx
import { Link, useNavigate } from "react-router-dom";

// Declarative link
<Link to="/">Home</Link>
<Link to={`/courses/${course.id}`}>View {course.code}</Link>

// Programmatic
const navigate = useNavigate();
navigate("/");
navigate(`/courses/${id}`);
```

### Reading URL params

```jsx
import { useParams } from "react-router-dom";

function CourseDetail() {
  const { id } = useParams();
  // fetch or find course by id
}
```

### Teaching points

- **Route** = URL path + component.
- **Link** for navigation without full page reload.
- **useParams** for dynamic segments; **useSearchParams** for query strings.

---

## 14. Patterns & Best Practices

### Key files in this codebase

| File             | Concepts demonstrated                          |
|------------------|--------------------------------------------------|
| `App.jsx`        | Root component, composition                     |
| `main.jsx`       | Entry, StrictMode, createRoot                    |
| `CourseManager.jsx` | useState, useMemo, lifting state, handlers   |
| `CourseListing.jsx` | useState, events (onSubmit, onClick), props  |
| `Course.jsx`     | Props, destructuring, callbacks                 |
| `CourseSearch.jsx` | Controlled input, props                        |

### Checklist for mid-level React

- [ ] Build function components and compose them.
- [ ] Use props (including callbacks) and destructuring.
- [ ] Manage local state with useState and update immutably (spread).
- [ ] Handle events: onClick, onChange, onSubmit, preventDefault, stopPropagation.
- [ ] Use useEffect for side effects and cleanup when needed.
- [ ] Derive state (filter, sort) and use useMemo when it matters.
- [ ] Lift state to the right parent and avoid prop drilling (or use Context).
- [ ] Fetch data with fetch (or similar), handle loading/error, and cleanup.
- [ ] Use Context for shared app-level state where appropriate.
- [ ] Add routing (react-router-dom) for multiple views/URLs.
- [ ] Keep components focused, name clearly, and prefer small, testable pieces.

### Optional next steps (beyond 3 hours)

- **Custom hooks** (e.g. `useCourses`, `useFetch`) to reuse state and effect logic.
- **Error boundaries** for graceful error handling in the tree.
- **React.memo** and **useCallback** when measurement shows that re-renders need to be limited.
- **Testing** with React Testing Library and Jest.
- **TypeScript** for props and state types.

---

## Quick reference: hooks used in this app

| Hook       | Purpose in this app                          |
|-----------|-----------------------------------------------|
| useState  | courses, searchTerm, modalOpen, editingCourse |
| useMemo   | filteredCourses from courses + searchTerm     |
| (useEffect) | (Could load courses from API on mount)     |
| (useContext) | (Could provide courses/actions globally)   |

---

*Slides content derived from the Course Manager app in `my-app/`. Use the repo as the live coding and demo source while presenting.*
