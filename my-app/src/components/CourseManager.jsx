import { useState, useMemo } from 'react'
import CourseSearch from './CourseSearch'
import CourseListing from './CourseListing'

const INITIAL_COURSES = [
  { id: 1, code: 'COMP 6501', title: 'Research Methods, Entrepreneurship and Intellectual Property', category: 'Core' },
  { id: 2, code: 'COMP 6925', title: 'Applied Operations Research', category: 'Core' },
  { id: 3, code: 'STAT 6105', title: 'Probability and Statistical Methods for Data Analytics', category: 'Core' },
  { id: 4, code: 'STAT 6106', title: 'Statistical Inference for Data Analytics', category: 'Core' },
  { id: 5, code: 'COMP 6930', title: 'Machine Learning and Data Mining', category: 'Core' },
  { id: 6, code: 'COMP 6940', title: 'Big Data and Visual Analytics', category: 'Core' },
  { id: 7, code: 'STAT 6005', title: 'Research Project', category: 'Core' },
  { id: 8, code: 'COMP 6300', title: 'Advanced Internet Technologies', category: 'Elective' },
  { id: 9, code: 'COMP 6401', title: 'Advanced Algorithms', category: 'Elective' },
  { id: 10, code: 'COMP 6802', title: 'Distributed and Parallel Database Systems', category: 'Elective' },
  { id: 11, code: 'COMP 6905', title: 'Cloud Technologies', category: 'Elective' },
  { id: 12, code: 'STAT 6160', title: 'Data Analysis', category: 'Elective' },
  { id: 13, code: 'STAT 6170', title: 'Multivariate Analysis', category: 'Elective' },
  { id: 14, code: 'STAT 6181', title: 'Computational Statistics I', category: 'Elective' },
  { id: 15, code: 'STAT 6182', title: 'Computational Statistics II', category: 'Elective' },
]

export default function CourseManager() {
  const [courses, setCourses] = useState(INITIAL_COURSES)
  const [searchTerm, setSearchTerm] = useState('')

  const filteredCourses = useMemo(() => {
    if (!searchTerm.trim()) return courses
    const term = searchTerm.toLowerCase().trim()
    return courses.filter(
      (c) =>
        c.code.toLowerCase().includes(term) ||
        c.title.toLowerCase().includes(term)
    )
  }, [courses, searchTerm])

  function handleCreate(course) {
    setCourses((prev) => [...prev, { ...course, id: Math.max(0, ...prev.map((c) => c.id)) + 1 }])
  }

  function handleUpdate(id, updates) {
    setCourses((prev) =>
      prev.map((c) => (c.id === id ? { ...c, ...updates } : c))
    )
  }

  function handleDelete(id) {
    setCourses((prev) => prev.filter((c) => c.id !== id))
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-2xl font-semibold text-slate-800 mb-6">Course list</h1>
      <CourseSearch value={searchTerm} onChange={setSearchTerm} />
      <CourseListing
        courses={filteredCourses}
        onCreate={handleCreate}
        onUpdate={handleUpdate}
        onDelete={handleDelete}
      />
    </div>
  )
}
