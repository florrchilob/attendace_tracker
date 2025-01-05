import * as XLSX from "xlsx";
import React, { useEffect, useState } from "react";
import AddLogo from "../assets/Logos/AddLogo";
import GarbageLogo from "../assets/Logos/GarbageLogo";
import EditLogo from "../assets/Logos/EditLogo.Jsx";
import LoadingIcon from "../components/loading";
import Swal from "sweetalert2";
import '../App.css'
// import ErrorPage from "../components/ErrorPage";

const AttendeesPage = () => {
  const [attendees, setAttendees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [file, setFile] = useState(null);

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
  
  useEffect(() => {
    fetchAttendees();
  }, []);
  
  const formatDate = (isoString) => {
    const date = new Date(isoString)
    const day = String(date.getDate()).padStart(2, "0")
    const month = String(date.getMonth() + 1).padStart(2, "0")
    const year = date.getFullYear()
    const hours = String(date.getHours()).padStart(2, "0")
    const minutes = String(date.getMinutes()).padStart(2, "0")
  
    return `${day}/${month}/${year} ${hours}:${minutes}`
  };

  const handleDelete = async() => {
    let response = await fetch("http://127.0.0.1:8000/attendees/deleteall", {
      method: 'DELETE',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      }
    });

    if (response.status === 200) {
      setAttendees([]);  
      Swal.fire({
        position: "center",
        icon: "success",
        title: "המשתתפים הוסרו בהצלחה",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup",
          title: "custom-title-success",
        },
      })
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
      })
    }

  };

  const exportErrorsToExcel = (missingData) => {
    const formattedData = missingData.map((item) => ({
      "מספר אישי": item.attendee.mispar_ishi || "",
      "תעודת זהות": item.attendee.tehudat_zehut || "",
      "שם מלא": item.attendee.full_name || "",
      "נוכחות": item.attendee.arrived === true ? "כן" : item.attendee.arrived === false ? "לא" : "",
      "תאריך הגעה": item.attendee.date_arrived || "",
      "שגיאה": item.error.message,
    }));
  
    const worksheet = XLSX.utils.json_to_sheet(formattedData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "שגיאות");
  
    XLSX.writeFile(workbook, "missing_data_errors.xlsx", { bookType: "xlsx", type: "binary" });
  };

  const handleImport = async(e) => {
    setFile(true);
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = async (event) => {
      const data = new Uint8Array(event.target.result);
      const workbook = XLSX.read(data, { type: "array" });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      let jsonData = XLSX.utils.sheet_to_json(sheet);

      const columnMapping = {
        "תעודת זהות": "tehudat_zehut",
        "מספר אישי": "mispar_ishi",
        "שם מלא": "full_name",
        "נוכחות": "arrived",
        "תאריך הגעה": "date_arrived",
      };

      jsonData = jsonData.map((row) => {
        const newRow = {};

        for (let key in row) {
          if (columnMapping[key]) {
            const mappedKey = columnMapping[key];
            const value = row[key];
        
            if (value !== null && value !== undefined && value !== "") {
              if (mappedKey === "arrived") {
                newRow[mappedKey] = value === "כן" ? true : value === "לא" ? false : null;
        
              } else if (mappedKey === "date_arrived") {
                if (typeof value === "number") {
                  const excelEpoch = new Date(1900, 0, 1);
                  const date = new Date(excelEpoch.getTime() + (value - 2) * 86400000);
        
                  const formattedDate = date
                    .toISOString()
                    .replace("T", " ")
                    .slice(0, 19);
                  newRow[mappedKey] = formattedDate;
        
                } else if (typeof value === "string" && value.includes(" ")) {
                  const dateParts = value.split(" ");
                  const date = dateParts[0].split("/").reverse().join("-");
                  const time = dateParts[1];
                  newRow[mappedKey] = `${date} ${time}:00`;
        
                } else {
                  newRow[mappedKey] = value;
                }
        
              } else {
                newRow[mappedKey] = value;
              }
            }
          }
        }
         
        return newRow;
      })

      const toSend = { "attendees": jsonData };
      fetch("http://127.0.0.1:8000/attendees/create", {
        method: 'POST',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(toSend)
      })
      .then(response => {
        if (response.status === 500) {
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
          });
          throw new Error("Server error 500");
        }
        return response.json();
      })
      .then(dataResponse => {
        fetchAttendees()
        const missingData = dataResponse["data"]["missing_data"];
        if (missingData.length > 0) {
          Swal.fire({
            position: "center",
            icon: "warning",
            title: "בדוק פרטים בבקשה",
            text: "בדוק את תיקיית ההורדות, הורד אקסל עם המשתמשים שיש להם שגיאות, אנא תקן את הנתונים שהוזנו עבור כל משתתף",
            showConfirmButton: false,
            timer: 2000,
            customClass: {
              popup: "custom-popup-505",
              title: "custom-popup-505-title"
            },
          });
          exportErrorsToExcel(missingData)
        } else {
          Swal.fire({
            position: "center",
            icon: "success",
            title: "הנתונים נשמרו בהצלחה",
            showConfirmButton: false,
            timer: 2000,
            customClass: {
              popup: "custom-popup",
              title: "custom-title-success",
            },
          });
        }
      })
      .catch(error => {
        console.error("Error:", error);
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
        });
      });
      };
      
    fetchAttendees();
    setTimeout(() => {
        setAdding(false);
    }, 1000);
    reader.readAsArrayBuffer(file);

  };
  
  function exportToExcel() {
    if (!attendees || attendees.length === 0) {
      alert("אין נתונים לייצוא.");
      return;
    }
  
    const exportData = attendees.map(attendee => ({
      "מספר אישי": attendee.mispar_ishi || "",
      "תעודת זהות": attendee.tehudat_zehut || "",
      "שם מלא": attendee.full_name || "",
      "נוכחות": attendee.arrived ? "כן" : "לא",
      "תאריך הגעה": attendee.date_arrived
        ? formatDate(attendee.date_arrived)
        : "—"
    }));
  
    const worksheet = XLSX.utils.json_to_sheet(exportData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "משתתפים");
  
    XLSX.writeFile(workbook, "רשימת_משתתפים.xlsx");
  }


