import React, { useState } from 'react'
import TypingGif from '../assets/gifs/Typing.gif'
import Swal from "sweetalert2";
import '../App.css'


function NamePage ({ inputID, setInputID, selectedOption, setSelectedOption, setCurrentCard}) {
    const [fullName, setFullName] = useState("")

    const handleSubmit = async() => {
        const now = new Date();
        const localISOTime = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
          .toISOString()
          .slice(0, 19)
          .replace("T", " ");
        const formattedOption = selectedOption.replace(/([A-Z])/g, "_$1").toLowerCase();
        let stringInputID = inputID.toString()
        if (selectedOption == "misparIshi" && stringInputID.startsWith("0")) {
            stringInputID = stringInputID.slice(1)
        }
        const attendee = {[formattedOption]: stringInputID, "full_name": fullName, "arrived": true, "date_arrived": localISOTime}
        const toSend = {"attendees": [attendee]}
        let response = await fetch("http://127.0.0.1:8000/attendees/create", {
            method:'POST',
                    headers: {
                        'Access-Control-Allow-Origin': 'http://localhost:5173',
                        'Content-Type': 'application/json', 
                    },
                    body: JSON.stringify(toSend)

        })
        const data = await response.json()
        const statusCode = response.status
        const errorCode = data.error_code
        if (statusCode == 201){
            const attendee = data["data"]["successfull"][formattedOption][0]
            const dateArrived = attendee["date_arrived"]
            const fullName = attendee["full_name"]
            Swal.fire({
                position: "center",
                icon: "success",
                title: `<div dir="rtl" style="text-align: center;">ההגעה של ${fullName} נרשמה בהצלחה ב${dateArrived}</div>`,
                showConfirmButton: false,
                timer: 2500,
                customClass: {
                popup: "custom-popup",
                title: "custom-title-success",
                },
            }).then(()=> {
                setInputID("")
                setSelectedOption("misparIshi")
                setFullName("")
                setCurrentCard("inputCard")
            })
        }
        else{ 
            Swal.fire({
                position: "center",
                icon: "error",
                title: "שגיאת שרת פנימית",
                text: "נסה שוב מאוחר יותר",
                showConfirmButton: false,
                timer: 2500,
                customClass: {
                popup: "custom-popup-505",
                title: "custom-popup-505-title"          
                },
            }).then(()=> {
                setInputID("")
                setSelectedOption("misparIshi")
                setFullName("")
                setCurrentCard("inputCard")
            })
        }
    };
    
  
    return (
    <div className="bg-gray-800 bg-opacity-90 rounded-3xl w-full shadow-lg p-6 py-10 my-auto items-center overflow-hidden">
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
                    onKeyDown={(e) => 
                        {
                          if (e.key === "Enter") {
                            handleSubmit();
                          }
                        }
                    }
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
    );
  };

export default NamePage