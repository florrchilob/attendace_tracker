import React, { useState } from 'react'

function NamePage({ inputID, setInputID, selectedOption, setSelectedOption, setCurrentCard}) {
    const [fullName, setFullName] = useState("")
  

    // const handleSubmit = () => {
    //   if (!fullName.trim() || fullName.trim().split(" ").length < 2) {
    //     alert("אנא הכנס שם מלא המכיל לפחות שתי מילים");
    //     return;
    //   }
    //   onSubmitName(fullName);
    // };
  
    return (
    <div
    dir="rtl"
    className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center overflow-hidden"
    >      
        <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg h-full w-full px-auto py-auto items-center overflow-hidden px-12">
            <h1 className="text-7xl font-bold text-white align-top flex justify-center my-24">בן אדם לא ברשימה</h1>
            <h2 className="text-3xl font-bold text-gray-400 ">אנא הכנס שם מלא:</h2>
            <input
            type="text"
            className="p-2 bg-gray-700 text-white rounded-lg mb-4 w-full h-20 mt-3 text-center " 
            placeholder="הכנס שם מלא"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            />
            <div className="flex gap-4 justify-center">
                <button
                    // onClick={handleSubmit}
                    className="py-4 px-16 mx-12 mt-6 bg-greenConvined text-black rounded-2xl font-bold hover:bg-green-600 transition"
                >
                    שלח
                </button>
                <button
                    // onClick={onCancel}
                    className="py-4 px-16 mx-12 mt-6 bg-redConvinedStronger text-black rounded-2xl font-bold hover:bg-red-600 transition"
                >
                    בטל
                </button>
            </div>
        </div>
    </div>
    );
  };

export default NamePage