return (
    <div
      dir="rtl"
      className="bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center"
    >      
      <div className="bg-gray-800 bg-opacity-90 rounded-3xl shadow-lg p-6 w-screen py-10">
          <h1 className="text-4xl font-bold text-center mb-6 text-white justify-center flex flex-col">
            רשימת משתתפים
          </h1>
          
  
          {loading === false &&
            (
              <h1 className="absolute bg-greenConvined my-6 mx-auto px-2 text-black rounded-xl pb-4 bg-opacity-80 justify-center text-center top-0 text-6xl font-bold ml-4  flex flex-col">
                הגיעו {attendees.filter(a => a.arrived).length}/{attendees.length}
              </h1>
            )
          }
        <div className="flex flex-row justify-between">  
          {adding ? (
            <div className="flex items-center space-x-2 transition-all duration-500 flex-row py-auto">
              <input
                type="file"
                accept=".xlsx"
                onChange={handleImport}
                className="transition-all duration-400 block my-4 bg-transparent hover:bg-lavanderConvined
                border-white hover:border-white font-semibold justify-start text-white bg-gray-700 rounded-lg p-2 flex-col"
              />
              {file &&
                <button
                  onClick={() => {
                    setAdding(false);
                    setFile(null);
                  }}
                  className="transition-all border-none duration-400 bg-redConvinedStronger hover:bg-red-700 text-white font-semibold rounded-full py-2 px-3 flex-col my-auto"
                >
                  ✕
                </button>
              }
            </div>
          ) : (
            <button
              onClick={() => setAdding(true)}
              className="transition-all duration-500 block mb-4 bg-transparent hover:bg-lavanderConvined
              border-white hover:border-white font-semibold justify-start text-white bg-gray-700 rounded-full py-2 px-3"
            >
              <AddLogo />
            </button>
          )}
            <div className="flex flex-row items-center">
              <button
                      onClick={() => handleDelete()}
                      className="py-2 px-4 bg-transparent text-white font-semibold rounded-lg hover:border-redConvinedStronger border border-white"
                      >
                <GarbageLogo/>
              </button>
              <div className="flex justify-end m-4">
                <button
                  onClick={exportToExcel}
                  className="transition-all duration-400 px-4 py-2 bg-transparent hover:border-greenConvined text-greenConvined font-semibold rounded-lg border border-white"
                  >
                  ייצא לאקסל
                </button>
              </div>
            </div>
        </div>

      <div className="overflow-y-auto max-h-[500px] rounded-lg">
        <table className="w-full text-right bg-gray-700 bg-opacity-70 rounded-lg overflow-hidden">
          <thead className="bg-gray-600 text-gray-300 sticky top-0 z-10">
            <tr>
              <th className="px-4 py-2 text-center">מספר אישי</th>
              <th className="px-4 py-2 text-center">תעודת זהות</th>
              <th className="px-4 py-2 text-center">שם מלא</th>
              <th className="px-4 py-2 text-center">נוכחות</th>
              <th className="px-4 py-2 text-center">תאריך הגעה</th>
            </tr>
          </thead>
          <tbody>
            {loading === true ? (
              <tr>
                <td colSpan="6" className="text-center py-10">
                  <div className="flex justify-center items-center mx-auto">
                    <LoadingIcon />
                  </div>
                </td>
              </tr>
            ) : loading === null ? (
              <tr className="h-60">
                <td>
                  <div className="flex justify-center items-center mx-auto flex-col">
                    <h4 className="text-4xl font-bold text-center mb-[-80px] text-white justify-center flex flex-col"> מצטערים יש לנו תקלה כרגע נה לנשות שוב מאוחר יותר</h4>
                    {/* <ErrorPage /> */}
                  </div>
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
                    {attendee.date_arrived ? formatDate(attendee.date_arrived) : "—"}
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
