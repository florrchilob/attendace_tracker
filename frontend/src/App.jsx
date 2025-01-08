import { Route, Routes } from "react-router-dom"
import { useLocation } from 'react-router-dom'
import HomePage from "./pages/HomePage"
import AttendeesPage from "./pages/AttendeesPage"
import TestSocket from "./pages/SocketTest"

function App() {
  const location = useLocation().pathname

  return (
    <>
      <Routes>
        <Route path="/home" element={<HomePage/>}/>  
        <Route path='/attendees' element={<AttendeesPage/>}/>          
        <Route path='/testing' element={<TestSocket/>}/>          
      </Routes>
    </>
  )
}

export default App
