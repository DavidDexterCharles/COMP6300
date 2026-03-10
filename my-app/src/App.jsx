import "./App.css";
import { Routes, Route, Link } from "react-router-dom";
import CourseManager from "./components/CourseManager";
import About from "./pages/About";

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="border-b border-slate-200 bg-white px-6 py-3 flex gap-4">
        <Link to="/" className="text-slate-700 hover:text-slate-900 font-medium">
          Home
        </Link>
        <Link to="/about" className="text-slate-700 hover:text-slate-900 font-medium">
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
