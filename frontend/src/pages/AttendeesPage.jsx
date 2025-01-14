import withReactContent from "sweetalert2-react-content";
import * as XLSX from "xlsx";
import { io } from "socket.io-client";
import React, { useEffect, useRef, useState } from "react";
import AddLogo from "../assets/Logos/AddLogo";
import GarbageLogo from "../assets/Logos/GarbageLogo";
import Swal from "sweetalert2";
import '../App.css'


const AttendeesPage = () => {
  // const apiUrl = process.env.REACT_APP_API_URL + "/attendees";
  const apiUrl = "http://127.0.0.1:8000" + "/attendees";
  const [attendees, setAttendees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [file, setFile] = useState(null);
  const [addingManual, setAddingManual] = useState(false);
  const [newAttendee, setNewAttendee] = useState({
    mispar_ishi: "",
    tehudat_zehut: "",
    full_name: "",
    arrived: false,
    date_arrived: "",
  });
  
  const [filter, setFilter] = useState({ field: "", value: "" });
  const [sort, setSort] = useState({ field: "", direction: "asc" })
  
  useEffect(() => {
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
    let eventSource = new EventSource(apiUrl+"/clients");

    eventSource.onmessage = (event) => {
      console.log("Mensaje recibido: ", event.data);
    };
  
    eventSource.addEventListener("create", (event) => {
      const data = JSON.parse(event.data);
      console.log("Create recibido:", data);
      setAttendees((prev) => [...prev, ...data.attendees]);
    });

    eventSource.addEventListener("update", (event) => {
      const updatedAttendee = JSON.parse(event.data);
      console.log("Update received:", updatedAttendee);
      setAttendees((prev) =>
        prev.map((attendee) =>
          attendee.id === updatedAttendee.id ? updatedAttendee : attendee
        )
      );
    });

    eventSource.addEventListener("restart_all", () => {
      console.log("Reset all arrived received");
      Swal.fire({
        position: "center",
        icon: "info",
        title: "מנהל התחיל מחדש את הנוכחות של כל המשתתפים",
        showConfirmButton: false,
        timer: 3500,
        customClass: {
          popup: "custom-popup",
          title: "custom-title-success",        
        },
      })
      setAttendees((prev) =>
        prev.map((attendee) => ({ ...attendee, arrived: false }))
      );
    });

    eventSource.addEventListener("delete_all", () => {
      Swal.fire({
        position: "center",
        icon: "info",
        title: "מנהל מחק את כל המשתתפים",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"    
        },
      })
      console.log("Delete all received");
      setAttendees([])
    });


    eventSource.onerror = (error) => {
      console.error("Error con SSE:", error);
      setTimeout(() => {
        console.log("Intentando reconectar SSE...");
        eventSource = new EventSource(`${apiUrl}/clients`);
      }, 5000);
    };
    
    fetchAttendees();
    Swal.close();
      return () => {
        eventSource.close();
      };
  }, []);
  

  async function fetchAttendees() {
    try {
      const response = await fetch(`${apiUrl}/get`);
      const data = await response.json();
      const attendees = data["data"]
      setAttendees(attendees);
    } catch (error) {
      setLoading(null)
    } finally {
      setLoading(false);
    }
  }

  
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
        let response = await fetch(`${apiUrl}/deleteall`, {
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
      "שם": item.attendee.full_name || "",
      "נוכחות": item.attendee.arrived === true ? "כן" : item.attendee.arrived === false ? "לא" : "",
      "תאריך הגעה": item.attendee.date_arrived || "",
      "שגיאה": item.error.message,
    }));
  
    const worksheet = XLSX.utils.json_to_sheet(formattedData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "שגיאות");
  
    XLSX.writeFile(workbook, "missing_data_errors.xlsx", { bookType: "xlsx", type: "binary" });
  };

  const excelToJSON = (event) => {
    const data = new Uint8Array(event.target.result);
      const workbook = XLSX.read(data, { type: "array" });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      let jsonData = XLSX.utils.sheet_to_json(sheet);

      const columnMapping = {
        "תעודת זהות": "tehudat_zehut",
        "מספר אישי": "mispar_ishi",
        "שם": "full_name",
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
      return jsonData 
  }
  const handleImport = async(e, cameFrom = null) => {
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
    let jsonData = null
    if (cameFrom === null){
      jsonData = excelToJSON(event)
    }
    else{
      
    }
    const toSend = { "attendees": jsonData };
    console.log("toSend", toSend)
      fetch(`${apiUrl}/create`, {
        method: 'POST',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(toSend)
      })
      .then(response => {
        console.log("response" , response)
        Swal.close();
        console.log(response)
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
        setAddingManual(false)
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
      "שםי": attendee.full_name || "",
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
      const response = await fetch(`${apiUrl}/restart`, {
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
  
  const handleManualSubmit = (newAttendee) => {
    setAddingManual(false);
    handleImport(null, newAttendee);
    // setNewAttendee({
    //   mispar_ishi: "",
    //   tehudat_zehut: "",
    //   full_name: "",
    //   arrived: false,
    //   date_arrived: "",
    // });
  };

  const MySwal = withReactContent(Swal);

  const handleAddManual = () => {
    MySwal.fire({
      title: '<h1 class="text-2xl font-bold text-limeConvined">משתתף חדש</h1>',
      html: `
        <div class="flex flex-col gap-4">
          <div class="flex flex-col">
            <label for="full_name" class="text-white font-semibold">שם מלא *</label>
            <input
              id="full_name"
              type="text"
              placeholder="הכנס שם מלא"
              class="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
            />
            <small class="text-redConvinedStronger mt-1">שדה זה חובה</small>
          </div>
          <div class="flex flex-col">
            <label for="mispar_ishi" class="text-white font-semibold">מספר אישי</label>
            <input
              id="mispar_ishi"
              type="number"
              placeholder="הכנס מספר אישי"
              class="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
            />
            <small class="text-gray-400 mt-1">שדה לא חובה</small>
          </div>
          <div class="flex flex-col">
            <label for="tehudat_zehut" class="text-white font-semibold">תעודת זהות</label>
            <input
              id="tehudat_zehut"
              type="number"
              placeholder="הכנס תעודת זהות"
              class="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
            />
            <small class="text-gray-400 mt-1">שדה לא חובה</small>
          </div>
          <div class="flex flex-col">
            <label for="attendance" class="text-white font-semibold">נוכחות</label>
            <select
              id="attendance"
              value=""
              class="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
            >
              <option value={null}>בחר נוכחות</option>
              <option value="כן">כן</option>
              <option value="לא">לא</option>
            </select>
            <small class="text-gray-400 mt-1">שדה לא חובה</small>
          </div>
          <div class="flex flex-col">
            <label for="date_arrived" class="text-white font-semibold">תאריך הגעה</label>
            <input
              id="date_arrived"
              type="datetime-local"
              class="bg-gray-600 p-2 rounded focus:outline-none focus:ring-2 focus:ring-turquiseConvined"
            />
            <small class="text-gray-400 mt-1">שדה לא חובה</small>
          </div>
        </div>
      `,
      showCancelButton: true,
      confirmButtonText: "הוסף",
      cancelButtonText: "ביטול",
      customClass: {
        popup: "custom-popup bg-gray-700 p-6 rounded-lg shadow-xl",
        confirmButton: "bg-greenConvined text-black p-2 rounded-lg hover:bg-green-700",
        cancelButton: "bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700",
      },
      preConfirm: () => {
        const full_name = document.getElementById("full_name").value.trim();
        const mispar_ishi = document.getElementById("mispar_ishi").value.trim();
        const tehudat_zehut = document.getElementById("tehudat_zehut").value.trim();
        const attendance = document.getElementById("attendance").value;
        const date_arrived = document.getElementById("date_arrived").value;
          if (!full_name) {
          Swal.showValidationMessage("יש למלא שם");
          return false;
        }
  
        if (!tehudat_zehut && !mispar_ishi) {
          Swal.showValidationMessage("יש למלא מספר אישי או תעודת זהות");
          return false;
        }
  
        if (tehudat_zehut && !/^\d{9}$/.test(tehudat_zehut)) {
          Swal.showValidationMessage("תעודת זהות חייבת להכיל 9 ספרות");
          return false;
        }
  
        if (mispar_ishi && mispar_ishi.length < 6) {
          Swal.showValidationMessage("מספר אישי חייב להכיל לפחות 6 ספרות");
          return false;
        }
  
        if (attendance === "כן" && !date_arrived) {
          Swal.showValidationMessage("אם המשתתף הגיע, יש להזין תאריך ושעה");
          return false;
        }
        handleManualSubmit({
          full_name,
          mispar_ishi,
          tehudat_zehut,
          arrived: attendance === "כן",
          date_arrived: attendance === "כן" ? date_arrived : null,
        });
  
        return true;
      },
    });
  };
  
  const handleFilterChange = (e) => {
    setFilter((prev) => ({ ...prev, value: e.target.value.toLowerCase() }));
  };
  
  const handleFilterFieldChange = (e) => {
    const newField = e.target.value;
  
    setFilter((prev) => {
      const shouldRetainValue =
        (prev.field === "tehudat_zehut" && newField === "mispar_ishi") ||
        (prev.field === "mispar_ishi" && newField === "tehudat_zehut");
  
      return {
        ...prev,
        field: newField,
        value: shouldRetainValue ? prev.value : "",
      };
    });
  };
  
  

  const handleSort = (field) => {
    setSort((prev) => ({
      field,
      direction: prev.field === field && prev.direction === "asc" ? "desc" : "asc",
    }));
  };
  
  
  return (
    <div
      dir="rtl"
      className="transition-all duration-700 bg-bg-desktop bg-cover bg-center h-screen w-screen p-16 flex justify-center items-center"
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
            <div className="flex items-center gap-4">
              <button
                onClick={handleAddManual}
                className="transition-all duration-400 bg-gray-700 hover:bg-lavanderConvined hover:text-black text-white font-semibold py-2 px-4 rounded-lg cursor-pointer"
              >
                הוסף משתתף ידני
              </button>
              <label
                htmlFor="file-upload"
                className="transition-all duration-400 bg-gray-700 hover:bg-greenConvined hover:text-black text-white font-semibold py-2 px-4 rounded-lg cursor-pointer"
              >
                העלה קובץ אקסל
              </label>
              <input
                id="file-upload"
                type="file"
                accept=".xlsx"
                onChange={handleImport}
                className="hidden"
              />
              {file === true && (
                <button
                  onClick={() => {
                    setAdding(false);
                    setFile(null);
                    setAddingManual(false);
                  }}
                  className="transition-all border-none duration-400 bg-redConvinedStronger hover:bg-red-700 text-white font-semibold rounded-full py-2 px-3"
                >
                  ✕
                </button>
              )}
            </div>
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
          <div className="flex flex-row w-full mb-4 mt-6 justify-between px-80">
            <div className="flex items-center w-1/2">
              <select
                onChange={handleFilterFieldChange}
                value={filter.field}
                className="transition-all duration-400 bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 w-1/3 mx-2 text-center"
              >
                <option value="">חפש לפי</option>
                <option value="mispar_ishi">מספר אישי</option>
                <option value="tehudat_zehut">תעודת זהות</option>
                <option value="full_name">שם מלא</option>
                <option value="arrived">נוכחות</option>
                <option value="date_arrived">תאריך הגעה</option>
              </select>
              <div className="flex items-center w-2/3">
                <input
                  type="text"
                  value={filter.value}
                  onChange={handleFilterChange}
                  placeholder="הקלד ערך"
                  className="transition-all duration-400 bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 w-full text-center"
                />
                <div
                  className={`transition-opacity duration-400 ${
                    filter.value ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
                  }`}
                >
                  <button
                    onClick={() => setFilter((prev) => ({ ...prev, value: "" }))}
                    className="bg-redConvinedStronger bg-opacity-55 border-transparent border-none text-white font-semibold rounded-full py-2 px-3 mr-2"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
            <div className="flex items-center w-1/2 justify-end">
              <select
                onChange={(e) => handleSort(e.target.value)}
                className="transition-all duration-400 bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 w-1/3 mx-2 text-center"
              >
                <option value="">מיין לפי</option>
                <option value="mispar_ishi">מספר אישי</option>
                <option value="tehudat_zehut">תעודת זהות</option>
                <option value="full_name">שם</option>
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
                className="border-none hover:border-none text-sm transition-all duration-400 bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full text-center h-16 w-16 flex flex-col justify-center items-center"
              >
                {sort.direction === "asc" ? (
                  <>
                    <span>סדר</span>
                    <span>עולה</span>
                  </>
                ) : (
                  <>
                    <span>סדר</span>
                    <span>יורד</span>
                  </>
                )}
              </button>
            </div>
          </div>

        <div className="transition-all duration-400 overflow-y-auto max-h-[500px] rounded-lg">
          <table className="w-full text-right bg-gray-700 bg-opacity-70 rounded-lg overflow-hidden">
            <thead className="bg-gray-600 text-gray-300 sticky top-0 z-10">
              <tr>
                <th className="px-4 py-2 text-center">מספר אישי</th>
                <th className="px-4 py-2 text-center">תעודת זהות</th>
                <th className="px-4 py-2 text-center">שם</th>
                <th className="px-4 py-2 text-center">נוכחות</th>
                <th className="px-4 py-2 text-center">תאריך הגעה</th>
              </tr>
            </thead>
            <tbody>
              {filteredAttendees.map((attendee, index) => (
                <tr
                  key={index}
                  className="transition-all duration-400 border-b bg-gray-800 border-gray-600 hover:bg-gray-600"
                >
                  <td className="transition-all duration-400 px-4 py-2 text-limeConvined text-lg text-center">
                    {attendee.mispar_ishi}
                  </td>
                  <td className="transition-all duration-400 px-4 py-2 text-turquiseConvined text-lg text-center">
                    {attendee.tehudat_zehut}
                  </td>
                  <td className="transition-all duration-400 px-4 py-2 text-greenConvined text-lg text-center">
                    {attendee.full_name}
                  </td>
                  <td className="transition-all duration-400 px-4 py-2 text-lavanderConvined text-lg text-center">
                    {attendee.arrived ? "כן" : "לא"}
                  </td>
                  <td className="transition-all duration-400 px-4 py-2 text-pinkConvined text-lg text-center">
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
