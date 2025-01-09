import React, { useEffect, useRef, useState } from "react";
import TypingGif from '../assets/animations/Typing.gif'
import ScanningGif from '../assets/animations/Scanning.gif'
import Swal from 'sweetalert2';
import '../App.css'


const InputPage = ({ inputID, setInputID, selectedOption, setSelectedOption, setCurrentCard}) => {
  const inputRef = useRef(null);
  
  const apiUrl = process.env.REACT_APP_API_URL + "/attendees";
  
  const onChangeInput = () => {
    if (selectedOption == "misparIshi" && inputRef.current.value.length > 253 || selectedOption == "tehudatZehut" && inputRef.current.value.length > 9){
      Swal.fire({
        position: "top",
        icon: "error",
        title: "בדוק את המספר שהוזן בבקשה",
        showConfirmButton: false,
        timer: 3500,
        customClass: {
          popup: "custom-popup",
          title: "custom-title",
        },
      });
    }
    else{
      setInputID(inputRef.current.value)
    }
  }

  const  handleSubmit = async() => {
    if (selectedOption == "misparIshi" && inputID.length < 6 || selectedOption == "tehudatZehut" && inputID.length != 9) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "בדוק את המספר שהוזן בבקשה",
        showConfirmButton: false,
        timer: 3500,
        customClass: {
          popup: "custom-popup",
          title: "custom-title",
        },
      });
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
    else{
      const formattedOption = selectedOption.replace(/([A-Z])/g, "_$1").toLowerCase();
      let stringInputID = inputID.toString()
      if (selectedOption == "misparIshi" && stringInputID.startsWith("0")) {
        stringInputID = stringInputID.slice(1)
      }
      const attendee = {[formattedOption]: stringInputID}
      const  response = await fetch(`${apiUrl}/arrived`, {
        method:'PUT',
                headers: {
                    'Access-Control-Allow-Origin': 'http://localhost:80',
                    'Content-Type': 'application/json', 
                },
                body: JSON.stringify(attendee)

      })
      const data = await response.json()
      const statusCode = response.status
      const errorCode = data.error_code
      if (statusCode == 200){
        const fullName = data['data']['full_name']
        const formattedTime = data['data']['date_arrived']
        Swal.fire({
          position: "center",
          icon: "success",
          title: `<div dir="rtl" style="text-align: center;">ההגעה של ${fullName} נרשמה בהצלחה ב${formattedTime}</div>`,
          showConfirmButton: false,
          customClass: {
            popup: "custom-popup",
            title: "custom-title-success",
          },
        }).then(()=> {
          setInputID("")
          setSelectedOption("misparIshi")
          setTimeout(() => {
            if (inputRef.current) {
              inputRef.current.focus();
            }
          }, 100);
        })
      }
      else{
          if (statusCode == 400 && errorCode == 104){
            setCurrentCard("nameCard")
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
              setTimeout(() => {
                if (inputRef.current) {
                  inputRef.current.focus();
                }
              }, 100);
            })
          }
      }
    }
  };

  const onChangeSelect = (e) => {
    if (e.target.value == "misparIshi" && inputID.length > 11 || e.target.value == "tehudatZehut" && inputID.length > 9){
      setInputID("")
    }
    setSelectedOption(e.target.value)
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);
  
  useEffect(() => {
    const handleFocusChange = () => {
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  
    window.addEventListener("focus", handleFocusChange, true);
    window.addEventListener("blur", handleFocusChange, true);
  
    return () => {
      window.removeEventListener("focus", handleFocusChange, true);
      window.removeEventListener("blur", handleFocusChange, true);
    };
  }, []);
  
  

  return (
    <div className="bg-gray-800 bg-opacity-90 rounded-3xl w-full shadow-lg p-6 py-10 my-auto items-center overflow-hidden">
      <h1 className="text-4xl font-bold text-white mb-8 text-center flex-row">איזה כיף שמישהו הגיע!</h1>
      <div className="flex flex-row justify-center mt-16">
        <div className="w-5/12 text-center flex justify-center flex-col items-center relative z-20 transition-all duration-500">
          <select
            className="w-full mb-4 p-2 bg-gray-700 text-white rounded-lg h-12"
            value={selectedOption}
            onChange={(e) => onChangeSelect(e)}
          >
            <option value="misparIshi">מספר אישי</option>
            <option value="tehudatZehut">תעודת זהות</option>
          </select>
          <input
            ref={inputRef}
            type="number"
            className="w-full p-2 bg-gray-700 text-white rounded-lg mb-4 h-12"
            placeholder="הכנס מספר"
            value={inputID}
            onChange={() => onChangeInput()}
            onKeyDown={(e) => 
              {
                if (e.key === "Enter") {
                  handleSubmit();
                }
              }
            }
          />
          <button
            onClick={handleSubmit}
            className="px-16 py-2 bg-turquiseConvined text-black rounded-3xl border-white font-bold hover:bg-greenConvined hover:border-white transition"
          >
            שלח
          </button>
        </div>
      </div>
      <div className="py-0 justify-between items-stretch flex flex-row h-auto overflow-hidden my-[-69px] z-0 ms-[-109px]">
        <div className="w-3/5 flex align-center flex-col justify-end items-start">
          <img className="flex my-auto justify-end" src={ScanningGif} alt="Barcode Scanner"/>
        </div>
        <div className="w-2/5 flex align-center flex-col justify-end items-end">
            <img className="flex my-auto justify-start" src={TypingGif} alt="Barcode Scanner" />
        </div>
        
      </div>
    </div>
  );
};

export default InputPage;
