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
          className="text-sm px-3 py-1.5 rounded bg-slate-200 text-slate-700 hover:bg-slate-300">
          Edit
        </button>
        <button
          type="button"
          onClick={() => onDelete(course.id)}
          className="text-sm px-3 py-1.5 rounded bg-red-100 text-red-700 hover:bg-red-200">
          Delete
        </button>
      </div>
    </Card>
  );
}
