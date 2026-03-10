/** Arrow-function component example: receives props and returns JSX. */
const CategoryBadge = ({ label }) => (
  <span className="inline-block mt-2 text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600">
    {label}
  </span>
);

export default CategoryBadge;
