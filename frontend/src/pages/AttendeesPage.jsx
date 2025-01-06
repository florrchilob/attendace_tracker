import * as XLSX from "xlsx";
import React, { useEffect, useRef, useState } from "react";
import AddLogo from "../assets/Logos/AddLogo";
import GarbageLogo from "../assets/Logos/GarbageLogo";
import Swal from "sweetalert2";
import '../App.css'

const AttendeesPage = () => {
  const [attendees, setAttendees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [file, setFile] = useState(null);
  const titles = [
    "מספר אישי",
    "תעודת זהות",
    "שם מלא",
    "נוכחות",
    "תאריך הגעה"
  ];
  const [filter, setFilter] = useState({ field: "", value: "" });
  const [sort, setSort] = useState({ field: "", direction: "asc" })
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    // Abrir conexión
    socket.onopen = () => {
      console.log("Conectado al WebSocket");
      socket.send("Hola desde el cliente");
    };

    // Recibir mensajes
    socket.onmessage = (event) => {
      console.log("Mensaje recibido:", event.data);
    };

    // Manejar errores
    socket.onerror = (error) => {
      console.error("Error en WebSocket:", error);
    };

    // Cerrar conexión
    socket.onclose = () => {
      console.log("Conexión cerrada");
    };

  }, []);

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
    Swal.fire({
      title: "האם ברצונך למחוק את כל המשתתפים?",
      text: '"delete"' + ' כדי לאשר למחוק כתוב' ,
      input: "text",
      inputPlaceholder: '"delete" כתוב  כאן',
      showCancelButton: true,
      confirmButtonText: "מחק",
      cancelButtonText: "ביטול",
      customClass: {
        popup: "custom-popup-505",
        title: "custom-popup-505-title"
      },
      preConfirm: (inputValue) => {
        if (inputValue !== "delete") {
          Swal.showValidationMessage('עליך לכתוב "delete" כדי לאשר את המחיקה');
          return false;
        }
        return true;
      }
    }).then(async (result) => {
      if (result.isConfirmed) {
        exportToExcel()
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
            text: "אם זו הייתה שגיאה, הרשימה המלאה הורדה, הזן אותה שוב",
            showConfirmButton: false,
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
      } else if (result.dismiss === Swal.DismissReason.cancel) {
        Swal.fire({
          position: "center",
          icon: "info",
          title: "המחיקה בוטלה",
          showConfirmButton: false,
          timer: 2500,
          customClass: {
            popup: "custom-popup-505",
            title: "custom-popup-505-title"          
          },
        })
      }
    });
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
    Swal.fire({
      title: "טוען...",
      html: "אנא המתן בזמן שהנתונים נטענים.",
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading()
      },
      customClass: {
        popup: "custom-popup",
        title: "custom-title-success",
      },
    });
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
        Swal.close();
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

  const handleRestartAttendace = async() => {

    try { 
      const response = await fetch("http://127.0.0.1:8000/attendees/restart", {
      method: 'PUT',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      }
    });  
      if(response.status === 500){
        setLoading(null)
      }
    } catch (error) {
      setLoading(null)
    } finally {
      fetchAttendees();
    }
  }

  const handleFilterChange = (e) => {
    setFilter((prev) => ({ ...prev, value: e.target.value.toLowerCase() }));
  };
  
  const handleFilterFieldChange = (e) => {
    setFilter((prev) => ({ ...prev, field: e.target.value }));
  };
  
  

useEffect(() => {
  console.log(file)
}, [file])

