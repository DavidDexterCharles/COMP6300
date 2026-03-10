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
