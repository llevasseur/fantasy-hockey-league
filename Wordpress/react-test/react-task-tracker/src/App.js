import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Tasks from './components/Tasks'
import AddTask from './components/AddTask'
import Footer from './components/Footer'
import About from './components/About'

function App() {
    const [showAddTask, setShowAddTask] = useState(false)
    const [tasks, setTasks] = useState([])

    useEffect(() => {
      const getTasks = async () => {
        const tasksFromServer = await fetchTasks()
        setTasks(tasksFromServer)
      }

      getTasks()
    }, [])

    // Fetch Tasks
    const fetchTasks = async () => {
      // Replace this part with any other backend
      const res = await fetch('http://localhost:5000/tasks')
      const data = await res.json()

      return data
    }

    // Fetch Task
    const fetchTask = async (id) => {
      // Replace this part with any other backend
      const res = await fetch(`http://localhost:5000/tasks/${id}`)
      const data = await res.json()

      return data
    }

    // Add Task
    const addTask = async (task) => {
      const res = await fetch('http://localhost:5000/tasks', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body: JSON.stringify(task)
      })

      const data = await res.json()
      setTasks([...tasks, data])
      // if no backend so create an id here
      //const id = Math.floor(Math.random() * 10000) + 1
      //const newTask = { id, ...task }
      //setTasks([...tasks, newTask])
    }

    // Delete Task
    const deleteTask = async (id) => {
        await fetch(`http://localhost:5000/tasks/${id}`, {
          method: "DELETE",
        })

        setTasks(tasks.filter((task) => task.id !== id))
    }

    // Toggle reminder
    const toggleReminder = async (id) => {
        const taskToToggle = await fetchTask(id)
        const updTask = {...taskToToggle, reminder: !taskToToggle.reminder}

        const res = await fetch(`http://localhost:5000/tasks/${id}`, {
          method: "PUT",
          headers: {
            "Content-type": "application/json"
          },
          body: JSON.stringify(updTask)
        })

        const data = await res.json()
        
        setTasks(
          tasks.map((task) => 
            task.id === id ? {...task, reminder: 
            data.reminder} : task
          )
        )
    }

    // Show 

    return (
        <Router>
          <div className="container">
            <Header onAdd={() => setShowAddTask(!showAddTask)} showAdd={showAddTask}/>
            <Routes>
              <Route path='/' exact element={
                <>
                  {showAddTask && <AddTask onAdd={addTask}/>}
                  {tasks.length > 0 ? (
                      <Tasks 
                          tasks={tasks} 
                          onDelete={deleteTask} 
                          onToggle={toggleReminder}
                      /> 
                  ) : (
                    "No tasks to show."
                  )}
                </>
              } />
              <Route path='/about' element={<About/>} />
            </Routes>
            <Footer />
          </div>
        </Router>
    );
}

export default App;
