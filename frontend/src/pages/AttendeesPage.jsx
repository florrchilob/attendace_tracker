import withReactContent from "sweetalert2-react-content";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import * as XLSX from "xlsx";
import { io } from "socket.io-client";
import React, { useEffect, useRef, useState } from "react";
import AddLogo from "../assets/Logos/AddLogo";
import GarbageLogo from "../assets/Logos/GarbageLogo";
import Swal from "sweetalert2";
import '../App.css'
import EditLogo from "../assets/Logos/EditLogo";
import DeleteUserLogo from "../assets/Logos/DeleteUserLogo";
import "react-datepicker/dist/react-datepicker.css";
import { registerLocale } from "react-datepicker";
import { format } from "date-fns";
import he from "date-fns/locale/he";

const AttendeesPage = () => {
  const apiUrl = import.meta.env.VITE_BACKEND_URL + "/attendees"
  const [attendees, setAttendees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [file, setFile] = useState(null);
  const [addingManual, setAddingManual] = useState(false);
  const [vibrate, setVibrate] = useState(false)
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({
    mispar_ishi: "",
    tehudat_zehut: "",
    full_name: "",
    arrived: false,
    date_arrived: ""
  });
  const [manual, setManual] = useState({
    mispar_ishi: "",
    tehudat_zehut: "",
    full_name: "",
    arrived: false,
    date_arrived: ""
  })

  const placeholderMap = {
    mispar_ishi: "הקלד מספר אישי",
    tehudat_zehut: "הקלד תעודת זהות",
    full_name: "הקלד שם מלא",
    arrived: "הקלד נוכחות",
    date_arrived: "הקלד תאריך הגעה"
  };

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
    let eventSource = new EventSource(apiUrl + "/clients");

    eventSource.onmessage = (event) => {
      console.log("Message received: ", event.data);
    };

    eventSource.addEventListener("create", (event) => {
      const data = JSON.parse(event.data);
      console.log("Create received (raw):", data);
      const formattedAttendees = data.attendees.map((attendee) => ({
        ...attendee,
        dateArrived: attendee.dateArrived
          ? formatDate(attendee.dateArrived)
          : null,
      }));

      console.log("Create received (formatted):", formattedAttendees);

      setAttendees((prev) => [...prev, ...formattedAttendees]);
    });

    eventSource.addEventListener("update", (event) => {
      const updatedAttendee = JSON.parse(event.data);
      console.log("Update received:", updatedAttendee);
      setAttendees((prev) =>
        prev.map((attendee) =>
          attendee.id === updatedAttendee.id
            ? { ...attendee, ...updatedAttendee }
            : attendee
        )
      );
    });

    eventSource.addEventListener("delete_user", (event) => {
      const idUserDelete = JSON.parse(event.data).id;
      setAttendees((prev) => prev.filter((attendee) => attendee.id !== idUserDelete));
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
        console.log("Trying to reconect  SSE...");
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
      const attendees = data["data"].map((attendee) => ({
        ...attendee,
        dateArrived: attendee.dateArrived
          ? formatDate(attendee.dateArrived)
          : null,
      }));

      setAttendees(attendees);
    } catch (error) {
      console.error("Error fetching attendees:", error);
      setLoading(null);
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

  const handleDelete = async () => {
    Swal.fire({
      title: "האם ברצונך למחוק את כל המשתתפים?",
      text: '"delete"' + ' כדי לאשר למחוק כתוב',
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
        else {
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

  const handleDeleteUser = async (id) => {
    Swal.fire({
      title: "האם ברצונך למחוק את כל המשתתפים?",
      text: '"delete"' + ' כדי לאשר למחוק כתוב',
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
        let response = await fetch(`${apiUrl}/delete/${id}`, {
          method: 'DELETE',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
          }
        });

        if (response.status === 200) {
          setAttendees((prev) => prev.filter((attendee) => attendee.id !== id));
          Swal.fire({
            position: "center",
            icon: "success",
            title: "המשתתף הורס בהצלחה",
            timer: 2500,
            showConfirmButton: false,
            customClass: {
              popup: "custom-popup",
              title: "custom-title-success",
            },
          })
        }
        else {
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

  const handleImport = async (e, sent = null) => {
    try {
      Swal.fire({
        title: "טוען...",
        html: "אנא המתן בזמן שהנתונים נטענים.",
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading(),
        customClass: {
          popup: "custom-popup",
          title: "custom-title-success",
        },
      });

      let jsonData = null;

      if (sent === null) {
        setFile(true);
        const file = e.target.files[0];
        const reader = new FileReader();

        jsonData = await new Promise((resolve, reject) => {
          reader.onload = (event) => resolve(excelToJSON(event));
          reader.onerror = (error) => reject(error);
          reader.readAsArrayBuffer(file);
        });
      } else {
        jsonData = sent;
      }

      await sendDataToAPI(jsonData);
    } catch (error) {
      console.error("Error in handleImport:", error);
      Swal.fire({
        position: "center",
        icon: "error",
        title: "שגיאה בלתי צפויה",
        text: "נסה שוב מאוחר יותר",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title",
        },
      });
    } finally {
      if (sent === null) {
        fetchAttendees();
      }
      setAdding(false);
      setAddingManual(false);
    }
  };

  const sendDataToAPI = async (data) => {
    const toSend = { attendees: data };
    try {
      const response = await fetch(`${apiUrl}/create`, {
        method: "POST",
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(toSend),
      });

      if (response.status == 500) {
        throw new Error(`Server error: ${response.status}`);
      }
      const dataResponse = await response.json();
      handleAPIResponse(dataResponse);
    } catch (error) {
      console.error("Error in sendDataToAPI:", error);
      Swal.fire({
        position: "center",
        icon: "error",
        title: "שגיאת שרת פנימית",
        text: "נסה שוב מאוחר יותר",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title",
        },
      });
    }
  };

  const handleAPIResponse = (dataResponse) => {
    const missingData = dataResponse?.data?.missing_data || [];
    if (dataResponse.error_code) {
      if (dataResponse.error_code == 101) {
        Swal.fire({
          position: "center",
          icon: "warning",
          title: "בדוק פרטים בבקשה",
          text: "בדוק את תיקיית ההורדות, הורד אקסל עם המשתמשים שיש להם שגיאות, אנא תקן את הנתונים שהוזנו עבור כל משתתף",
          showConfirmButton: false,
          timer: 2000,
          customClass: {
            popup: "custom-popup-505",
            title: "custom-popup-505-title",
          },
        });
        exportErrorsToExcel(missingData);
      }
    }
    else {
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
            title: "custom-popup-505-title",
          },
        });
        exportErrorsToExcel(missingData);
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
    }
  };


  function exportToExcel() {
    if (!attendees || attendees.length === 0) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "אין נתונים לייצוא.",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title",
        },
      });
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

  const handleRestartAttendace = async () => {
    Swal.fire({
      title: "\u202Eהאם ברצונך לעדכן את כל המשתתפים כלא נוכחים?",
      text: 'כתוב "restart" כדי לאשר את העדכון',
      input: "text",
      inputPlaceholder: '"restart" כתוב כאן',
      showCancelButton: true,
      confirmButtonText: "עדכן",
      cancelButtonText: "ביטול",
      customClass: {
        popup: "custom-popup-505",
        title: "custom-popup-505-title"
      },
      preConfirm: (inputValue) => {
        if (inputValue !== "restart") {
          Swal.showValidationMessage('עליך לכתוב "restart" כדי לאשר את העדכון');
          return false;
        }
        return true;
      }
    }).then(async (result) => {
      try {
        const response = await fetch(`${apiUrl}/restart`, {
          method: 'PUT',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
          }
        });
        if (response.status === 500) {
          setLoading(null)
        }
      } catch (error) {
        setLoading(null)
      } finally {
        fetchAttendees();
      }
    })
  }

  registerLocale("he", he);

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

  const MySwal = withReactContent(Swal);

  const handleFilterChange = (e) => {
    setFilter((prev) => ({ ...prev, value: e.target.value.toLowerCase() }));
  };

  const handleFilterFieldChange = (e) => {
    const newField = e.target.value;

    setFilter((prev) => {
      const shouldRetainValue =
        (prev.field === "tehudat_zehut" && newField === "mispar_ishi") ||
        (prev.field === "mispar_ishi" && newField === "tehudat_zehut") ||
        prev.value === "";

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

  const handleManualSubmit = async () => {
    if (!manual.full_name || manual.full_name.trim() === "") {
      setVibrate(true);
      setTimeout(() => {
        setVibrate(false);
      }, 500);
      return;
    }
    if (!manual.tehudat_zehut && !manual.mispar_ishi) {
      setVibrate(true);
      setTimeout(() => {
        setVibrate(false);
      }, 500);
      return;
    }
    if (manual.tehudat_zehut && (!/^\d{9}$/.test(manual.tehudat_zehut))) {
      setVibrate(true);
      setTimeout(() => {
        setVibrate(false);
      }, 500);
      return;
    }
    if (manual.mispar_ishi && (!/^\d{6,}$/.test(manual.mispar_ishi))) {
      setVibrate(true);
      setTimeout(() => {
        setVibrate(false);
      }, 500);
      return;
    }
    if (manual.arrived === true && (!manual.date_arrived || manual.date_arrived.trim() === "")) {
      setVibrate(true);
      setTimeout(() => {
        setVibrate(false);
      }, 500);
      return;
    }

    if (manual.mispar_ishi && manual.mispar_ishi.startsWith('0')) {
      manual.mispar_ishi = manual.mispar_ishi.slice(1);
    }

    const isDuplicate = attendees.some(
      (attendee) =>
        (manual.tehudat_zehut && attendee.tehudat_zehut === manual.tehudat_zehut) ||
        (manual.mispar_ishi && attendee.mispar_ishi === manual.mispar_ishi)
    );

    if (isDuplicate) {
      setVibrate(true);
      Swal.fire({
        position: "center",
        icon: "error",
        title: "תעודת זהות או מספר אישי כבר קיימים ברשימה.",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title",
        },
      });
      return;
    }
    setVibrate(true);
    setTimeout(() => {
      setVibrate(false);
    }, 500);

    const cleanManual = Object.fromEntries(
      Object.entries(manual).filter(([key, value]) => value !== "" && value !== null && value !== undefined)
    );
    await handleImport(null, [cleanManual]);

    setManual({
      mispar_ishi: "",
      tehudat_zehut: "",
      full_name: "",
      arrived: false,
      date_arrived: ""
    })
  };


  const handleEdit = (id) => {
    const attendeeToEdit = attendees.find((attendee) => attendee.id === id);
    setEditingId(id);
    setEditData(attendeeToEdit);
  };

  const handleEditSubmit = async () => {
    if (!editData.full_name || editData.full_name.trim() === "") {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "שם מלא הוא שדה חובה",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
      return;
    }

    if (!editData.tehudat_zehut && !editData.mispar_ishi) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "תעודת זהות או מספר אישי הם שדות חובה",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
      return;
    }

    if (editData.tehudat_zehut && (!/^\d{9}$/.test(editData.tehudat_zehut))) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "תעודת הזהות חייבת להיות בת 9 ספרות",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
      return;
    }

    if (editData.mispar_ishi && (!/^\d{6,}$/.test(editData.mispar_ishi))) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "המספר האישי חייב להיות בעל 6 ספרות לפחות",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
      return;
    }

    if (editData.arrived === true && (!editData.date_arrived || editData.date_arrived.trim() === "")) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "שדה תאריך הגעה הוא חובה",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
      return;
    }

    const originalData = attendees.find((attendee) => attendee.id === editingId);

    if (!originalData) {
      console.error("Original data not found");
      return;
    }

    if (editData.mispar_ishi && editData.mispar_ishi.startsWith('0')) {
      editData.mispar_ishi = editData.mispar_ishi.slice(1);
    }

    const isDuplicate = attendees.some(
      (attendee) =>
        attendee.id !== editingId &&
        ((editData.tehudat_zehut && attendee.tehudat_zehut === editData.tehudat_zehut) ||
          (editData.mispar_ishi && attendee.mispar_ishi === editData.mispar_ishi))
    );

    if (isDuplicate) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "תעודת זהות או מספר אישי כבר קיימים ברשימה",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title"
        },
      });
      return;
    }

    const changes = { id: editingId };
    Object.keys(editData).forEach((key) => {
      if (editData[key] !== originalData[key]) {
        changes[key] = editData[key];
      }
    });

    if (Object.keys(changes).length === 1) { 
      console.log("No changes were made.");
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/edit`, {
        method: "PUT",
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(changes),
      });

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
            title: "custom-popup-505-title",
          },
        });
      }
    } catch (error) {
      Swal.fire({
        position: "center",
        icon: "error",
        title: "שגיאת שרת פנימית",
        text: "נסה שוב מאוחר יותר",
        showConfirmButton: false,
        timer: 2500,
        customClass: {
          popup: "custom-popup-505",
          title: "custom-popup-505-title",
        },
      });
    }

    setAttendees((prev) =>
      prev.map((attendee) =>
        attendee.id === editingId ? { ...attendee, ...editData } : attendee
      )
    );
    setEditingId(null);
    setEditData({});
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
                  <GarbageLogo />
                </button>
                <button
                  onClick={() => { setAdding(true); setFile(true) }}
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
                  onClick={() => setAddingManual(true)}
                  className="transition-all duration-400 bg-gray-700 hover:bg-lavanderConvined hover:text-black text-white font-semibold py-2 px-4 rounded-lg cursor-pointer"
                >
                  הוסף משתתף ידני
                </button>
                <div className="flex items-center gap-4 relative">
                  <label
                    htmlFor="file-upload"
                    className="transition-all duration-400 bg-gray-700 hover:bg-greenConvined hover:text-black text-white font-semibold py-2 px-4 rounded-lg cursor-pointer relative w-full text-center"
                    onMouseEnter={() => setIsHovered(true)}
                    onMouseLeave={() => setIsHovered(false)}
                  >
                    {isHovered && (
                      <div className="absolute -top-16 left-0 w-full bg-gray-800 text-white text-xs rounded-md px-2 py-1 text-center">
                        כותרות נדרשות באקסל: שם ותעודת זהות או מספר אישי, כתובים בדיוק כך.
                        כותרות אופציונליות: נוכחות ותאריך הגעה
                      </div>
                    )}
                    העלה קובץ אקסל
                    <input id="file-upload"
                      type="file"
                      accept=".xlsx"
                      onChange={handleImport}
                      className="hidden"
                    />
                  </label>
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
            </div>

          )}
          <div className="flex flex-row items-center">
            <div className="flex justify-end">
              <button
                onClick={handleRestartAttendace}
                className="transition-all duration-400 px-4 py-2 bg-transparent hover:border-lavanderConvined text-lavanderConvined font-semibold rounded-lg border border-white"
              >
                איפוס נוכחות
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
              <option value="full_name">שם</option>
              <option value="arrived">נוכחות</option>
              <option value="date_arrived">תאריך הגעה</option>
            </select>
            <div className="flex items-center w-2/3 transform-all duration-700">
              {
                filter.field != "" &&
                <input
                  type="text"
                  value={filter.value}
                  onChange={handleFilterChange}
                  placeholder={placeholderMap[filter.field] || "הקלד ערך"}
                  className="transition-all duration-400 bg-gray-700 bg-opacity-70 text-white font-semibold rounded-full p-2 w-full text-center"
                />
              }
              <div
                className={`transition-opacity duration-400 ${filter.value ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
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
                <th className="px-4 py-2 text-center w-48">תאריך הגעה</th>
                <th className="py-2 text-center">פעולות עם <br /> המשתמש היחיד</th>
              </tr>
            </thead>
            <tbody>
              {
                addingManual &&
                <tr
                  className="transition-all duration-400 border-b h-14 border-gray-600"
                >
                  <td className="transition-all w-min justify-center mx-auto duration-400 text-center">
                    <input
                      type="number"
                      value={manual.mispar_ishi}
                      onChange={(e) => setManual((prev) => ({ ...prev, mispar_ishi: e.target.value }))}
                      placeholder={"משתתף חדש"} 
                      className="transition-all text-gray-800 duration-400 mt-2 mb-1 bg-white text-center  focus:outline-limeConvined rounded-sm hover:shadow-[0_0_10px_rgba(174,247,142,1)]"
                    />
                    <div className="h-3">
                      {
                        manual.mispar_ishi === "" && manual.tehudat_zehut === "" &&
                        <small className={`block text-[10px] text-redConvinedStronger ${vibrate === true ? "animate-vibrate" : ""
                          }`}>
                          *  מ.א או ת.ז חובה
                        </small>
                      }
                      {
                        manual.mispar_ishi !== "" && (manual.mispar_ishi && (!/^\d{6,}$/.test(manual.mispar_ishi))) &&
                        <small className={`block text-[10px] text-redConvinedStronger ${vibrate === true ? "animate-vibrate" : ""
                          }`}>
                          * המ.א חייב להיות בעל 6 ספרות לפחות
                        </small>
                      }
                    </div>
                  </td>
                  <td className="transition-all w-min justify-center mx-auto duration-400 text-center">
                    <input
                      type="text"
                      value={manual.tehudat_zehut}
                      placeholder={"משתתף חדש"} 
                      onChange={(e) => setManual((prev) => ({ ...prev, tehudat_zehut: e.target.value }))}
                      className="transition-all text-gray-800 duration-400 mt-2 mb-1 bg-white  text-center focus:outline-turquiseConvined  rounded-sm hover:shadow-[0_0_10px_rgba(141,247,246,1)]"
                    />
                    <div className="h-3">
                      {
                        manual.tehudat_zehut === "" && manual.mispar_ishi === "" &&
                        <small className={`block text-[10px] text-redConvinedStronger ${vibrate === true ? "animate-vibrate" : ""
                          }`}>
                          * ת.ז או מ.א חובה
                        </small>
                      }
                      {
                        manual.tehudat_zehut !== "" && (manual.tehudat_zehut && (!/^\d{9}$/.test(manual.tehudat_zehut))) &&
                        <small className={`block text-[10px] text-redConvinedStronger ${vibrate === true ? "animate-vibrate" : ""
                          }`}>
                          *  הת.ז חייבת להיות בת 9 ספרות
                        </small>
                      }
                    </div>
                  </td>
                  <td className="transition-all w-min justify-center mx-auto duration-400 text-center">
                    <input
                      type="text"
                      value={manual.full_name}
                      placeholder={"משתתף חדש"} 
                      onChange={(e) => setManual((prev) => ({ ...prev, full_name: e.target.value }))}
                      className="transition-all text-gray-800 mt-2 mb-1 duration-400 bg-white roundee text-center focus:outline-greenConvined rounded-sm hover:shadow-[0_0_10px_rgba(141,249,176,1)]"
                    />
                    <div className="h-3">
                      {
                        manual.full_name === "" &&
                        <small className={`block text-[10px] text-redConvinedStronger ${vibrate === true ? "animate-vibrate" : ""
                          }`}>
                          * ת.ז או מ.א חובה
                        </small>
                      }
                    </div>
                  </td>
                  <td className="transition-all duration-400 px-4 py-2 text-lg text-center">
                    <select
                      onChange={(e) =>
                        setManual((prev) => ({
                          ...prev,
                          arrived: JSON.parse(e.target.value),
                        }))
                      }
                      className="duration-400 mx-2 text-center text-gray-800 transition-all duration-400 bg-white focus:outline-lavanderConvined rounded-sm hover:shadow-[0_0_10px_rgba(141,145,247,1)]"
                    >
                      <option value={false}>לא</option>
                      <option value={true}>כן</option>
                    </select>
                    <div className="h-3">
                    </div>
                  </td>
                  <td className="transition-all w-min justify-center mx-auto duration-400 text-center">
                    {
                      manual.arrived === true &&
                      <div>
                        <DatePicker
                          selected={manual.date_arrived ? new Date(manual.date_arrived) : null}
                          placeholderText="בחר תאריך"
                          onChange={(date) => {
                            const formattedDate = format(date, "yyyy-MM-dd HH:mm:ss");
                            setManual((prev) => ({
                              ...prev,
                              date_arrived: formattedDate,
                            }));
                          }}
                          showTimeSelect
                          timeIntervals={15}
                          dateFormat="yyyy-MM-dd HH:mm:ss"
                          className="transition-all mt-2 text-gray-800 mb-1 duration-400 bg-white text-center focus:outline-pinkConvined rounded-sm hover:shadow-[0_0_10px_rgba(242,141,247,1)]"
                          locale="he"
                          inputMode="numeric"
                          autoComplete="off"
                          maxLength={19}
                        />
                        <div className="h-3">
                          {manual.date_arrived === "" && (
                            <small
                              className={`block text-[10px] text-redConvinedStronger ${vibrate === true ? "animate-vibrate" : ""
                                }`}
                            >
                              * שדה זה חובה
                            </small>
                          )}
                        </div>
                      </div>
                    }
                  </td>
                  <td className="transition-all duration-400 px-4 py-2 text-center">
                    <button onClick={handleManualSubmit} className="focus:outline-greenConvined text-green-900 font-bold rounded-2xl border-none border-transparent bg-greenConvined px-2 py-1 shadow-[0_0_20px_rgba(141,249,176,1)]">  להוסיף </button>
                    <button onClick={() => {
                      setAddingManual(false)
                      setManual({
                        mispar_ishi: "",
                        tehudat_zehut: "",
                        full_name: "",
                        arrived: false,
                        date_arrived: "",
                      });
                    }}
                      className="focus:outline-none underline text-redConvinedStronger text-sm font-serif border-none border-transparent  px-2 py-1 ms-3">  לבטל
                    </button>
                  </td>
                </tr>
              }
              {filteredAttendees.map((attendee, index) => (
                (editingId !== attendee.id ?
                  (
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
                      <td className="flex transition-all duration-400 text-lg gap-10 justify-center">
                        <button className="text-sm text-white rounded-md hover:border-redConvinedStronger p-1 my-1" onClick={() => handleDeleteUser(attendee.id)}><DeleteUserLogo /></button>
                        <button className="text-sm text-white rounded-md hover:border-yellowConvined p-1 my-1" onClick={() => handleEdit(attendee.id)}> <EditLogo /> </button>
                      </td>
                    </tr>
                  ) :
                  (
                    <tr
                      className="transition-all duration-400 border-b border-gray-600"
                      key={index}
                    >
                      <td className="transition-all justify-center mx-auto duration-400 text-center">
                        <input
                          type="number"
                          value={editData.mispar_ishi || ""}
                          onChange={(e) => setEditData((prev) => ({ ...prev, mispar_ishi: e.target.value }))}
                          placeholder={placeholderMap[filter.field] || "מספר אישי"}
                          className="transition-all duration-400 mt-2 mb-1 bg-white text-center text-gray-800 focus:outline-limeConvined rounded-sm hover:shadow-[0_0_10px_rgba(174,247,142,1)]"
                        />
                      </td>
                      <td className="transition-all justify-center mx-auto duration-400 text-center">
                        <input
                          type="text"
                          value={editData.tehudat_zehut || ""}
                          placeholder={placeholderMap[filter.field] || "תהודת זהות"}
                          onChange={(e) => setEditData((prev) => ({ ...prev, tehudat_zehut: e.target.value }))}
                          className="transition-all duration-400 mt-2 mb-1 bg-white text-gray-800 text-center focus:outline-turquiseConvined  rounded-sm hover:shadow-[0_0_10px_rgba(141,247,246,1)]"
                        />
                      </td>
                      <td className="transition-all justify-center mx-auto duration-400 text-center">
                        <input
                          type="text"
                          value={editData.full_name || ""}
                          placeholder={placeholderMap[filter.field] || "שם"}
                          onChange={(e) => setEditData((prev) => ({ ...prev, full_name: e.target.value }))}
                          className="transition-all mt-2 mb-1 duration-400 text-gray-800 bg-white roundee text-center focus:outline-greenConvined rounded-sm hover:shadow-[0_0_10px_rgba(141,249,176,1)]"
                        />
                      </td>
                      <td className="transition-all duration-400 px-4 py-2 text-lg text-center">
                        <select
                          onChange={(e) =>
                            setEditData((prev) => ({
                              ...prev,
                              arrived: JSON.parse(e.target.value),
                            }))
                          }
                          value={editData.arrived || false}
                          className="duration-400 mx-2 text-center transition-all text-gray-800 duration-400 bg-white focus:outline-lavanderConvined rounded-sm hover:shadow-[0_0_10px_rgba(141,145,247,1)]"
                        >
                          <option value={false}>לא</option>
                          <option value={true}>כן</option>
                        </select>
                      </td>
                      <td className="transition-all justify-center mx-auto duration-400 text-center">
                        {
                          editData.arrived === true &&
                          <div>
                            <DatePicker
                              selected={editData.date_arrived ? new Date(editData.date_arrived) : null}
                              placeholderText="בחר תאריך"
                              onChange={(date) => {
                                const formattedDate = format(date, "yyyy-MM-dd HH:mm:ss");
                                setEditData((prev) => ({
                                  ...prev,
                                  date_arrived: formattedDate,
                                }));
                              }}
                              showTimeSelect
                              timeIntervals={15}
                              dateFormat="yyyy-MM-dd HH:mm:ss"
                              className="transition-all mt-2 text-gray-800 mb-1 duration-400 bg-white text-center focus:outline-pinkConvined rounded-sm hover:shadow-[0_0_10px_rgba(242,141,247,1)]"
                              locale="he"
                              inputMode="numeric"
                              autoComplete="off"
                              maxLength={19}
                            />
                          </div>
                        }
                      </td>
                      <td className="transition-all duration-400 px-4 py-2 text-center">
                        <button onClick={handleEditSubmit} className="focus:outline-greenConvined text-green-900 font-bold rounded-2xl border-none border-transparent bg-greenConvined px-2 py-1 shadow-[0_0_20px_rgba(141,249,176,1)]">  לשלוח </button>
                        <button onClick={() => {
                          setEditingId(null);
                          setEditData({
                            mispar_ishi: "",
                            tehudat_zehut: "",
                            full_name: "",
                            arrived: false,
                            date_arrived: "",
                          });
                        }}
                          className="focus:outline-none underline text-redConvinedStronger text-sm font-serif border-none border-transparent  px-2 py-1 ms-3">  לבטל
                        </button>
                      </td>
                    </tr>
                  )
                )
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AttendeesPage;
