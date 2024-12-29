import React, { useState } from "react";

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
    <div className="bg-bg-desktop bg-cover bg-center h-screen w-screen flex items-center justify-center">
      <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg p-8 text-center w-4/5 md:w-2/3 lg:w-1/2">
        <h1 className="text-4xl font-bold text-white mb-8">ברוך הבא!</h1>
        <div className="flex flex-wrap justify-between items-center mb-8">
          <div className="w-1/3">
            <div className="bg-black rounded-lg h-48 w-full flex items-center justify-center">
              <span className="text-white">gif scanning card</span>
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
            <div className="bg-black rounded-lg h-48 w-full flex items-center justify-center">
              <span className="text-white">gif writing number</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