const filteredAttendees = attendees
  .filter((attendee) => {
    if (!filter.field || !filter.value) return true;

    if (filter.field === "arrived") {
      const arrivedValue = filter.value === "כן" ? true : filter.value === "לא" ? false : null;
      return attendee.arrived === arrivedValue;
    }

    const value = attendee[filter.field]?.toString().toLowerCase();
    return value && value.includes(filter.value);
  })
  .sort((a, b) => {
    if (!sort.field) return 0;
    const aValue = a[sort.field]?.toString().toLowerCase() || "";
    const bValue = b[sort.field]?.toString().toLowerCase() || "";

    if (sort.direction === "asc") {
      return aValue.localeCompare(bValue);
    } else {
      return bValue.localeCompare(aValue);
    }
  });



  const handleSort = (field) => {
    setSort((prev) => ({
      field,
      direction: prev.direction === "asc" ? "desc" : "asc", // Alterna entre ascendente y descendente
    }));
  };
  
  useEffect(() => {
    if (attendees.length > 0 && filteredAttendees.length === 0 && (filter.field || filter.value)) {
      Swal.fire({
        position: "center",
        icon: "warning",
        title: "לא נמצאו תוצאות",
        text: "נסה לשנות את החיפוש או לבדוק את הנתונים.",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
    }
  }, [filteredAttendees]);
  

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
          {!adding ? (
            <div className="flex items-center space-x-2 transition-all duration-500 flex-row py-auto">
              <div className="flex flex-row">
                <button
                        onClick={handleDelete}
                        className="transition-all duration-500 block mb-4 bg-transparent hover:bg-redConvinedStronger
                  border-white hover:border-white font-semibold justify-start text-white bg-gray-700 rounded-full p-4 me-4"
                  >
                  <GarbageLogo/>
                </button>
                <button
                  onClick={() => {setAdding(true); setFile(true)}}
                  className="transition-all duration-500 block mb-4 bg-transparent hover:bg-pinkConvined
                  border-white hover:border-white font-semibold justify-start text-white bg-gray-700 rounded-full px-4"
                  >
                  <AddLogo />
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-row">
              <input
                type="file"
                accept=".xlsx"
                onChange={handleImport}
                className="transition-all duration-400 block my-4 bg-transparent hover:bg-lavanderConvined
                border-white hover:border-white font-semibold justify-start text-white bg-gray-700 rounded-lg p-2 flex-col"
                />
              {file === true &&
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
          )}
          <div className="flex flex-row items-center">
            <div className="flex justify-end">
              <button
                onClick={handleRestartAttendace}
                className="transition-all duration-400 px-4 py-2 bg-transparent hover:border-lavanderConvined text-lavanderConvined font-semibold rounded-lg border border-white"
                >
                להפעיל מחדש כניסות                
              </button>
            </div>
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

        <div className="flex flex-row my-5 w-full">
          <div className="flex w-full justify-center gap-40">
            <div className="flex flex-row border-none hover:border-orangeConvined rounded-full">
              <select
                onChange={handleFilterFieldChange}
                value={filter.field}
                className="transition-all duration-400 block bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 text-center hover:border-orangeConvined focus:border-orangeConvined"
              >
                <option value="">חפש לפי</option>
                <option value="mispar_ishi">מספר אישי</option>
                <option value="tehudat_zehut">תעודת זהות</option>
                <option value="full_name">שם מלא</option>
                <option value="arrived">נוכחות</option>
                <option value="date_arrived">תאריך הגעה</option>
              </select>

              <input
                type="text"
                value={filter.value}
                onChange={handleFilterChange}
                placeholder="הקלד ערך"
                className="transition-all duration-400 block bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 text-center hover:border-orangeConvined focus:border-orangeConvined"
              />
            </div>

            <div className="flex flex-row border-none hover:border-orangeConvined rounded-full">
              <select
                onChange={(e) => handleSort(e.target.value)}
                className="transition-all duration-400 block bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 w-full mx-2 text-center hover:border-orangeConvined focus:border-orangeConvined"
              >
                <option value="">מיין לפי</option>
                <option value="mispar_ishi">מספר אישי</option>
                <option value="tehudat_zehut">תעודת זהות</option>
                <option value="full_name">שם מלא</option>
                <option value="arrived">נוכחות</option>
                <option value="date_arrived">תאריך הגעה</option>
              </select>
              <button
                onClick={() =>
                  setSort((prev) => ({
                    ...prev,
                    direction: prev.direction === "asc" ? "desc" : "asc",
                  }))
                }
                className="transition-all duration-400 block bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 text-center hover:border-orange-500 w-24  items-center justify-center"
              >
                {sort.direction === "asc" ? "סדר עולה" : "סדר יורד"}
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
            {filteredAttendees.map((attendee, index) => (
              <tr
                key={index}
                className="border-b bg-gray-800 border-gray-600 hover:bg-gray-600"
              >
                <td className="px-4 py-2 text-limeConvined text-lg text-center">
                  {attendee.mispar_ishi}
                </td>
                <td className="px-4 py-2 text-turquiseConvined text-lg text-center">
                  {attendee.tehudat_zehut}
                </td>
                <td className="px-4 py-2 text-greenConvined text-lg text-center">
                  {attendee.full_name}
                </td>
                <td className="px-4 py-2 text-lavanderConvined text-lg text-center">
                  {attendee.arrived ? "כן" : "לא"}
                </td>
                <td className="px-4 py-2 text-pinkConvined text-lg text-center">
                  {attendee.date_arrived ? formatDate(attendee.date_arrived) : "—"}
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
