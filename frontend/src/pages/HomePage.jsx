import React, { useEffect, useRef, useState } from "react";
import TypingGif from '../assets/gifs/Typing.gif'
import ScanningGif from '../assets/gifs/Scanning.gif'

const HomePage = () => {
  const [inputValue, setInputValue] = useState("");
  const inputRef = useRef(null);
  const [selectedOption, setSelectedOption] = useState("misparIishi");

  const onChangeInput = () => {
    if (selectedOption == "misparIshi"){
      if (inputRef.length > 11){
        // alert
      }
      else{
        setInputValue(inputRef)
      }
    }
    if (selectedOption == "tehudatZehut"){
      if (inputRef.length > 9){
        // alert
      }
      else{
        setInputValue(inputRef)
      }
    }
  }

  const handleSubmit = () => {
    if (!inputValue.trim()) {
      alert("Por favor, ingresa un número válido.");
      return;
    }

    const response = { status: "ok" };

    if (response.status === "ok") {
      alert("Número guardado correctamente.");
    } else if (response.status === "new") {
      const fullName = prompt("Nuevo asistente. Por favor, ingresa el nombre completo:");
      if (fullName) {
        alert(`Nuevo asistente registrado: ${fullName}`);
      }
    } else {
      alert("Error del sistema. Intenta nuevamente.");
    }
  };

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  return (
    <div
      dir="rtl"
      className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center"
    >      
    <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg p-6 w-screen py-10 h-full px-auto py-auto items-center overflow-hidden">
      <h1 className="text-4xl font-bold text-white mb-8 text-center flex-row">איזה כיף שמישהבו הגיע!</h1>
      <div className="flex flex-row justify-center mt-16">
        <div className="w-5/12 text-center flex justify-center flex-col items-center relative z-20">
          <select
            className="w-full mb-4 p-2 bg-gray-700 text-white rounded-lg h-12"
            value={selectedOption}
            onChange={(e) => setSelectedOption(e.target.value)}
          >
            <option value="misparIshi">מספר אישי</option>
            <option value="tehudatZehut">תעודת זהות</option>
          </select>
          <input
            ref={inputRef}
            type="number"
            className="w-full p-2 bg-gray-700 text-white rounded-lg mb-4 h-12"
            placeholder="הכנס מספר"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button
            onClick={handleSubmit}
            className="px-16 py-2 bg-turquiseConvined text-black rounded-3xl border-white font-bold hover:bg-greenConvined hover:border-white transition"
          >
            שלח
          </button>
        </div>
      </div>
      <div className="py-0 justify-between items-stretch flex flex-row h-auto overflow-hidden my-[-69px] z-0">
        <div className="w-3/5 flex align-center flex-col justify-end items-start">
          <img className="flex my-auto justify-end" src={ScanningGif} alt="Barcode Scanner" />
        </div>
        <div className="w-2/5 flex align-center flex-col justify-start items-end">
            <img className="flex my-auto justify-start" src={TypingGif} alt="Barcode Scanner" />
        </div>
        
      </div>
    </div>
    </div>
  );
};

export default HomePage;
