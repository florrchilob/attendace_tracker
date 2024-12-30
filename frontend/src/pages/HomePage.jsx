import React, { useState } from "react";
import TypingGif from '../assets/gifs/Typing.gif'

const HomePage = () => {
  const [inputValue, setInputValue] = useState("");
  const [selectedOption, setSelectedOption] = useState("misparIishi");

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

  return (
    <div
      dir="rtl"
      className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center"
    >      
    <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg p-6 w-screen py-10 h-full px-auto">
      <h1 className="text-4xl font-bold text-white mb-8 text-center">איזה כיף שמישהבו הגיע!</h1>
        <div className="flex justify-between items-center mb-8 py-auto my-auto align-middle">
          <div className="w-1/3 flex align-center">
            <div className="bg-transparent rounded-lg h-48 w-full flex items-center justify-center">
              <span className="text-white">
                <img className="flex my-auto mx-auto align-center" src={TypingGif} alt="Barcode Scanner" />
              </span>
            </div>
          </div>
          <div className="w-1/3 text-center">
            <select
              className="w-full mb-4 p-2 bg-gray-700 text-white rounded-lg"
              value={selectedOption}
              onChange={(e) => setSelectedOption(e.target.value)}
            >
              <option value="misparIishi">מספר אישי</option>
              <option value="tehudatZehut">תעודת זהות</option>
            </select>
            <input
              type="text"
              className="w-full p-2 bg-gray-700 text-white rounded-lg mb-4"
              placeholder="הכנס מספר"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <button
              onClick={handleSubmit}
              className="w-full p-2 bg-limeConvined text-white rounded-lg font-bold hover:bg-lime-700 transition"
            >
              שלח
            </button>
          </div>
          <div className="w-1/3">
            <div className="bg-transparent rounded-lg h-48 w-full flex items-center justify-center">
              <span className="text-white">gif writing number</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
