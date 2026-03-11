export default function About() {
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-semibold text-slate-800 mb-4">About</h1>
      <p className="text-slate-600 mb-4">
        This app is a <strong>Course Manager</strong> for viewing and managing a
        list of courses. You can search by course code or title, create new
        courses, edit existing ones, and delete courses. The course list is
        shown on the Home page; this About page describes what the app does.
      </p>
      <p className="text-slate-600">
        It is built with React and used as a teaching example for components,
        state, props, events, and routing.
      </p>
    </div>
  );
}
