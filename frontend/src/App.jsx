import { Route, Routes } from "react-router-dom"
import { useLocation } from 'react-router-dom'
import HomePage from "./pages/HomePage"
import AttendeesPage from "./pages/AttendeesPage"

function App() {

  return (
    <>
      <Routes>
        <Route path="/home" element={<HomePage/>}/>  
        <Route path='/attendees' element={<AttendeesPage/>}/>          
      </Routes>
    </>
  )
}

export default App
