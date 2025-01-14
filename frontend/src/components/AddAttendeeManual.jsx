import React, { useState } from "react";
import Modal from "react-modal";

const AddAttendeeManual = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    full_name: "",
    mispar_ishi: "",
    tehudat_zehut: "",
    attendance: "",
    date_arrived: "",
  });

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = () => {
    const { full_name, mispar_ishi, tehudat_zehut, attendance, date_arrived } =
      formData;

    if (!full_name || (!mispar_ishi && !tehudat_zehut)) {
      alert("שם ותעודת זהות או מספר אישי הם שדות חובה");
      return;
    }

    if (attendance === "כן" && !date_arrived) {
      alert("אם המשתתף הגיע, יש להזין תאריך ושעה");
      return;
    }

    console.log("Form Data:", formData);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onRequestClose={onClose} className="modal-content">
      <div className="flex flex-col gap-4">
        <h2 className="text-2xl font-bold text-center text-white">
          הוסף משתתף
        </h2>
        <div className="flex flex-col">
          <label htmlFor="full_name" className="text-white font-semibold">
            שם *
          </label>
          <input
            id="full_name"
            type="text"
            placeholder="הכנס שם"
            value={formData.full_name}
            onChange={handleChange}
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
          />
        </div>
        <div className="flex flex-col">
          <label htmlFor="mispar_ishi" className="text-white font-semibold">
            מספר אישי
          </label>
          <input
            id="mispar_ishi"
            type="number"
            placeholder="הכנס מספר אישי"
            value={formData.mispar_ishi}
            onChange={handleChange}
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
          />
        </div>
        <div className="flex flex-col">
          <label htmlFor="tehudat_zehut" className="text-white font-semibold">
            תעודת זהות
          </label>
          <input
            id="tehudat_zehut"
            type="number"
            placeholder="הכנס תעודת זהות"
            value={formData.tehudat_zehut}
            onChange={handleChange}
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
          />
        </div>
        <div className="flex flex-col">
          <label htmlFor="attendance" className="text-white font-semibold">
            נוכחות
          </label>
          <select
            id="attendance"
            value={formData.attendance}
            onChange={handleChange}
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
          >
            <option value="">בחר נוכחות</option>
            <option value="כן">כן</option>
            <option value="לא">לא</option>
          </select>
        </div>
        {formData.attendance === "כן" && (
          <div className="flex flex-col">
            <label htmlFor="date_arrived" className="text-white font-semibold">
              תאריך הגעה *
            </label>
            <input
              id="date_arrived"
              type="datetime-local"
              value={formData.date_arrived}
              onChange={handleChange}
              className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
            />
          </div>
        )}
        <button
          onClick={handleSubmit}
          className="bg-greenConvined text-black py-2 px-4 rounded hover:bg-green-700"
        >
          שמור
        </button>
        <button
          onClick={onClose}
          className="bg-redConvinedStronger text-white py-2 px-4 rounded hover:bg-red-700"
        >
          ביטול
        </button>
      </div>
    </Modal>
  );
};

export default AddAttendeeManual;
