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
