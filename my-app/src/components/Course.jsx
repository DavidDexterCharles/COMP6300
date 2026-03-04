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
  )
}
