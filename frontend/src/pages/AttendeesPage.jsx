import * as XLSX from "xlsx";
import React, { useEffect, useState } from "react";
import AddLogo from "../assets/Logos/AddLogo";
import GarbageLogo from "../assets/Logos/GarbageLogo";
import EditLogo from "../assets/Logos/EditLogo.Jsx";
import LoadingIcon from "../components/loading";
import ErrorPage from "../components/ErrorPage";

const AttendeesPage = () => {
  const [attendees, setAttendees] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    async function fetchAttendees() {
      try {
        const response = await fetch("http://127.0.0.1:8000/attendees/get");
        const data = await response.json();
        const attendees = data["data"]
        setAttendees(attendees);
      } catch (error) {
        setLoading(null)
      } finally {
        setLoading(false);
      }
    }
    fetchAttendees();
  }, []);
  

  const handleDelete = (index) => {
    const newAttendees = attendees.filter((_, i) => i !== index);
    setAttendees(newAttendees);
  };


  const handleImport = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
  
    reader.onload = (event) => {
      const data = new Uint8Array(event.target.result);
      const workbook = XLSX.read(data, { type: "array" });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(sheet);
  
      console.log(jsonData);
    };
  
    reader.readAsArrayBuffer(file);
  };

  // const handleEdit = (index) => {
  //   const newName = prompt("Ingrese un nuevo nombre:");
  //   if (newName) {
  //     const newAttendees = [...attendees];
  //     newAttendees[index].full_name = newName;
  //     setAttendees(newAttendees);
  //   }
  // };

return (
  <div
    dir="rtl"
    className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center"
  >      
    <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg p-6 w-screen py-10">
        <h1 className="text-4xl font-bold text-center mb-6 text-white justify-center flex flex-col">
          רשימת משתתפים
        </h1>
        <h1 className="absolute bg-greenConvined my-6 mx-auto px-2 text-black rounded-xl pb-4 bg-opacity-80 justify-center text-center top-0 text-6xl font-bold ml-4  flex flex-col">
          הגיעו {attendees.length}/{attendees.filter(a => a.arrived).length}
        </h1>
        <input
            type="file"
            accept=".xlsx"
            onChange={handleImport}
            className="transition-all duration-400 block mb-4 bg-transparent hover:bg-lavanderConvined
             border-white hover:border-white font-semibold justify-start my-4 text-white bg-gray-700 rounded-lg p-2"
          />

      <div className="overflow-y-auto max-h-[500px] rounded-lg">
        <table className="w-full text-right bg-gray-700 bg-opacity-70 rounded-lg overflow-hidden">
          <thead className="bg-gray-600 text-gray-300 sticky top-0 z-10">
            <tr>
              <th className="px-4 py-2 text-center">מספר אישי</th>
              <th className="px-4 py-2 text-center">תעודת זהות</th>
              <th className="px-4 py-2 text-center">שם מלא</th>
              <th className="px-4 py-2 text-center">נוכחות</th>
              <th className="px-4 py-2 text-center">תאריך הגעה</th>
              <th className="py-2 w-1 text-center"></th>
            </tr>
          </thead>
          <tbody>
            {loading === true ? (
              <tr>
                <td colSpan="6" className="text-center py-10">
                  <div className="flex justify-center items-center">
                    <LoadingIcon />
                  </div>
                </td>
              </tr>
            ) : loading === null ? (
              <tr>
                <td colSpan="6" className="text-center py-10 text-red-500">
                  שגיאה בטעינת הנתונים. אנא נסה שוב מאוחר יותר.
                </td>
              </tr>
            ) : (
              Array.isArray(attendees) && attendees.map((attendee, index) => (
                <tr key={index} className="border-b bg-gray-800 border-gray-600 hover:bg-gray-600">
                  <td className="px-4 py-2 text-limeConvined text-lg text-center">{attendee.mispar_ishi}</td>
                  <td className="px-4 py-2 text-turquiseConvined text-lg text-center">{attendee.tehudat_zehut}</td>
                  <td className="px-4 py-2 text-greenConvined text-lg text-center">{attendee.full_name}</td>
                  <td className="px-4 py-2 text-lavanderConvined text-lg text-center">
                    {attendee.arrived ? "כן" : "לא"}
                  </td>
                  <td className="px-4 py-2 text-pinkConvined text-lg text-center">
                    {attendee.date_arrived || "—"}
                  </td>
                  <td className="p-2 flex justify-center">
                    {/* <button
                      onClick={() => handleEdit(index)}
                      className="py-1 px-3 bg-transparent text-white font-semibold rounded-lg hover:border-yellowConvined"
                    >
                      <EditLogo/>
                    </button> */}
                    <button
                      onClick={() => handleDelete(index)}
                      className="py-1 px-3 bg-transparent text-white font-semibold rounded-lg hover:border-redConvinedStronger"
                    >
                      <GarbageLogo/>
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  </div>
);

  
  
  
};

export default AttendeesPage;
