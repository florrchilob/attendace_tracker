import React, { useState } from 'react'
import TypingGif from '../assets/gifs/Typing.gif'
import Swal from "sweetalert2";
import '../App.css'


function NamePage({ inputID, setInputID, selectedOption, setSelectedOption, setCurrentCard}) {
    const [fullName, setFullName] = useState("")

    const handleSubmit = () => {
      if (!fullName.trim() || fullName.trim().split(" ").length < 2) {
        Swal.fire({
          icon: "error",
          title: "שגיאה",
          text: "אנא הכנס שם מלא המכיל לפחות שתי מילים",
          showConfirmButton: false,
          timer: 3500,
          customClass: {
            popup: "custom-popup",
            title: "custom-title-error",
          },
        });
        return;
      }
    //   LLamar a backend para guardar el nombre en la base de datos
    };
    
  
    return (
    <div
    dir="rtl"
    className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center overflow-hidden"
    >      
        <div className="bg-gray-800  bg-opacity-90 rounded-3xl shadow-lg h-full w-full px-auto py-auto items-center overflow-hidden px-12 flex flex-col">
            <h1 className="text-7xl font-bold text-greenConvined border-b border-turquiseConvined align-top flex justify-center my-24 flex-row w-full">בן אדם לא ברשימה</h1>
            <div className='flex flex-row justify-between'>
                <div className='w-1/2 flex flex-col justify-start  items-center my-auto bg-slate-700 hover:bg-slate-600 h-full p-10 rounded-3xl'>
                    <div className='align-middle flex flex-col my-auto'>
                        <h2 className="text-5xl font-bold text-white mb-8">אנא הכנס שם מלא:</h2>
                        <input
                        type="text"
                        className="p-2 bg-gray-500 text-white rounded-lg mb-4 h-12 my-12"
                        placeholder="הכנס שם מלא"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        />
                        <div className="flex gap-4 justify-center">
                            <button
                                onClick={handleSubmit}
                                className="py-4 px-16 mx-12 mt-6 bg-turquiseConvined border-none text-black rounded-2xl font-bold hover:bg-limeConvined transition"
                                >
                                שלח
                            </button>
                        </div>
                    </div>
                </div>
                <div className='w-1/2 flex flex-col justify-end'>
                    <img className="flex my-auto justify-start" src={TypingGif} alt="Barcode Scanner" />
                </div>
            </div>
        </div>
    </div>
    );
  };

export default NamePage