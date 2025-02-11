import { Route, Routes, useNavigate  } from "react-router-dom"
import { useLocation } from 'react-router-dom'
import HomePage from "./pages/HomePage"
import AttendeesPage from "./pages/AttendeesPage"
import AkaIcon from "../src/assets/Logos/AkaIcon"

function App() {

  const navigate = useNavigate()

  const handleNavigateHome = () => {
    navigate('/home')
  }

  return (
    <>
      <button 
        onClick={handleNavigateHome} 
        className="absolute top-8 left-8 border-none cursor-pointer z-50 focus:outline-none 
        rounded-full 
        transition-all 
        duration-300 
        hover:shadow-lg 
        hover:shadow-lavanderConvined"
      >     
        <AkaIcon />
      </button>
      <Routes>
        <Route path="/home" element={<HomePage/>}/>  
        <Route path="/attendees" element={<AttendeesPage/>}/>          
      </Routes>
    </>
  )
}

export default App
