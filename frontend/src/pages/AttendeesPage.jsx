import React, { useState } from "react";
import AddLogo from "../assets/Logos/AddLogo";
import GarbageLogo from "../assets/Logos/GarbageLogo";
import EditLogo from "../assets/Logos/EditLogo.Jsx";

const AttendeesPage = () => {
  const [attendees, setAttendees] = useState([
    { mispar_ishi: "123456", tehudat_zehut: "987654321", full_name: "זינזו צ'אן לי", arrived: true, date_arrived: "2023-12-17" },
    { mispar_ishi: "234567", tehudat_zehut: "876543219", full_name: "ג'יט סרו", arrived: false, date_arrived: null },
  ]);

  const handleDelete = (index) => {
    const newAttendees = attendees.filter((_, i) => i !== index);
    setAttendees(newAttendees);
  };

  const handleAdd = () => {
    const newAttendee = {
      mispar_ishi: "Nuevo",
      tehudat_zehut: "Nuevo",
      full_name: "חדש",
      arrived: false,
      date_arrived: null,
    };
    setAttendees([...attendees, newAttendee]);
  };

  const handleEdit = (index) => {
    const newName = prompt("Ingrese un nuevo nombre:");
    if (newName) {
      const newAttendees = [...attendees];
      newAttendees[index].full_name = newName;
      setAttendees(newAttendees);
    }
  };

  return (
    <div
      dir="rtl"
      className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center"
    >      
      <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg p-6 w-screen py-10">
        <h1 className="text-4xl font-bold text-center mb-6 text-white">רשימת משתתפים</h1>
        <button
          onClick={handleAdd}
          className="transition-all duration-400 block mb-4 p-2 bg-transparent hover:bg-lavanderConvined border-white hover:border-white font-semibold rounded-full justify-start"
        >
          <AddLogo/>
        </button>
        <div className="overflow-x-auto">
          <table className="w-full text-right bg-gray-700 bg-opacity-70 rounded-lg overflow-hidden">
            <thead className="bg-gray-600 text-gray-300">
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
              {attendees.map((attendee, index) => (
                <tr key={index} className="border-b bg-gray-800  border-gray-600 hover:bg-gray-600">
                  <td className="px-4 py-2 text-limeConvined text-lg text-center">{attendee.mispar_ishi}</td>
                  <td className="px-4 py-2 text-turquiseConvined text-lg text-center">{attendee.tehudat_zehut}</td>
                  <td className="px-4 py-2 text-greenConvined text-lg text-center">{attendee.full_name}</td>
                  <td className="px-4 py-2 text-lavanderConvined text-lg text-center">{attendee.arrived ? "כן" : "לא"}</td>
                  <td className="px-4 py-2 text-pinkConvined text-lg text-center">{attendee.date_arrived || "—"}</td>
                  <td className="p-2 flex justify-center">
                    <button
                      onClick={() => handleEdit(index)}
                      className="py-1 px-3 bg-transparent text-white font-semibold rounded-lg hover:border-yellowConvined"
                    >
                      <EditLogo/>
                    </button>
                    <button
                      onClick={() => handleDelete(index)}
                      className="py-1 px-3 bg-transparent text-white font-semibold rounded-lg hover:border-redConvinedStronger"
                    >
                      <GarbageLogo/>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AttendeesPage;
