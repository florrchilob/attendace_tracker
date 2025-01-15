import React, { useState } from "react";


const AddAttendeeManual = ( ) => {
  const [formData, setFormData] = useState({
    full_name: "",
    mispar_ishi: "",
    tehudat_zehut: "",
    attendance: "",
    date_arrived: "",
  });

  const handleSubmit = () => {
    // const { full_name, mispar_ishi, tehudat_zehut, attendance, date_arrived } =
    //   formData;

    // if (!full_name || (!mispar_ishi && !tehudat_zehut)) {
    //   alert("שם ותעודת זהות או מספר אישי הם שדות חובה");
    //   return;
    // }

    // if (attendance === "כן" && !date_arrived) {
    //   alert("אם המשתתף הגיע, יש להזין תאריך ושעה");
    //   return;
    // }

    // console.log("Form Data:", formData);
    // onClose();
  };

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-2xl font-bold text-limeConvined">משתתף חדש</h1>
      <div className="flex flex-col">
        <label for="full_name" className="text-white font-semibold">שם *</label>
        <input
          id="full_name"
          type="text"
          placeholder="הכנס שם"
          className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
        />
        <small className="text-redConvinedStronger mt-1">שדה זה חובה</small>
      </div>
      <div className="flex flex-col">
        <label for="mispar_ishi" className="text-white font-semibold">מספר אישי</label>
        <input
          id="mispar_ishi"
          type="number"
          placeholder="הכנס מספר אישי"
          className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
        />
        <small className="text-redConvinedStronger mt-1">תעודת זהות או מספר אישי הם שדות חובה</small>
      </div>
      <div className="flex flex-col">
        <label for="tehudat_zehut" className="text-white font-semibold">תעודת זהות</label>
        <input
          id="tehudat_zehut"
          type="number"
          placeholder="הכנס תעודת זהות"
          className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
        />
        <small className="text-redConvinedStronger mt-1">תעודת זהות או מספר אישי הם שדות חובה</small>
      </div>
      <div className="flex flex-col">
        <label for="attendance" className="text-white font-semibold">נוכחות</label>
        <select
          id="attendance"
          className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
          onchange="toggleDateField(this.value)"
        >
          <option value="">בחר נוכחות</option>
          <option value="כן">כן</option>
          <option value="לא">לא</option>
        </select>
      </div>
      <div id="date-field" className="flex flex-col">
        <label for="date_arrived" className="text-white font-semibold">תאריך הגעה *</label>
        <input
          id="date_arrived"
          type="datetime-local"
          className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
        />
        <small className="text-redConvinedStronger mt-1">שדה זה חובה אם המשתתף הגיע</small>
      </div>
    </div>
  );
};

export default AddAttendeeManual;
