import React, { useState } from "react";

function HomePage() {
  const [inputValue, setInputValue] = useState(""); // Para el input
  const [selectedOption, setSelectedOption] = useState("misparIishi"); // Default: Mispar Iishi

  const handleSubmit = () => {
    if (!inputValue.trim()) {
      alert("Por favor, ingresa un número válido.");
      return;
    }

    // Simula una llamada al backend
    const response = { status: "ok" }; // Simulación de respuesta del backend

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
  <div dir="rtl" className="bg-bg-desktop bg-cover bg-center h-screen w-screen"  >
    <h1>dfdsfgdfgברוך הבא</h1>
      <div>
        {/* Input */}
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="הכנס מספר זהות"
          style={{
            padding: "10px",
            margin: "20px",
            textAlign: "right",
            direction: "rtl",
            fontSize: "16px",
          }}
        />
        {/* Switch */}
        <div style={{ marginBottom: "20px" }}>
          <label>
            <input
              type="radio"
              name="type"
              value="tehudatZehut"
              onChange={() => setSelectedOption("tehudatZehut")}
            />
            תעודת זהות
          </label>
          <label style={{ marginLeft: "20px" }}>
            <input
              type="radio"
              name="type"
              value="misparIishi"
              onChange={() => setSelectedOption("misparIishi")}
              defaultChecked
            />
            מספר אישי
          </label>
        </div>
        {/* Botón */}
        <button
          onClick={handleSubmit}
          style={{
            padding: "10px 20px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
            fontSize: "16px",
          }}
        >
          שלח
        </button>
      </div>
    </div>
  );
}

export default HomePage;
