import React from 'react'

function InputAttendeeManual({newAttendee, setNewAttendee}) {
  return (
    <div className="bg-gray-700 p-6 rounded-lg w-3/4 max-w-lg shadow-xl transform scale-100">
    <h1 className="text-xl font-bold text-center mb-5 text-white">
        משתתף חדש
    </h1>
    <div className="flex flex-col gap-4">
        <div className="flex flex-col">
        <label htmlFor="full_name" className="text-white font-semibold">שם מלא *</label>
        <input
            id="full_name"
            type="text"
            value={newAttendee.full_name}
            onChange={(e) => setNewAttendee({ ...newAttendee, full_name: e.target.value })}
            placeholder="הכנס שם מלא"
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-greenConvined"
        />
        <small className="text-red-500 mt-1">שדה זה חובה</small>
        </div>

        <div className="flex flex-col">
        <label htmlFor="mispar_ishi" className="text-white font-semibold">מספר אישי</label>
        <input
            id="mispar_ishi"
            type="text"
            value={newAttendee.mispar_ishi}
            onChange={(e) => setNewAttendee({ ...newAttendee, mispar_ishi: e.target.value })}
            placeholder="הכנס מספר אישי"
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-greenConvined"
        />
        <small className="text-red-500 mt-1">שדה זה חובה</small>
        </div>

        <div className="flex flex-col">
        <label htmlFor="tehudat_zehut" className="text-white font-semibold">תעודת זהות</label>
        <input
            id="tehudat_zehut"
            type="text"
            value={newAttendee.tehudat_zehut}
            onChange={(e) => setNewAttendee({ ...newAttendee, tehudat_zehut: e.target.value })}
            placeholder="הכנס תעודת זהות"
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-greenConvined"
        />
        <small className="text-red-500 mt-1">חובה למלא תעודה מזהה</small>
        </div>

        <div className="flex flex-col">
        <label htmlFor="attendance" className="text-white font-semibold">נוכחות (כן/לא)</label>
        <select
            id="attendance"
            value={""}
            onChange={(e) => setNewAttendee({ ...newAttendee, arrived: e.target.value === "כן" })}
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-greenConvined"
        >
            <option value="" disabled hidden>בחר נוכחות</option>
            <option value="כן">כן</option>
            <option value="לא">לא</option>
        </select>
        </div>

        <div className="flex flex-col">
        <label htmlFor="date_arrived" className="text-white font-semibold">תאריך הגעה</label>
        <input
            id="date_arrived"
            type="datetime-local"
            value={newAttendee.date_arrived}
            onChange={(e) => setNewAttendee({ ...newAttendee, date_arrived: e.target.value })}
            className="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-greenConvined"
        />
        </div>

        <button
        onClick={() => handleManualSubmit()}
        className="bg-greenConvined font-semibold text-black p-2 rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-offset-2 focus:ring-green-500 mt-4"
        >
        הוסף
        </button>
    </div>
    </div>
  )
}

export default InputAttendeeManual