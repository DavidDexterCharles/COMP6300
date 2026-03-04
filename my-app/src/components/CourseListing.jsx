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
