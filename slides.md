# React: From Foundations to Mid-Level

**Codebase:** This repo (`my-app`) — Course Manager app

Code examples are taken from or aligned with the Course Manager app in `my-app/`.

**JS Side Notes:** Throughout the slides, **JS Side Note** callouts appear where JavaScript (especially ES6+) concepts are used. They cover topics such as: arrow functions, destructuring, spread/rest operators, closures, promises & async/await, the event loop, and array methods (`map`, `filter`, `reduce`).

---

## Table of Contents

1. [React at a Glance](#1-react-at-a-glance)
2. [Components](#2-components)
3. [Props](#3-props)
4. [Destructuring](#4-destructuring)
5. [useState — Local State](#5-usestate--local-state)
6. [Event Handling](#6-event-handling)
7. [useEffect — Side Effects After Render](#7-useeffect--side-effects-after-render)
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
- **Declarative:** The UI is described in terms of _what_ it should look like for a given state; React updates the DOM.
- **Component-based:** UIs are built from reusable, composable components.
- **Single source of truth:** State lives in one place; the UI is a function of state.

### Entry point (this codebase)

```jsx
// main.jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

- **`createRoot` + `render`** — The React 18+ way to mount the app. The DOM node (here `document.getElementById("root")`) is passed to `createRoot`, which returns a _root_ object. Calling `root.render(<App />)` tells React to take over that DOM node and render the component tree inside it. React then manages updates: when state or props change, it re-renders only what’s needed and updates the real DOM (this is the “virtual DOM” idea). In React 17 and earlier, the API was `ReactDOM.render(<App />, document.getElementById("root"))`; the new API enables React 18 features like concurrent rendering and is the one to use going forward.
- **`StrictMode`** — A development-only wrapper that helps write safer code. It doesn’t render any extra UI.
  - In development, React intentionally _double-invokes_ certain functions (e.g. component bodies and some effect-related logic) so that side effects and impure code become visible.
  - **Why double-invoke?** If a component body does side effects during render (e.g. mutates a global variable — changing something outside the component, like `window.someCounter = (window.someCounter || 0) + 1`; or writes to `localStorage`; or triggers a network request), running it twice makes the bug obvious: duplicate requests, wrong counts, or inconsistent state.
  - **Where to put mutations and side effects:** React’s model is that the component function should be _pure_ for a given props/state (same in, same out). Any mutation or side effect — e.g. updating a global, writing to storage, or fetching data — should live in **`useEffect`** (or similar), not in the render path. That way React controls when they run (after commit, with cleanup), and StrictMode’s double-invoke won’t run them twice in the same way.
  - Double-invoking doesn’t change behaviour in production; it only helps find code that breaks the pure-render assumption.
  - StrictMode also warns about deprecated APIs (e.g. legacy string refs and other deprecated patterns) and highlights potential problems with concurrent rendering.
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

- A **function** (or class) that returns **JSX**. In practice a function is written that describes the UI for a given set of inputs (props and state). React calls that function whenever it needs to render or re-render that part of the tree. The return value is JSX — a syntax that looks like HTML but compiles to `React.createElement` calls, i.e. plain JavaScript objects describing elements and components. So a component is really “a recipe for a piece of UI”: same inputs should give the same output (ideally pure), and React handles when to run the recipe and how to apply the result to the DOM.
- Name must start with a capital letter so React treats it as a component, not an HTML tag. For example, `<Course />` is treated as the `Course` component; `<course />` would be treated as a lowercase HTML element (invalid in HTML5 and not the intended component). Same for `<CourseListing />` vs `<courselisting />`.

### Function components

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
  {
    courses.map((course) => (
      <div key={course.id} className="w-[280px]">
        <Course course={course} onEdit={openEdit} onDelete={onDelete} />
      </div>
    ));
  }
  ```

  Each item gets a unique `key` (here `course.id`) so React can track list items correctly across re-renders.

  **JS Side Note: Arrow functions** — Arrow functions provide a shorter syntax for writing functions. The main benefits here are concise callbacks and easy passing of arguments. Sample examples from this codebase:
  - **Array rendering** — In `CourseListing.jsx`, each course is rendered via an arrow function passed to `.map()`: it receives `course` and returns the JSX for one list item.

    ```jsx
    {
      courses.map((course) => (
        <div key={course.id} className="w-[280px]">
          <Course course={course} onEdit={openEdit} onDelete={onDelete} />
        </div>
      ));
    }
    ```

  - **Event handlers (passing arguments)** — In `Course.jsx`, the handler must pass `course` or `course.id` into the parent callback. An arrow function wraps the call so the correct argument is passed when the button is clicked.

    ```jsx
    <button onClick={() => onEdit(course)}>Edit</button>
    <button onClick={() => onDelete(course.id)}>Delete</button>
    ```

  - **Event handlers (using the event)** — In `CourseSearch.jsx`, the handler reads from the event and forwards the value; in `CourseListing.jsx`, it stops the click from bubbling to the backdrop. **This means:** In the DOM, a click on a child element “bubbles” up to its parents, so a click on the modal content would also fire the backdrop’s `onClick` (which closes the modal). Calling `e.stopPropagation()` on the inner div stops the event from reaching the backdrop, so clicking inside the modal does not close it; only clicking the dark backdrop does.

    ```jsx
    // CourseSearch.jsx — pass input value up
    <input onChange={(e) => onChange(e.target.value)} />
    // CourseListing.jsx — keep modal open when clicking inside it
    <div onClick={(e) => e.stopPropagation()}>
    ```

  - **Functional component (arrow form)** — A component can be defined as an arrow function that takes props and returns JSX. In the codebase, `CategoryBadge.jsx` is an example (used by `Course.jsx` for the category label).

    ```jsx
    // CategoryBadge.jsx
    const CategoryBadge = ({ label }) => (
      <span className="inline-block mt-2 text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600">
        {label}
      </span>
    );
    export default CategoryBadge;
    ```

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

- **Composition:** Small components are composed into larger ones (`Course` inside `CourseListing` inside `CourseManager`). Example from the codebase:

  ```jsx
  // CourseManager.jsx — composes CourseSearch and CourseListing
  import CourseSearch from "./CourseSearch";
  import CourseListing from "./CourseListing";
  // ...
  return (
    <div>
      <CourseSearch value={searchTerm} onChange={setSearchTerm} />
      <CourseListing courses={filteredCourses} onCreate={...} onUpdate={...} onDelete={...} />
    </div>
  );
  ```

  ```jsx
  // CourseListing.jsx — composes Course for each item
  import Course from "./Course";
  // ...
  {
    courses.map((course) => (
      <div key={course.id}>
        <Course course={course} onEdit={openEdit} onDelete={onDelete} />
      </div>
    ));
  }
  ```

- **Default export:** Components use `export default` and are imported by name. Example from the codebase:

  ```jsx
  // Course.jsx
  export default function Course({ course, onEdit, onDelete }) { ... }
  ```

  ```jsx
  // CourseListing.jsx — imports Course
  import Course from "./Course";
  ```

---

## 3. Props

### What are props?

- **Props** are the inputs that a parent component passes down to a child. They are **read-only**: the child receives them but must not change them. Changing a prop from inside the child would break React’s idea of a single source of truth and make the UI harder to reason about.
- Data flow is **one-way**, from parent to child. The parent owns the data (or state) and passes a copy or a callback down; the child renders from those props and may notify the parent via callbacks. Children never mutate props — they only read them and, when needed, call functions passed as props (e.g. `onSave`) so the parent can update state.

### Passing props (parent → child)

**In `CourseListing.jsx`:**

```jsx
<Course course={course} onEdit={openEdit} onDelete={onDelete} />
```

- **`course`** — A data object. The parent gets it from the list it owns (e.g. from `courses.map`) and passes one item down so the child can display it.
- **`onEdit`, `onDelete`** — Functions (callbacks) defined on the parent. The parent passes references to its own functions (`openEdit`, `onDelete`) so that when the child calls them, the parent’s logic runs (e.g. open the edit modal, or remove the course from state). When the child sends information back to the parent by calling these functions, that is often called **child-to-parent communication** or **inverse data flow**: data still flows one way (parent → child via props), but the child can signal back or send values by invoking the callback props the parent provided.

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

- The child **reads** `course` to render the card (code, title, category). It **calls** `onEdit(course)` or `onDelete(course.id)` when the user clicks a button, passing back the relevant data (the whole course for edit, or just the id for delete). The child does not know where the data lives in the parent or how edit/delete are implemented — it only receives props and invokes the callbacks when the user acts. The parent is responsible for updating its own state or opening the modal when those callbacks run.

### Props can be anything

| Type      | Example in this app                              |
| --------- | ------------------------------------------------ |
| Primitive | `value={searchTerm}`, `onChange={setSearchTerm}` |
| Object    | `course={course}`                                |
| Function  | `onEdit={openEdit}`, `onDelete={onDelete}`       |
| Array     | `courses={filteredCourses}`                      |

### Children (special prop)

`children` is the content between opening and closing tags. The component receives it as a prop and renders it where `{children}` appears.

**Before (without `Card`):** All content lived in one component. The course code, title, category, and buttons were siblings inside a single `div`:

```jsx
// Course.jsx — everything in one place
return (
  <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-4 ...">
    <div className="font-medium text-slate-800">{course.code}</div>
    <div className="text-sm text-slate-600 mt-1">{course.title}</div>
    {course.category && <CategoryBadge label={course.category} />}
    <div className="mt-3 flex gap-2">
      <button onClick={() => onEdit(course)}>Edit</button>
      <button onClick={() => onDelete(course.id)}>Delete</button>
    </div>
  </div>
);
```

**After (with `Card` and `children`):** The outer wrapper and the “title” slot are moved into a reusable `Card`. The same inner content is passed as **children** — the JSX between `<Card>` and `</Card>`.

**`Card.jsx`** — accepts `title` and `children`; renders the wrapper, then the title, then `{children}`:

```jsx
export default function Card({ title, children }) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-4 ...">
      <h2 className="font-medium text-slate-800 text-base mb-1">{title}</h2>
      {children}
    </div>
  );
}
```

**`Course.jsx`** — uses `Card`; the content between the tags becomes the `children` prop:

```jsx
export default function Course({ course, onEdit, onDelete }) {
  return (
    <Card title={course.code}>
      <div className="text-sm text-slate-600 mt-1">{course.title}</div>
      {course.category && <CategoryBadge label={course.category} />}
      <div className="mt-3 flex gap-2">
        <button onClick={() => onEdit(course)}>Edit</button>
        <button onClick={() => onDelete(course.id)}>Delete</button>
      </div>
    </Card>
  );
}
```

**How it works:** React passes the content between `<Card>` and `</Card>` as the second argument to `Card`, which destructures it as `children`. So `title` is `course.code`, and `children` is the three elements (title div, category badge, button div). `Card` renders that content where it puts `{children}` — directly under the heading. The UI is the same; the structure is split into a reusable wrapper (`Card`) and slot for content (`children`).

---

## 4. Destructuring

### Why destructure?

- Cleaner code and an explicit surface for the component (what it accepts is clear from the parameter list).
- Used for **props** and **state** throughout this app.

### Destructuring props

**Without destructuring:**

```jsx
function Course(props) {
  return (
    <div>
      {props.course.code} — {props.course.title}
    </div>
  );
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

**Typical pattern for optional props:**

```jsx
function Badge({ label, variant = "default" }) {
  return <span className={variant}>{label}</span>;
}
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
courses.push(newCourse); // ❌ Don’t mutate
setCourses(courses); // React may not re-render
```

- **Why this is mutation:** `courses.push(newCourse)` changes the existing array in place — it adds an item to the same array object that React is already holding in state. The array reference does not change. Then `setCourses(courses)` passes that same reference back. React compares the previous and next state by reference; when the reference is the same, it may skip re-rendering. So the UI can stay stale. In general, **mutation** means modifying an existing object or array (e.g. `arr.push`, `obj.foo = x`) instead of creating a new one. React expects state to be updated by passing a new reference (new array or object) to the setter.

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

**JS Side Note: Spread operator** — Here `...prev` creates a **new** array containing all previous items; the new element is added to that new array, so the original `prev` is never mutated. Similarly, `{ ...course, id: ... }` creates a new object. React sees a new reference and re-renders. The same idea applies in `handleUpdate` below: `prev.map(...)` returns a new array, and `{ ...c, ...updates }` creates a new object for the updated item.

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
    prev.map((c) => (c.id === id ? { ...c, ...updates } : c)),
  );
}
```

- In `handleUpdate`, **why this is not mutation:** `prev.map(...)` returns a new array; for the matching item, `{ ...c, ...updates }` creates a new object instead of changing `c`. The original `prev` and each `c` are left unchanged.

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

- Using an inline arrow function here lets us pass arguments into the handler: we need to send the whole `course` to `onEdit` and only `course.id` to `onDelete`. If we wrote `onClick={onEdit}` the handler would run with the click event, not the course data. Wrapping it in `() => onEdit(course)` means “when clicked, call onEdit with this course.”

**From `CourseListing.jsx`:**

```jsx
<button type="button" onClick={openCreate}>+ Create course</button>
<div onClick={closeModal}>  {/* backdrop */}
  <div onClick={(e) => e.stopPropagation()}>  {/* modal content */}
```

- Calling `e.stopPropagation()` on the modal content stops the click from bubbling up to the backdrop. So when the user clicks inside the white modal, only that handler runs; the backdrop’s handler (which closes the modal) does not run. That way the modal stays open when you click inside it and only closes when you click the dark overlay.

### onChange (controlled inputs)

**From `CourseSearch.jsx`:**

```jsx
<input value={value} onChange={(e) => onChange(e.target.value)} />
```

- This is a **controlled** input: the value shown in the field comes from React state, and every keystroke updates that state through `onChange`. So the input never “owns” its own text — React does. That gives a single source of truth: the state drives what you see, and you can validate or transform the value in one place.

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

- **e.preventDefault()** stops the browser’s default form behaviour, which is to submit the form and reload the page. In a React app we want to handle submit in JavaScript and stay on the same page, so we call `preventDefault()` at the start of the handler.
- The handler receives the event `e`; the form element is `e.target`. You can read field values from `e.target` (e.g. `e.target.code`, `e.target.title`) or by giving inputs a `name` and then reading `form.name.value`, as in the code above.

### Event object

- **e.target:** DOM element that received the event (e.g. input, button).
- **e.preventDefault():** prevent default browser action (e.g. form submit, link navigation).
- **e.stopPropagation():** stop event bubbling (e.g. modal content click).

---

## 7. useEffect — Side Effects After Render

- The component function should be pure: given props and state, it returns JSX. Side effects (fetch, subscriptions, DOM updates, timers) should not run during render. They run **after** render via **useEffect**, so React can control when they run and clean them up.

### useEffect signature

```js
useEffect(() => {
  // effect code
  return () => {
    /* optional cleanup */
  };
}, [dep1, dep2]); // dependency array
```

- **Runs after** the component has committed to the DOM (after paint).
- **Dependencies:** when the list changes, the effect runs again. Omit = run after every render. `[]` = run once (mount only).

### Run once on mount (e.g. fetch initial data)

```jsx
useEffect(() => {
  fetch("/api/courses")
    .then((res) => res.json())
    .then((data) => setCourses(data));
}, []); // empty = only on mount
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
  return () => clearInterval(id); // cleanup on unmount or when deps change
}, []);
```

### This codebase

- The app currently uses **initial state** (`INITIAL_COURSES`) and no `useEffect`. A `useEffect` with `[]` can be added to load courses from an API on mount (see “Calling APIs with fetch” below).

---

## 8. Spread Operator in React

**JS Side Note: Spread/rest** — The `...` syntax is ES6+: _spread_ copies enumerable properties from an object or elements from an array into a new object/array (used below for immutable updates); _rest_ collects remaining arguments or properties (e.g. `const { a, ...rest } = obj`). In React, spread is common when updating state or passing props.

### Spreading objects (updating state immutably)

**From `CourseManager.jsx`:**

```jsx
// Add new course (spread existing array, add new object)
setCourses((prev) => [
  ...prev,
  { ...course, id: Math.max(0, ...prev.map((c) => c.id)) + 1 },
]);

// Update one course (new array, spread old course + updates)
setCourses((prev) => prev.map((c) => (c.id === id ? { ...c, ...updates } : c)));

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

### Prop drilling

**Prop drilling** is the common, informal term for passing a prop through several components so it reaches a deeply nested component. It becomes an anti-pattern when it is verbose and makes the code hard to maintain or read.

**Example (hypothetical):** Suppose the app needed to pass an `onReportError` callback from `App` down to `Course` so each card could report errors. Every component in between would have to accept and forward the prop even if it doesn’t use it:

```jsx
// App.jsx — owns the callback
<CourseManager onReportError={handleReportError} />

// CourseManager.jsx — doesn’t use it, just forwards
<CourseListing onReportError={onReportError} ... />

// CourseListing.jsx — doesn’t use it, just forwards
<Course course={course} onReportError={onReportError} onEdit={openEdit} onDelete={onDelete} />

// Course.jsx — finally uses it
<button onClick={() => onReportError(course.id)}>Report</button>
```

That chain is prop drilling. The app in this repo avoids it for course data by only passing props one or two levels; for data needed many levels deep, the **Context API** (see section 12) is used instead.

### Lifting state up

When multiple components need access to the same changing data (state), the recommended practice is to move (lift) the shared state to their **closest common ancestor**. That parent then passes the state down as props (and passes setters or callbacks so children can request updates).

**Example from this codebase:** `CourseSearch` and `CourseListing` both need `searchTerm` or the list of courses. The closest common ancestor is `CourseManager`, so state lives there and is passed down:

```jsx
// CourseManager.jsx — state lives here (closest common ancestor)
const [courses, setCourses] = useState(INITIAL_COURSES);
const [searchTerm, setSearchTerm] = useState("");

return (
  <div>
    <CourseSearch value={searchTerm} onChange={setSearchTerm} />
    <CourseListing
      courses={filteredCourses}
      onCreate={handleCreate}
      onUpdate={handleUpdate}
      onDelete={handleDelete}
    />
  </div>
);
```

- `CourseSearch` receives `value` and `onChange` so it can display and update the search term; it does not own state.
- `CourseListing` receives `courses` (the filtered list) and the handlers; `Course` receives one `course` and callbacks. None of them own the list; they only read and request changes via callbacks.

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

### Context API (preview)

To avoid excessive prop drilling, React provides the **Context API**. Context allows data to be provided at a top-level component and consumed by any descendant without passing it through every intermediate component — often described as “teleporting” data to deep parts of the tree. Section 12 shows how to add a `CourseContext` so components like `CourseListing` or `Course` can read course data via `useCourses()` instead of receiving it through props from `CourseManager`.

### Composition vs prop drilling

- **Composition:** pass components as props or `children` to avoid passing many props through intermediate components.
- When the same props would be passed through many layers, **Context** can be used instead (see section 12).

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
  return () => {
    cancelled = true;
  }; // avoid setState after unmount
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

### Note

- Always handle **loading** and **error** state.
- Use **cleanup** (e.g. a `cancelled` flag) so that `setState` is not called after unmount.
- Check `res.ok` and parse `res.json()` once.

---

## 12. App Context and Global State

### When to use Context

- Same data or functions needed by **many components** at different levels (theme, auth, “current user”, API client).
- **Context API** lets a top-level component provide data that any descendant can consume without passing it through every level. Data is effectively “teleported” to deep components, avoiding **prop drilling** (passing props through many layers), which becomes verbose and hard to maintain.

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
    createCourse: (course) =>
      setCourses((prev) => [...prev, { ...course, id: Date.now() }]),
    updateCourse: (id, updates) =>
      setCourses((prev) =>
        prev.map((c) => (c.id === id ? { ...c, ...updates } : c)),
      ),
    deleteCourse: (id) => setCourses((prev) => prev.filter((c) => c.id !== id)),
  };

  return (
    <CourseContext.Provider value={value}>{children}</CourseContext.Provider>
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
  const {
    courses,
    createCourse,
    updateCourse,
    deleteCourse,
    searchTerm,
    setSearchTerm,
  } = useCourses();
  // no need to receive these as props
}
```

### Best practices

- **Split contexts** by concern (e.g. AuthContext, CourseContext) so only consumers that need a value re-render when it changes.
- **Stable value:** memoize the context value with `useMemo` if it’s an object/array to avoid unnecessary re-renders.
---

## 13. Routing

### Why routing?

- Multiple “pages” or views (e.g. Home vs About) with a URL. The app can show different components for different paths without a full page reload.
- **Client-side rendering:** The server sends one initial HTML page and the JavaScript bundle. After that, React and the router run in the browser. When the user goes from Home to About (or the other way), the router only changes the URL and tells React which component to render. React updates the DOM in place — no new request to the server for another HTML page. So the "page change" is done entirely on the client: the same JS is already loaded, and it just swaps the visible component. That is client-side rendering for navigation: the browser does the rendering and the server is not asked for a new document on each route change.
- **react-router-dom** is the standard library.

### Setup in this codebase

The app uses two routes: **Home** (`/`) shows the course list (CourseManager); **About** (`/about`) shows a short description of the app. Navigation between them is done with `Link`.

**1. Install and wrap with `BrowserRouter` (`main.jsx`):**

```jsx
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

**2. Define routes and nav (`App.jsx`):**

```jsx
import { Routes, Route, Link } from "react-router-dom";
import CourseManager from "./components/CourseManager";
import About from "./pages/About";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="border-b border-slate-200 bg-white px-6 py-3 flex gap-4">
        <Link to="/" className="...">Home</Link>
        <Link to="/about" className="...">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<CourseManager />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </div>
  );
}
```

- **Home** (`/`): renders `CourseManager`, which contains the course list, search, and create/edit/delete.
- **About** (`/about`): renders `About`, a page that describes what the app does.

**3. About page (`pages/About.jsx`):**

A simple component that explains the app (course manager, search, create/edit/delete, and that it is a teaching example). No routing logic inside the page — it just renders content.

### Navigation

- **`Link`** — Declarative navigation: the user clicks a link, the URL changes, and the matching route’s component is rendered. No full page reload. In this app, the nav bar uses `<Link to="/">Home</Link>` and `<Link to="/about">About</Link>`.
- **`useNavigate()`** — For programmatic navigation (e.g. after a form submit): `const navigate = useNavigate();` then `navigate("/")` or `navigate("/about")`.

### Note

- **Route** = URL path + component. When the URL matches the path, the corresponding `element` is rendered.
- **Link** keeps navigation inside the React app (no full page reload).
- For dynamic segments (e.g. `/courses/:id`), use **useParams** in the route component to read `id`; for query strings, use **useSearchParams**. This app uses only static paths `/` and `/about`.

---

## 14. Patterns & Best Practices

### Key files in this codebase

| File                | Concepts demonstrated                       |
| ------------------- | ------------------------------------------- |
| `App.jsx`           | Root component, routing (Routes, Route, Link), nav |
| `main.jsx`          | Entry, StrictMode, createRoot, BrowserRouter |
| `pages/About.jsx`   | Route component, static content             |
| `CourseManager.jsx` | useState, useMemo, lifting state, handlers  |
| `CourseListing.jsx` | useState, events (onSubmit, onClick), props |
| `Course.jsx`        | Props, destructuring, callbacks             |
| `CourseSearch.jsx`  | Controlled input, props                     |

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

---

## Quick reference: hooks used in this app

| Hook         | Purpose in this app                           |
| ------------ | --------------------------------------------- |
| useState     | courses, searchTerm, modalOpen, editingCourse |
| useMemo      | filteredCourses from courses + searchTerm     |
| (useEffect)  | (Could load courses from API on mount)        |
| (useContext) | (Could provide courses/actions globally)      |

---

_Slides content derived from the Course Manager app in `my-app/`. ._
